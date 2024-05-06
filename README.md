## Project Overview

* This project utilizes Python programming language along with Flask framework to create a web application for downloading financial data, cleaning it, and generating insights. 
* The application has been tested with "TSLA", "AAPL", and "AMZN" tickers.

    
## Downloading data-  
* The sec-edgar-downloader library is used to fetch the SEC 10-K filings of the respective companies.

## Generating insights-  
* Insights are generated from Item 7 and Item 7A sections of the SEC 10-K filings.
* The HuggingFaceH4/zephyr-7b-beta inference API is utilized for this purpose.

## Questions asked-  
1. Based on the MD&A section of the ITEM 7, what are the main factors driving the companies revenue?
2. Based on the MD&A, how does the company perceive its competitive position within the industry?
3. In the MD&A of the 10-K filing, what market trends or industry factors does the company discuss as impacting its performance?
4. From the MD&A, extract insights into the trends and drivers behind the company's operating expenses.
5. According to the MD&A in ITEM 7, what are the major cost components affecting the company's profitability?
6. According to the MD&A in ITEM 7, derive some insights about the companys growth?

## Why users care about these insights?-  
1. Main factors driving the company's revenue: Users would care about this insight because it provides valuable information on what aspects of the company's operations contribute most significantly to its top line.
   Understanding the revenue drivers helps investors and stakeholders gauge the company's growth prospects, identify potential risks or opportunities, and make informed decisions regarding investment or partnership.
2. Perception of competitive position within the industry: Users are interested in this insight as it offers crucial context on how the company views its position relative to competitors.
   It gives investors and stakeholders a sense of the company's strategic positioning, its strengths and weaknesses compared to peers, and its ability to withstand competitive pressures or capitalize on market opportunities.
3. Discussion of market trends or industry factors impacting performance: This insight is important for users to understand the external forces shaping the company's performance. By knowing how the company perceives
   market trends and industry dynamics, users can assess the company's adaptability, its responsiveness to changing conditions, and its ability to navigate challenges or capitalize on emerging opportunities.
4. Insights into trends and drivers behind operating expenses: Users care about this insight because it reveals how the company manages its costs and resources. Understanding the trends and drivers behind operating
   expenses helps users evaluate the company's efficiency, cost control measures, and potential areas for improvement. It also provides insights into the sustainability of the company's profitability over the long term.
5. Major cost components affecting profitability: Users are interested in this insight because it highlights the key cost factors impacting the company's bottom line. By identifying the major cost components,
   users can assess the company's cost structure, its ability to manage expenses, and the potential impact on profitability. This information is essential for making investment decisions and evaluating the company's financial health.
6. Insights about the company's growth: Users care about this insight as it provides a snapshot of the company's trajectory and potential future performance. Understanding the factors driving growth, whether it's through
   expansion into new markets, product innovation, or strategic partnerships, helps users assess the company's competitive position, scalability, and overall business outlook. It informs investment decisions and provides context
   for evaluating the company's long-term prospects.

## Limitations and future scope-  
1. The project focuses on generating insights from Item 7 and Item 7A of the SEC 10-K filing, but can be expanded to other sections such as Risk Factors, Financial Statements, etc.
2. Future enhancements can include deeper analysis and more comprehensive insights generation.
3. Some insights generated are not very accurate. The accuracy of the insights can be further improved.

## Demo-  
The demo of the web app can be seen [here](https://drive.google.com/file/d/1SKPTSU4iYnFExyuyU4vHkBH0AFE-9jF2/view?usp=sharing).
