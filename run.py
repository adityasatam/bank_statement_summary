import requests
import numpy as np

# 1) keep your bank statement in xls format in local folder.
# 2) copy this run.py in your local VS Code.
# 4) modify only line 13 with bank statement file name, file path and other parameters.
# 5) execute run.py in your local VS Code.

url = "https://raw.githubusercontent.com/adityasatam/bank_statement_summary/refs/heads/main/main.py"
response = requests.get(url)

if response.status_code == 200:
    exec(response.text)
    #print(response.text)
    main(bank_name='icici', file_path=r"C:/Users/sasuk/", file_name="OpTransactionHistoryTpr02-04-2025 (1)", year=2025, month=[1,2,3,4], amount_greater_than=1000, remark_match='VIN/')
    #main(bank_name='hdfc', file_path=r"C:/Users/sasuk/", file_name="Acct_Statement_XX7897_20062025", year=2025, month=[4,5,6], amount_greater_than=1000, remark_match='POS ')
else:
    print("Failed to execute the github code")
