import pandas as pd

def process_data(input_file, output_file):
    """
    Reads the raw YouTube stats CSV, processes it to compute metrics,
    and saves the result as a Parquet file.
    """
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    # Type casting and date conversion
    df['pull_date'] = pd.to_datetime(df['pull_date'])
    
    # Convert numeric columns to numeric, coercing errors if any (though we will drop NaNs)
    # The user request specifically asked to "type cast the columns correctly and drop rows with missing values"
    # We will drop NaNs first to ensure casting to int works cleanly
    cols_to_check = ['viewCount', 'likeCount', 'commentCount']
    df = df.dropna(subset=cols_to_check).copy()
    
    for col in cols_to_check:
        df[col] = df[col].astype(int)
        
    # Sort data for diff calculation
    df = df.sort_values(['id', 'pull_date'])
    
    print("Computing metrics...")
    # Group by video ID and compute diffs
    # We use shift(1) to get the previous value within each group
    # but the diff() method is more direct for numeric columns.
    # For datetime, diff() works too immediately.
    
    grouped = df.groupby('id')
    
    df['time_since_last_pull'] = grouped['pull_date'].diff()
    df['view_diff'] = grouped['viewCount'].diff()
    df['like_diff'] = grouped['likeCount'].diff()
    df['comment_diff'] = grouped['commentCount'].diff()
    
    print(f"Saving to {output_file}...")
    df.to_parquet(output_file)
    print("Done!")

if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(base_dir, 'mrbeast_dataset', 'MrBeast_youtube_stats.csv')
    output_parquet = os.path.join(base_dir, 'mrbeast_dataset', 'MrBeast_youtube_stats_processed.parquet')
    process_data(input_csv, output_parquet)
