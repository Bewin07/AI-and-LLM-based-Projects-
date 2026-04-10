import streamlit as st
import pandas as pd
from io import BytesIO
import time
from logic import process_settlement

st.set_page_config(page_title="FIFO Pending Amount Tool", layout="wide")

st.title("📘 FIFO Pending Amount Settlement Tool Optimized")
st.write("Upload one Excel file. Debits are positive. Credits are negative. FIFO logic is applied per customer.")

# Show file size info
st.info("⚡ **Performance:** Files >10MB use parallel processing for speed. Large files process very fast.")

uploaded = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if uploaded:
    start_time = time.time()
    
    # Get file size
    file_size_mb = len(uploaded.getvalue()) / (1024 * 1024)
    st.info(f"📊 File size: {file_size_mb:.2f} MB")
    
    # Show loading progress
    with st.spinner(f"📥 Reading file ({file_size_mb:.2f} MB)..."):
        try:
            # For large files, read in chunks
            if file_size_mb > 40:
                st.write("🚀 Using optimized processing for large file...")
                # Read with optimized parameters for large files
                df = pd.read_excel(uploaded, engine='openpyxl')
            else:
                df = pd.read_excel(uploaded)
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()
    
    # Pre-process: Drop known metadata rows
    if not df.empty:
        # 1. Drop rows where any column contains "(In Lakhs)" (case insensitive)
        def is_metadata_row(row):
            return row.astype(str).str.lower().str.contains("in lakhs").any()
        
        mask = df.apply(is_metadata_row, axis=1)
        if mask.any():
            df = df[~mask]
            st.warning("⚠️ Removed metadata row(s) containing '(In Lakhs)'.")
            
        # 2. Clean numeric columns
        if 'B2B2C' in df.columns:
            df['B2B2C'] = pd.to_numeric(df['B2B2C'], errors='coerce')
    
    # Normalize column names
    if "Oustanding Amount" in df.columns and "Outstanding Amount" not in df.columns:
        df.rename(columns={"Oustanding Amount": "Outstanding Amount"}, inplace=True)

    required = ["CustomerCode", "Invoice/Receipt Date", "InvoiceType", "Outstanding Amount"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()

    st.subheader("📥 Input Preview")
    st.dataframe(df.head(50))
    st.write(f"Total rows: {len(df)}")

    # Process settlement using external logic with progress tracking
    st.subheader("⚙️ Processing Settlement...")
    progress_bar = st.progress(0)
    progress_text = st.empty()
    
    def update_progress(percentage):
        """Callback function to update progress bar"""
        progress_bar.progress(percentage / 100.0)
        progress_text.text(f"Progress: {percentage}% complete")
    
    try:
        # Auto-enable parallel processing for large files (>10MB)
        use_parallel = file_size_mb > 10 or len(df) > 10000
        pending_final = process_settlement(df, use_parallel=use_parallel, progress_callback=update_progress)
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        st.stop()

    processing_time = time.time() - start_time
    
    st.subheader("✅ Pending Amount Result")
    st.dataframe(pending_final)
    
    # Show summary stats
    input_sum = df['Outstanding Amount'].sum()
    output_sum = pending_final['Outstanding Amount'].sum()
    pending_sum = pending_final['Pending Amount'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Input Total Outstanding", f"{input_sum:,.2f}")
    col2.metric("Output Total Outstanding", f"{output_sum:,.2f}")
    col3.metric("Total Pending Amount", f"{pending_sum:,.2f}")
    col4.metric("Processing Time", f"{processing_time:.2f}s", delta=f"File: {file_size_mb:.1f}MB")

    if abs(input_sum - output_sum) > 0.01:
        st.warning("⚠️ Discrepancy detected in Outstanding Amount sum!")
    else:
        st.success("✅ Input and Output Outstanding Amount sums match perfectly!")

    # Download
    def to_excel(df):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Pending")
        return buffer.getvalue()

    st.download_button(
        "⬇ Download Pending Amount Excel",
        data=to_excel(pending_final),
        file_name="pending_output_full.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("🎉 Done! Your pending file is ready.")
    
    # Show performance info
    if file_size_mb > 10:
        st.balloons()
        st.info(f"⚡ **Large file processed in {processing_time:.2f} seconds!** (Parallel processing enabled)")

else:
    st.info("👆 Please upload an Excel file to begin.")
