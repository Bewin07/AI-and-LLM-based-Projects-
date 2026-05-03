import pandas as pd
from logic import process_settlement
import time
import numpy as np

print("Generating test dataframe...")
dates = pd.date_range('2024-01-01', periods=100, freq='D')
customers = [f"CUST{int(i):03d}" for i in range(500)]
df = pd.DataFrame({
    'CustomerCode': np.repeat(customers, 100),
    'Invoice/Receipt Date': np.tile(dates, 500),
    'InvoiceType': ['Invoice']*25000 + ['Payment']*25000,
    'Outstanding Amount': np.random.uniform(-1000, 1000, 50000)
})

print("Testing process_settlement with use_parallel=False ...")
start = time.time()
res_seq = process_settlement(df.copy(), use_parallel=False)
time_seq = time.time()-start
print(f"Sequential executed cleanly in {time_seq:.2f}s")

print("Testing process_settlement with use_parallel=True ...")
start = time.time()
try:
    res_parallel = process_settlement(df.copy(), use_parallel=True)
    time_par = time.time()-start
    print(f"Parallel executed cleanly in {time_par:.2f}s")
    if time_par > time_seq:
        print(f"WARNING: Parallel is SLOWER by {time_par - time_seq:.2f}s")
    else:
        print(f"SUCCESS: Parallel is FASTER by {time_seq - time_par:.2f}s")
except Exception as e:
    print(f"FAILED: {str(e)}")
