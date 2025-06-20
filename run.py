import requests

url = "https://raw.githubusercontent.com/adityasatam/bank_statement_summary/refs/heads/main/main.py?token=GHSAT0AAAAAADEQJLXYAXX4DA5ZH264TCD42BTLJNQ"
response = requests.get(url)

if response.status_code == 200:
    exec(response.text)
    #print(response.text)
    #main(bank_name='icici', file_path=r"C:/Users/sasuk/", file_name="OpTransactionHistoryTpr02-04-2025 (1).xls", year=2025, month=1, amount_greater_than=5000)
    #main(bank_name='hdfc', file_path=r"C:/Users/sasuk/", file_name="Acct_Statement_XX7897_20062025.xls", year=2025, month=1, amount_greater_than=5000)
else:
    print("Failed to execute the github code")
