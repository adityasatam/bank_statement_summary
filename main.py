# input: bank xls format bank statement
# set the required values: bank_name, file_path, file_name, year, month, amount_greater_than
# output: Monthly Summary of Withdrawals, Deposits and Significant Withdrawals/Deposits, Quaterly Summary of Withdrawals
# 02-04-2025 Aditya Satam: Monthly Summary of Withdrawals, Deposits and Significant Withdrawals/Deposits
# 20-04-2025 Aditya Satam: Quaterly Summary of Withdrawals
# 03-04-2025 Aditya Satam: Quaterly Summary of Debit Card Withdrawals (Lounge Access)
# 20-06-2025 Aditya Satam: included hdfc bank with icici bank
# 21-06-2025 Aditya Satam: included multiple months, remark_match, day in report "Monthly Summary of Significant Withdrawals/Deposits"
# 28-06-2025 Aditya Satam: added save% and spend/invest% monthly report

import pandas as pd

pd.set_option('display.max_rows', None)        # 1. Show all rows
pd.set_option('display.max_columns', None)     # 2. Show all columns
pd.set_option('display.max_colwidth', None)    # 3. Don't truncate long column values
pd.set_option('display.expand_frame_repr', False)  # 4. Prevent wrapping to multiple lines

# Data reading, cleaning and EDA
def data_cleaning_EDA(file_path, file_name, bank_name):
    # read xls file into python dataframe
    df = pd.read_excel(file_path+file_name+".xls", engine="xlrd")

    if bank_name=='hdfc':
        # rename xls columns
        df.columns = ["Date", "Remark", "ChequeNo", "TransationDate", 
                    "Withdrawal", "Deposit", "Balance"]
        
        # filter top description till Balance column has data
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
        first_idx = None
        last_idx = None
        for idx, val in df['Balance'].items():
            if pd.notna(val):
                if first_idx is None:
                    first_idx = idx  # first numeric
            else:
                if first_idx is not None:
                    last_idx = idx  # first non-numeric after numeric started
                    break
        fdf = df.loc[first_idx:last_idx-1].copy()

        # create new month, year columns using Transation date column
        fdf['TransationDate'] = pd.to_datetime(fdf['TransationDate'], format='%d/%m/%y')

        remark_keyword = 'POS '
    else:
        # rename xls columns
        df.columns = ["DummyColumn", "SNo", "ValueDate", "TransationDate", 
                    "ChequeNo", "Remark", "Withdrawal", "Deposit", "Balance"]

        # filter top description till Balance column has data
        first_valid_row = df['Balance'].first_valid_index()
        fdf = df.loc[first_valid_row+1:] # +1 to filter out Balalnce (INR) header
        fdf =fdf[fdf['Balance'].notna()] # filter out Nan records

        # create new month, year columns using Transation date column
        fdf['TransationDate'] = pd.to_datetime(fdf['TransationDate'], format='%d/%m/%Y')

        remark_keyword = 'VIN/'

    fdf['Year'] = fdf['TransationDate'].dt.year.astype(int) # Extract Year
    fdf['Month'] = fdf['TransationDate'].dt.month.astype(int) # Extract Month (Numeric)
    fdf['Day'] = fdf['TransationDate'].dt.day.astype(int) # Extract Day (Numeric)
    fdf['MonthName'] = fdf['TransationDate'].dt.strftime('%b')  # Extract Full Month Name
    return fdf, remark_keyword

# Monthly Summary of Withdrawals and Deposits
def summary_dr_cr(fdf):
    # month number, name mapping
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7:
                      'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    Current_Balance = fdf['Balance'].iloc[-1]
    df_dr_cr = fdf.groupby(['Month',
                                                'Year'])[['Withdrawal',
                                                          'Deposit']].sum().sort_values(by=['Year',
                                                                                            'Month'], 
                                                                                            ascending=False).reset_index()
    
    # Adding Savings, Balance MonthEnd
    df_dr_cr['Savings'] = df_dr_cr['Deposit'] - df_dr_cr['Withdrawal']
    df_dr_cr['Balance_MonthEnd'] = Current_Balance - df_dr_cr['Savings'].cumsum().shift(fill_value=0)
    df_dr_cr['Month'] = df_dr_cr['Month'].map(month_dict)

    safe_deposit = np.where(df_dr_cr['Deposit'] == 0, np.nan, df_dr_cr['Deposit'])
    df_dr_cr['Save%'] = (pd.to_numeric(df_dr_cr['Savings']/safe_deposit)*100).round(1).fillna(0)
    df_dr_cr['Spend/Invest%'] = (pd.to_numeric(df_dr_cr['Withdrawal']/safe_deposit)*100).round(1).fillna(0)
    return df_dr_cr

# Print Monthly Summary of Withdrawals and Deposits
def print_summary_dr_cr(df_dr_cr):
    print("\n>>>>>> Monthly Summary of Withdrawals and Deposits\n")
    print(df_dr_cr)

# Monthly Summary of Significant Withdrawals/Deposits
def summary_dr_cr_indiv(fdf, year, month, amount_greater_than, remark_match):
    df_dr = fdf[(fdf['Withdrawal'].astype(float) > amount_greater_than) & 
                            (fdf['Remark'].astype(str).str.contains(remark_match, case=True, na=False)) &
                            (fdf['Month'].isin(month)) & 
                            (fdf['Year'] == year)][['Day', 'MonthName', 'Remark',
                                                            'Withdrawal']].rename(columns={'Withdrawal': 'Amount'})
    df_dr['Type'] = 'Withdrawal'
    df_cr = fdf[(fdf['Deposit'].astype(float) > amount_greater_than) &
                            (fdf['Remark'].astype(str).str.contains(remark_match, case=False, na=False)) &
                            (fdf['Month'].isin(month)) & 
                            (fdf['Year'] == year)][['Day' ,'MonthName', 'Remark',
                                                            'Deposit']].rename(columns={'Deposit': 'Amount'})
    df_cr['Type'] = 'Deposit'
    df_union = pd.concat([df_dr, df_cr], ignore_index=True)
    print("\n>>>>>> Monthly Summary of Significant Withdrawals/Deposits\n")
    print(df_union)

# Quaterly Summary of Withdrawals
def summary_dr_qtr(df_dr_cr, message):
    df_qtr = pd.DataFrame(columns=['Year', 'Quarter', 'Period', 'Actual_Period', 'Withdrawal'])
    qtr_dict = {"Q1": ["Jan", "Feb", "Mar"], "Q2": ["Apr", "May", "Jun"], 
                    "Q3": ["Jul", "Aug", "Sep"], "Q4": ["Oct", "Nov", "Dec"]}
    unique_year_list = df_dr_cr['Year'].unique().tolist()
    for y in unique_year_list:
        for key, value in qtr_dict.items():
            wt_sum = 0
            mon_list = []
            for mon in value:
                df_dr_spent = df_dr_cr[(df_dr_cr['Month'] == mon) &
                                                    (df_dr_cr['Year'] == y)]['Withdrawal'].sum()
                if df_dr_spent:
                    wt_sum += df_dr_spent
                    mon_list.append(mon)
            if mon_list:
                new_row = {'Year': y, 'Quarter': key, 'Period': qtr_dict[key], 'Actual_Period': mon_list, 'Withdrawal': wt_sum}
                if not df_qtr.empty:
                    df_qtr = pd.concat([df_qtr, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    df_qtr = pd.DataFrame([new_row])
    print(f"\n>>>>>> {message}\n")
    print(df_qtr)

def main(bank_name='hdfc', file_path=r"C:/Users/sasuk/", file_name="Acct_Statement_XX7897_20062025", year=2025, month=[4,5,6], amount_greater_than=1000, remark_match=''):
    df, remark_keyword = data_cleaning_EDA(file_path, file_name, bank_name)
    summary_dr_cr_indiv(df, year, month, amount_greater_than, remark_match)

    res_df = summary_dr_cr(df)
    print_summary_dr_cr(res_df)

    summary_dr_qtr(res_df, "Quarterly Summary of Withdrawals Spent")
    
    filtered_df = df[df['Remark'].astype(str).str.contains(fr'{remark_keyword}', na=False)]
    new_res_df = summary_dr_cr(filtered_df)
    summary_dr_qtr(new_res_df, "Quarterly Debit Card Spend for Lounge Access")


# # set file path and name
# file_path=r"C:/Users/sasuk/"
# file_name="OpTransactionHistoryTpr02-04-2025 (1)"

# # set the filter for 2nd report on Top Withdrawal and Deposit
# year=2024
# month=11
# amount_greater_than=5000
# main()
