import pandas as pd
import numpy as np
import string

print("Creating >10MB physical excel file...")
# We need around 15MB of compressed data. 
# 1 million rows of random alphanumeric strings usually compresses to ~20MB
num_customers = 5000
transactions = 200

# Random strings to defeat compression
def random_strings(n, length=20):
    return [''.join(np.random.choice(list(string.ascii_letters + string.digits), length)) for _ in range(n)]

customer_codes = [f"CUST_{i:05d}" for i in range(num_customers)]

# We will just repeat dates
dates = pd.date_range('2023-01-01', periods=transactions, freq='D')

# create dataframe quickly
df = pd.DataFrame({
    'CustomerCode': np.repeat(customer_codes, transactions),
    'Invoice/Receipt Date': np.tile(dates, num_customers),
    'InvoiceType': np.where(np.random.rand(num_customers * transactions) > 0.5, 'Invoice', 'Payment'),
    'Outstanding Amount': np.random.uniform(-5000, 5000, num_customers * transactions),
    'RandomDataToMakeItBigger': random_strings(num_customers * transactions, 30)
})

print("Saving to large_test.xlsx...")
df.to_excel('large_test.xlsx', index=False)

import os
file_mb = os.path.getsize('large_test.xlsx') / (1024 * 1024)
print(f"Created large_test.xlsx. Physical File Size: {file_mb:.2f} MB")
