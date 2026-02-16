from log_collector import collect_logs
from log_compressor import compress_logs
from anomaly_detector import detect_anomalies

def main():
    logs = collect_logs()
    compressed = compress_logs(logs)
    alerts, _ = detect_anomalies(compressed)

    print("=== Alerts ===")
    for alert in alerts:
        print(alert)

if __name__ == "__main__":
    main()
