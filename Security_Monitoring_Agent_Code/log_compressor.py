def compress_logs(df):
    # Downsample by aggregating every 5 rows to reduce data volume and processing cost
    return df.groupby(df.index // 5).mean()
