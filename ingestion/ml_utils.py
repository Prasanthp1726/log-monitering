import pandas as pd
from sklearn.ensemble import IsolationForest
from .models import LogEntry

def detect_anomalies(queryset=None):
    if queryset is None:
        queryset = LogEntry.objects.all()
    logs = queryset.values("id", "timestamp", "service", "log_level", "message")
    df = pd.DataFrame(list(logs))

    if df.empty:
        return []

    # timestamp → numeric
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp_num"] = df["timestamp"].astype(int) / 10**9

    # encode categorical
    df["service_code"] = df["service"].astype("category").cat.codes
    df["level_code"] = df["log_level"].astype("category").cat.codes
    df["msg_code"] = df["message"].astype("category").cat.codes

    features = df[["timestamp_num", "service_code", "level_code", "msg_code"]]

    # Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]
    # Return list of anomalous IDs
    return [int(row['id']) for _, row in anomalies.iterrows()]
