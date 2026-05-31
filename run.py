import sys
import subprocess
import tempfile
import requests

requirements_url = "https://raw.githubusercontent.com/adityasatam/bank_statement_summary/refs/heads/main/requirements.txt"

try:
    response = requests.get(requirements_url, timeout=30)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False
    ) as f:
        f.write(response.text)
        temp_requirements = f.name

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        temp_requirements
    ])

except Exception as e:
    print(f"Failed to install requirements: {e}")
    sys.exit(1)

# 1) keep your bank statement in xls format in local folder.
# 2) copy this run.py in your local VS Code.
# 4) modify only line 13 with bank statement file name, file path and other parameters.
# 5) execute run.py in your local VS Code.

import requests
import numpy as np

url = "https://raw.githubusercontent.com/adityasatam/bank_statement_summary/refs/heads/main/main.py"
response = requests.get(url)

if response.status_code == 200:
    exec(response.text)
    main(
        bank_name='icici',
        file_path=r"C:/Users/sasuk/",
        file_name="OpTransactionHistory30-12-2025",
        year=2025,
        month=[10,11],
        amount_greater_than=1000,
        remark_match='VIN/',
        from_date='23/12/2025',
        to_date='26/12/2025'
    )
else:
    print("Failed to execute the github code")
