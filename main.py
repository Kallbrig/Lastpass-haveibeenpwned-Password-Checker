"""
This is the file script that handles recieving the passwords sending the email.
It's the brains of the operation.

"""




from pwned import *
import pandas as pd
import lastpass
from send_email import *

df_cracked = pd.DataFrame(columns=['name', 'username', 'password', ])

vault = lastpass.Vault.open_remote(lastpass_api['username'], lastpass_api['password'])

# runs through entries in Lastpass Account
for i in vault.accounts:

    account_url = str(i.url)[2:-1]
    account_user_name = str(i.username)[2:-1]
    account_pw = str(i.password)[2:-1]
    account_name = str(i.name)[2:-1]

    # Checks haveibeenpwned to see if the current password has been cracked
    num_times_cracked = lookup_pwned_api(account_pw)[1]

    # Print's a message about cracked passwords
    # print(f'Your password from {account_name} has been cracked {num_times_cracked} times. You should change it.\n'
    #       f'url  --- {account_url}\n')

    # adds cracked passwords to a dataframe
    if num_times_cracked != 0:
        cracked_entry = {'name': account_name, 'username': account_user_name, 'password': account_pw, }
        df_cracked = df_cracked.append(cracked_entry, ignore_index=True)

# print(df_cracked)
# If the dataframe is not empty, it sends a email with the cracked accounts.
if not df_cracked.empty:
    formatted_email = format_email(df_cracked.to_html())
    send_email(formatted_email)

    # Saves cracked passwords to a csv file
    # df_cracked.to_csv('pw_cracked.csv', index_label='index')
