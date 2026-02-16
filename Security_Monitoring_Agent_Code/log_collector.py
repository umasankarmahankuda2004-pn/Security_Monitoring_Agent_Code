import pandas as pd
import numpy as np

def collect_logs():
    """
    Simulates the collection of system logs (CPU, Memory, Network).
    Returns a pandas DataFrame with synthetic data and injected anomalies.
    """
    np.random.seed(42)
    n_rows = 200
    
    data = {
        'cpu': np.random.normal(loc=30, scale=5, size=n_rows),
        'memory': np.random.normal(loc=50, scale=10, size=n_rows),
        'network': np.random.exponential(scale=5, size=n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Inject synthetic anomalies (spikes)
    anomaly_indices = [20, 50, 85, 120, 180]
    for idx in anomaly_indices:
        df.loc[idx, 'cpu'] = np.random.uniform(80, 100)
        df.loc[idx, 'network'] = np.random.uniform(50, 100)
        
    return df