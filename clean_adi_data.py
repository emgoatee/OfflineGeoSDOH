import pandas as pd
import sys
import os

def clean_adi_file(input_path, output_path="data/adi.csv"):
    print(f"Reading raw file: {input_path}")
    print("Ensuring FIPS codes are read as Text to prevent corruption...")
    
    # Read CSV, ensuring all columns are read as strings initially to protect "0" prefixes
    try:
        df = pd.read_csv(input_path, dtype=str)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Columns found: {list(df.columns)}")
    
    # Normalizing column names (strip whitespace, upper case)
    df.columns = [c.strip() for c in df.columns]
    
    # Check for likely FIPS column name (usually 'FIPS' or 'GISJOIN')
    fips_col = None
    if 'FIPS' in df.columns:
        fips_col = 'FIPS'
    elif 'GISJOIN' in df.columns:
        # Sometimes raw data has GISJOIN (G+FIPS). If so, we'd need to parse. 
        # But assuming standard Neighborhood Atlas structure which usually has FIPS.
        fips_col = 'GISJOIN' 
    
    if not fips_col:
        print("ERROR: Could not find a 'FIPS' column.")
        print("Available columns:", df.columns)
        return

    # Check for ADI rank columns
    required_cols = ['ADI_NATRANK', 'ADI_STATERNK']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        return

    # Select only needed columns
    print("Filtering columns...")
    final_df = df[[fips_col, 'ADI_NATRANK', 'ADI_STATERNK']].copy()
    
    if fips_col != 'FIPS':
        final_df.rename(columns={fips_col: 'FIPS'}, inplace=True)

    # Clean FIPS: Remove 'G' if present (GISJOIN format) and ensure 12 chars
    final_df['FIPS'] = final_df['FIPS'].astype(str).str.replace('G', '', regex=False)
    
    # Remove rows with invalid FIPS (e.g. empty)
    final_df = final_df[final_df['FIPS'].str.len() >= 11]

    print(f"Saving cleaned data to {output_path}...")
    final_df.to_csv(output_path, index=False)
    print("Success! Your file is ready.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_adi_data.py <path_to_fresh_downloaded_file.csv>")
    else:
        clean_adi_file(sys.argv[1])
