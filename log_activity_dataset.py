import pandas as pd
import os
from datetime import datetime

csv_log = "activity_dataset.csv"

def log_to_csv(event_type, file_path):
    now = datetime.now()
    path_depth = len(file_path.split(os.sep))
    file_ext = os.path.splitext(file_path)[1]

    log_data = {
        "timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
        "event_type": event_type,
        "path_depth": path_depth,
        "extension": file_ext
    }

    df = pd.DataFrame([log_data])

    if not os.path.exists(csv_log):
        df.to_csv(csv_log, index=False)
    else:
        df.to_csv(csv_log, mode='a', header=False, index=False)
