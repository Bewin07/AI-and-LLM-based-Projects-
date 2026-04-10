import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
from functools import partial

def _process_customer_group(args):
    """
    Process a single customer group using FIFO logic.
    Optimized for parallel processing.
    """
    cust, g = args
    
    # Separate debits & credits using vectorized operations
    is_debit = g["Amount"] >= 0
    debits = g[is_debit].copy()
    credits = g[~is_debit].copy()
    
    # Add pending and settled columns
    debits["Pending Amount"] = debits["Amount"].astype(float)
    debits["SettledFlag"] = False
    
    credits["Pending Amount"] = credits["Amount"].astype(float)
    credits["SettledFlag"] = False
    
    if len(debits) == 0 or len(credits) == 0:
        result = pd.concat([debits, credits], ignore_index=False) if len(debits) + len(credits) > 0 else pd.DataFrame()
        return result
    
    # 1. Apply Credits to Debits using cumulative sum
    credit_pool = float(-credits["Amount"].sum())
    debit_amounts = debits["Amount"].values
    
    # Vectorized approach: check which debits are fully settled
    for idx, debit_idx in enumerate(debits.index):
        if credit_pool <= 0:
            break
        
        debit_amt = debit_amounts[idx]
        
        if debit_amt <= credit_pool:
            credit_pool -= debit_amt
            debits.at[debit_idx, "Pending Amount"] = 0.0
            debits.at[debit_idx, "SettledFlag"] = True
        else:
            debits.at[debit_idx, "Pending Amount"] = debit_amt - credit_pool
            credit_pool = 0
    
    # 2. Apply Debits to Credits using cumulative sum
    debit_pool = float(debits["Amount"].sum())
    credit_amounts = -credits["Amount"].values
    
    for idx, credit_idx in enumerate(credits.index):
        if debit_pool <= 0:
            break
        
        credit_amt = credit_amounts[idx]
        
        if debit_pool >= credit_amt:
            credits.at[credit_idx, "Pending Amount"] = 0.0
            credits.at[credit_idx, "SettledFlag"] = True
            debit_pool -= credit_amt
        else:
            credits.at[credit_idx, "Pending Amount"] = credits.at[credit_idx, "Pending Amount"] + debit_pool
            debit_pool = 0
    
    # Combine results
    result = pd.concat([debits, credits], ignore_index=False)
    return result

def process_settlement(df, num_workers=None, use_parallel=True):
    """
    Applies FIFO settlement logic to the dataframe with parallel processing support.
    Optimized for large files (40MB+).
    
    Parameters:
    - df: Input dataframe
    - num_workers: Number of parallel processes (default: CPU count)
    - use_parallel: Whether to use parallel processing (auto-enabled for large files)
    
    Returns: dataframe with 'Pending Amount' column
    """
    # Clean data
    df = df.copy()
    df["Invoice/Receipt Date"] = pd.to_datetime(df["Invoice/Receipt Date"], dayfirst=True, errors="coerce")
    
    # Handle column name normalization
    if "Oustanding Amount" in df.columns and "Outstanding Amount" not in df.columns:
        df.rename(columns={"Oustanding Amount": "Outstanding Amount"}, inplace=True)
    
    # Optimize memory: use category dtype for CustomerCode
    df["CustomerCode"] = df["CustomerCode"].fillna("Unassigned").astype(str)
    
    # Create Amount column for processing
    df["Amount"] = df["Outstanding Amount"].fillna(0.0).astype(np.float32)
    
    # Sort for FIFO (critical for correctness)
    df = df.sort_values(["CustomerCode", "Invoice/Receipt Date"], ignore_index=True)
    
    # Determine if parallel processing should be used
    num_customers = df["CustomerCode"].nunique()
    file_size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    # Use parallel processing if: large file OR many customer groups
    if use_parallel and (file_size_mb > 40 or num_customers > 100):
        num_workers = num_workers or max(2, cpu_count() - 1)
        
        # Create customer groups
        grouped_data = list(df.groupby("CustomerCode", sort=False))
        
        # Process in parallel
        with Pool(num_workers) as pool:
            results = pool.map(_process_customer_group, grouped_data)
        
        if results:
            pending_final = pd.concat(results, ignore_index=True)
        else:
            pending_final = pd.DataFrame(columns=df.columns)
    else:
        # Sequential processing for small files
        output_list = []
        for cust, grp in df.groupby("CustomerCode", sort=False):
            result = _process_customer_group((cust, grp))
            if not result.empty:
                output_list.append(result)
        
        if output_list:
            pending_final = pd.concat(output_list, ignore_index=True)
        else:
            pending_final = pd.DataFrame(columns=df.columns)
    
    # Restore sort order
    pending_final = pending_final.sort_values(
        ["CustomerCode", "Invoice/Receipt Date"], 
        ignore_index=True
    )
    
    # Remove helper column and convert Amount back to original precision
    pending_final = pending_final.drop(columns=["Amount"])
    pending_final["Outstanding Amount"] = pending_final["Outstanding Amount"].astype(float)
    pending_final["Pending Amount"] = pending_final["Pending Amount"].astype(float)
    
    return pending_final
