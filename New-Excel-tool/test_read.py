import pandas as pd
import time
import os

start = time.time()
print(f"Reading large_test.xlsx (Size: {os.path.getsize('large_test.xlsx')/(1024*1024):.2f} MB) using calamine...")
df = pd.read_excel("large_test.xlsx", engine="calamine")
print(f"Read {len(df)} rows in {time.time()-start:.2f} seconds")
