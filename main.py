# Import necessary libraries
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
from sec_edgar_downloader import Downloader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request





# Download filings to the current working directory
dl = Downloader("Yash", "yashanup@usc.edu")

# To load the HUGGINGFACE_TOKEN from .env file
load_dotenv()


# Using the zephyr-7b-beta inference API to generate insights
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()




def get_section_7_content(soup):
    """
    Function to extract the contents of section 7 from a 10K filing.

    Args:
    soup: BeautifulSoup object representing the parsed XML structure of the filing.

    Returns:
    Text content of section 7 from the 10K filing.
    """

    # Loop through each document in the parsed soup
    for filing_document in soup.find_all('document'):
        document_type = filing_document.type.find(string=True, recursive=False).strip()
        
        # Check if the document type is a 10-K filing
        if document_type == "10-K": 
            # Extract the text from the filing document
            ten_k_text = filing_document.find('text').extract().text
            
            # Set up regex pattern to identify relevant sections
            matches = re.compile(r'(item\s(7[\.\s]|8[\.\s])|'
                                'discussion\sand\sanalysis\sof\s(consolidated\sfinancial|financial)\scondition|'
                                '(consolidated\sfinancial|financial)\sstatements\sand\ssupplementary\sdata)', re.IGNORECASE)
            
            # Create a DataFrame to store matches and their locations
            matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(ten_k_text)])
            matches_array.columns = ['SearchTerm', 'Start']
            rows = matches_array['SearchTerm'].count()
            
            # Merge consecutive matches into single entries
            count = 0 
            while count < (rows-1): 
                matches_array.at[count,'Selection'] = (matches_array.iloc[count,0] + matches_array.iloc[count+1,0]).lower()
                count += 1
            
            # Define regex patterns for identifying Item 7 and Item 8
            matches_item7 = re.compile(r'(item\s7\.discussion\s[a-z]*)')
            matches_item8 = re.compile(r'(item\s8\.(consolidated\sfinancial|financial)\s[a-z]*)')
                
            # Lists to store the locations of Item 7/8 matches
            start_locs = []
            end_locs = []
                
            # Find and store the locations of Item 7/8 matches
            count = 0
            
            while count < (rows-1):
                if re.match(matches_item7, matches_array.at[count,'Selection']):
                    start_locs.append(matches_array.iloc[count,1]) # Store starting location of Item 7

                if re.match(matches_item8, matches_array.at[count,'Selection']):
                    end_locs.append(matches_array.iloc[count,1]) # Store ending location of Item 7
                
                count += 1

            # Extract text corresponding to Item 7
            item_7_text = ten_k_text[start_locs[1]:end_locs[1]]
            
            # Clean the extracted text

            # Remove leading/trailing white spaces
            item_7_text = item_7_text.strip() 
            # Replace new lines with spaces
            item_7_text = item_7_text.replace('\n', ' ')
            # Remove returns
            item_7_text = item_7_text.replace('\r', '')
            # Replace multiple spaces with single space 
            item_7_text = item_7_text.replace(' ', ' ')
            # Replace HTML special space character with space
            item_7_text = item_7_text.replace(' ', ' ')


            while '  ' in item_7_text:
                item_7_text = item_7_text.replace('  ', ' ') # Remove extra spaces

            # Return the cleaned text of Item 7
            return item_7_text





# Function to remove stopwords
def remove_stopwords(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Get English stop words
    stop_words = set(stopwords.words('english'))
    
    # Remove stop words
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Reconstruct text without stop words
    filtered_text = ' '.join(filtered_tokens)
    
    # Return the filtered text
    return filtered_text





# Creating the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def process_input():
    data = {}
    counter = 0
    final_text = []
    final_output = []


    user_input = request.form['user_input'].upper()
    dl.get("10-K", user_input, limit=5)
    main_folder_path = f'sec-edgar-filings/{user_input}/10-K'
    
    for folder_name in os.listdir(main_folder_path):
        folder_path = os.path.join(main_folder_path, folder_name)
        
        # Check if the item in the main folder is a directory (subfolder)
        if os.path.isdir(folder_path):
            
            # Access the file inside the subfolder
            file_path = os.path.join(folder_path, 'full-submission.txt')
            print(file_path)
            # Check if the file exists
            if os.path.isfile(file_path):
                
                # Open the file and read its content
                with open(file_path, 'r') as file:
                    text = file.read()
                    
                soup = BeautifulSoup(text, 'lxml')
                item7_text = get_section_7_content(soup)
                filtered_item7_text = remove_stopwords(item7_text)
                counter+=1
                
                output1 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : Based on the MD&A section of the ITEM 7, what are the main factors driving the companies revenue? ANSWER_OBTAINED : ",
                })

                output2 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : Based on the MD&A, how does the company perceive its competitive position within the industry? ANSWER_OBTAINED : ",
                })

                output3 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : In the MD&A of the 10-K filing, what market trends or industry factors does the company discuss as impacting its performance? ANSWER_OBTAINED : ",
                })

                output4 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : From the MD&A, extract insights into the trends and drivers behind the company's operating expenses. ANSWER_OBTAINED : ",
                })

                output5 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : According to the MD&A in ITEM 7, what are the major cost components affecting the company's profitability? ANSWER_OBTAINED : ",
                })

                output6 = query({
                    "inputs": str(filtered_item7_text) + ". QUESTION : According to the MD&A in ITEM 7, derive some insights about the companys growth? ANSWER_OBTAINED : ",
                })

                final_text.append(output1[0]["generated_text"].split(". QUESTION : ")[-1])
                final_text.append(output2[0]["generated_text"].split(". QUESTION : ")[-1])
                final_text.append(output3[0]["generated_text"].split(". QUESTION : ")[-1])
                final_text.append(output4[0]["generated_text"].split(". QUESTION : ")[-1])
                final_text.append(output5[0]["generated_text"].split(". QUESTION : ")[-1])
                final_text.append(output6[0]["generated_text"].split(". QUESTION : ")[-1])
                
    

    final_text_str = "".join(final_text)
    final_text_str = final_text_str.replace("ANSWER_OBTAINED","")


    finalOutput1 = query({
        "inputs": str(final_text_str) + ". QUESTION : Based on the MD&A section of the ITEM 7, what are the main factors driving the companies revenue? ANSWER_OBTAINED : ",
    })

    finalOutput2 = query({
        "inputs": str(final_text_str) + ". QUESTION : Based on the MD&A, how does the company perceive its competitive position within the industry? ANSWER_OBTAINED : ",
    })

    finalOutput3 = query({
        "inputs": str(final_text_str) + ". QUESTION : In the MD&A of the 10-K filing, what market trends or industry factors does the company discuss as impacting its performance? ANSWER_OBTAINED : ",
    })

    finalOutput4 = query({
        "inputs": str(final_text_str) + ". QUESTION : From the MD&A, extract insights into the trends and drivers behind the company's operating expenses. ANSWER_OBTAINED : ",
    })

    finalOutput5 = query({
        "inputs": str(final_text_str) + ". QUESTION : According to the MD&A in ITEM 7, what are the major cost components affecting the company's profitability? ANSWER_OBTAINED : ",
    })

    finalOutput6 = query({
        "inputs": str(final_text_str) + ". QUESTION : According to the MD&A in ITEM 7, derive some insights about the companys growth? ANSWER_OBTAINED : ",
    })

    final_output.append(finalOutput1[0]["generated_text"].split(". QUESTION : ")[-1])
    final_output.append(finalOutput2[0]["generated_text"].split(". QUESTION : ")[-1])
    final_output.append(finalOutput3[0]["generated_text"].split(". QUESTION : ")[-1])
    final_output.append(finalOutput4[0]["generated_text"].split(". QUESTION : ")[-1])
    final_output.append(finalOutput5[0]["generated_text"].split(". QUESTION : ")[-1])
    final_output.append(finalOutput6[0]["generated_text"].split(". QUESTION : ")[-1])
   

    for entry in final_output:
        print(entry)
        question, answer = entry.split("ANSWER_OBTAINED : ")
        data[question.strip()] = answer.strip()
        print("----------------------------------------")

    # return final_output
    return render_template('secondPage.html', data=data)






if __name__ == '__main__':
    app.run(debug=True)
