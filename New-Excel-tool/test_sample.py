import pandas as pd
from logic import process_settlement

# Test with sample data
test_data = pd.DataFrame({
    'CustomerCode': ['CUST001', 'CUST001', 'CUST001', 'CUST002', 'CUST002'],
    'Invoice/Receipt Date': ['2024-01-01', '2024-01-15', '2024-02-01', '2024-01-10', '2024-02-10'],
    'InvoiceType': ['Invoice', 'Invoice', 'Payment', 'Invoice', 'Payment'],
    'Outstanding Amount': [1000, 500, -800, 2000, -1500]
})

print("Input Data:")
print(test_data)
print("\n" + "="*60 + "\n")

result = process_settlement(test_data)

print("Output Data:")
print(result)
print("\n" + "="*60 + "\n")

print("Summary:")
print(f"Total rows processed: {len(result)}")
print(f"Total input outstanding: {test_data['Outstanding Amount'].sum():.2f}")
print(f"Total output outstanding: {result['Outstanding Amount'].sum():.2f}")
print(f"Total pending amount: {result['Pending Amount'].sum():.2f}")
print(f"Fully settled records: {result['SettledFlag'].sum()}")
print(f"Partially/Not settled records: {(~result['SettledFlag']).sum()}")
