from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()




data = {"Statement_Consolidated_finanacial_results_for_all_months": {
"Quarter ended 31 December 2024": {
    "Revenue from operations": 16175.71,
    "Other income": 1301.15,
    "Total income": 17476.86,
    "Cost of construction and development": 6272.52,
    "Changes in inventories of work-in-progress and finished properties": 1275.2,
    "Employee benefit expense": 2743.89,
    "Finance costs": 874.35,
    "Depreciation and amortisation expenses": 312.6,
    "Other expenses": 3596.12,
    "Total expenses": 12524.2,
    "Profit/loss before tax and share of profit/loss of joint ventures": 4952.66,
    "Share of profit/loss of joint ventures, net": 11.2,
    "Profit/loss before tax": 4941.42,
    "Current tax": 277.46,
    "Deferred tax": 411.9,
    "Profit/loss for the period/year": 4252.06,
    "Other comprehensive income/loss": 473.84,
    "Total comprehensive income/loss for the period/year, net of tax": 4725.9
},
}}

def get_llm_response(text,OPENAI_API_KEY):
    model = ChatOpenAI(model='gpt-4o',api_key=OPENAI_API_KEY)
    prompt1 = f"""
    it has the STANDALONE, CONSOLIDATED, Balance Sheet, and Cash Flow tables data . sometime this statement comes combine please extract properly.
    extract the table from this input text and extracted table should follow this kind of structure 
    give the proper heading to the table so we can understand for which statement it belongs to

    | Particulars                                  | 31-DEC-2024     | 30-SEPT-2024    | 31-DEC-2023     | 31-DEC-2024 (Nine Months) | 31-DEC-2023 (Nine Months) | 31-MAR-2024 (Year Ended) |
    |----------------------------------------------|-----------------|-----------------|-----------------|----------------------------|----------------------------|----------------------------|
    | **Income From Operations**                   |                 |                 |                 |                            |                            |                            |
    | a) Income from Operations                    | 4,463.99        | 4,403.25        | 5,727.44        | 13,948.72                   | 12,647.87                   | 21,260.03                   |
    | b) Other Income                              | 2.47            | 60.90           | 2.11            | 78.03                        | 11.45                        | 511.70                       |
    | **Total Income from Operations**             | 4,466.46        | 4,464.15        | 5,729.55        | 13,578.75                   | 12,659.32                   | 22,271.73                   |
    |                                              |                 |                 |                 |                            |                            |                            |
    | **Expenses**                                 |                 |                 |                 |                            |                            |                            |
    | a) Cost of materials consumed                | 2,100.58        | 2,810.09        | 2,526.36        | 7,266.44                     | 7,365.89                     | 9,992.20                     |
    | b) Purchase of stock-in-trade                | 214.15          | 330.05          | 1,563.06        | 964.71                       | 2,864.59                     | 3,477.84                     |
    | c) Changes in inventories of Finished Goods, WIP | 264.52          | (559.34)        | (282.32)        | (968.95)                     | 73.71                        | 223.20                       |
    | d) Employees benefit expense                 | 263.88          | 254.74          | 523.44          | 839.72                       | 1,809.40                     | 2,062.63                     |
    | e) Finance Costs                             | 63.32           | 108.00          | 179.21          | 307.21                       | 544.22                       | 742.90                       |
    | f) Depreciation and amortisation expense     | 79.55           | 61.51           | 101.38          | 242.47                       | 341.25                       | 457.63                       |
    | g) Job Charges                               | 878.17          | 932.55          | 654.38          | 2,612.83                     | 1,904.65                     | 2,767.18                     |
    | h) Other expenses                            | 465.31          | 497.15          | 615.53          | 1,524.57                     | 1,901.79                     | 2,705.27                     |
    | **Total Expenses**                           | 4,432.47        | 4,434.74        | 5,882.84        | 13,388.55                   | 16,805.48  

    keep continous adding remaining details after that here do not miss any data
    input is 
    :{text}
    """

    extracted_table  =model.invoke(prompt1).content

    prompt2 = f"""convert given table in json structure do it for all dates data for your understanding this is one example {data}\n
            it has the finacial statement for STANDALONE, CONSOLIDATED, Balance Sheet, and Cash Flow
            1.do not miss any data and give the proper formated json structures
            do not give any unnecessary text give the pure json i do not need any other explaination

            Ensure that data is:\n"
            All values are positive.\n"
            Genereate ouput for each datewise "
            if you see the mutiple table  because may be the page break"
            better understanding check given example"
            If a statement is not present, mark it as '<statement_name>_are_not_present'.\n"
            Use precise key names  instead of variations.\n"
            Do not include markdown formatting, newlines, or unnecessary characters.\n"
            Follow the data types (float for numeric values, string for text).\n"
            Ignore extra text that does not belong to the financial statements.\n"
            ensure the give all date detail data"

            Extract standalone and consolidated financial statements accurately.
            Convert the extracted data into structured JSON format.
            handle most scenarios and variations in financial statement formats.
            
            input table is :{extracted_table}
            """
    json_result  =model.invoke(prompt2).content
    
    try:
        result1 = eval(json_result)
        return result1
    except:
        result2 = json_result
        return result2

