from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df)
    preds = model.predict(df)

    alerts = []
    for i, p in enumerate(preds):
        if p == -1:
            # Include the data values for context
            alerts.append(f"Anomaly detected at compressed index {i}: {df.iloc[i].to_dict()}")
    return alerts, preds
