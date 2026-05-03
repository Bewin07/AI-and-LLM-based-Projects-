import pandas as pd
import numpy as np
from streamlit.testing.v1 import AppTest
import os

print("Creating 12MB file...")
num_customers = 1500
transactions_per_customer = 100
total_rows = num_customers * transactions_per_customer
customer_codes = [f"CUST_{i:05d}" for i in range(num_customers)]
dates = pd.date_range('2023-01-01', periods=transactions_per_customer, freq='D')
data = []
for cust in customer_codes:
    for i, date in enumerate(dates):
        amount = 1000 if i % 2 == 0 else -1000
        data.append({
            'CustomerCode': cust,
            'Invoice/Receipt Date': date,
            'InvoiceType': 'Invoice' if amount > 0 else 'Payment',
            'Outstanding Amount': amount
        })

df = pd.DataFrame(data)
# Save as bytes so we don't have to write to disk, AppTest accepts bytes!
# Or we can write to disk, but bytes is easier. Let's just write to disk.
df.to_excel('large_test.xlsx', index=False)
file_mb = os.path.getsize('large_test.xlsx') / (1024 * 1024)
print(f"Created large_test.xlsx. File Size: {file_mb:.2f} MB")
print(f"Dataframe Memory Size: {df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB")

print("Running AppTest...")
at = AppTest.from_file("app.py")
at.run()
# Set file value
at.file_uploader[0].set_value('large_test.xlsx').run(timeout=100)
print("AppTest completed.")

if at.error:
    print("\n--- ERRORS FOUND ---")
    for e in at.error:
        print(e.value)
else:
    print("\n--- RESULTS ---")
    print("Success! No errors.")
    # Check if we see the balloons or info message about large file processing
    for info in at.info:
        print("INFO:", info.value)
