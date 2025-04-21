import requests

url = "https://raw.githubusercontent.com/adityasatam/bank_statement_summary/refs/heads/main/main.py?token=GHSAT0AAAAAADCSNWSLS42Y52W27JQN4FWW2AGRGGA"
response = requests.get(url)

if response.status_code == 200:
    exec(response.text)
    #print(response.text)
    #main(file_path=r"C:/Users/sasuk/", file_name="OpTransactionHistoryTpr02-04-2025 (1).xls", year=2025, month=1, amount_greater_than=5000)
else:
    print("Failed to execute the github code")
