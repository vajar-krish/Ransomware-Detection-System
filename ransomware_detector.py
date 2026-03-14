import tkinter as tk
from tkinter import messagebox, scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
from plyer import notification
from log_activity_dataset import log_to_csv
import joblib
import time
import threading
import os
import logging

# === Configuration ===
path_to_watch = r"C:\Users\Bhavil\OneDrive\Desktop\monitor_folder"  
log_file = "activity_log.txt"

# Logging setup
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Thresholds
suspicious_threshold = 30
time_window = 30
event_times = []

# === File Event Handler ===
class RansomwareEventHandler(FileSystemEventHandler):
    def __init__(self, gui_ref):
        self.gui = gui_ref
        self.model = joblib.load("ransomware_model.pkl")
        self.le_event = joblib.load("label_encoder_event.pkl")
        self.le_ext = joblib.load("label_encoder_ext.pkl")

    def on_any_event(self, event):
        if not event.is_directory:
            event_time = datetime.now()
            event_times.append(event_time)

            event_type = event.event_type.upper()
            file_path = event.src_path
            log_line = f"[{event_type}] {file_path}"

          
            logging.info(log_line)

         
            timestamp = event_time.strftime('%Y-%m-%d %H:%M:%S')
            self.gui.update_log(f"{timestamp} - {log_line}")

          
            try:
                log_to_csv(event.event_type, event.src_path)
            except Exception as e:
                self.gui.update_log(f"[ML Logging Error] {e}")

            
            self.check_suspicious_activity()
            if self.check_with_ml(event.event_type, event.src_path):
                ml_msg = "⚠️ ML Model Detected Anomaly!"
                self.gui.show_alert(ml_msg)
                logging.warning("🚨 ML-Based Ransomware Detection 🚨")

                notification.notify(
                    title="⚠️ ML-Based Ransomware Alert!",
                    message="Anomaly detected by machine learning model.",
                    timeout=10
                )

    def check_suspicious_activity(self):
        global event_times
        now = datetime.now()
        event_times[:] = [t for t in event_times if now - t < timedelta(seconds=time_window)]
        if len(event_times) > suspicious_threshold:
            alert_msg = f"⚠️ ALERT: {len(event_times)} rapid file changes detected!"
            self.gui.show_alert(alert_msg)

            logging.warning("🚨 Threshold-Based Ransomware Detection 🚨")
            notification.notify(
                title="⚠️ Ransomware Alert!",
                message="Suspicious file modification behavior detected.",
                timeout=10
            )
            event_times.clear()

    def check_with_ml(self, event_type, file_path):
        try:
            timestamp = datetime.now()
            event_encoded = self.le_event.transform([event_type])[0]
            ext_encoded = self.le_ext.transform([os.path.splitext(file_path)[1]])[0]
            depth = len(file_path.split(os.sep))
            hour = timestamp.hour

            X_new = [[event_encoded, depth, ext_encoded, hour]]
            result = self.model.predict(X_new)
            return result[0] == -1  # -1 means anomaly
        except Exception as e:
            self.gui.update_log(f"[ML Prediction Error] {e}")
            return False

# === GUI Class ===
class RansomwareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡 Ransomware Detection Dashboard")
        self.root.geometry("750x520")
        self.observer = None

        # Title
        tk.Label(root, text="📂 Monitoring Folder Activity", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Log Display
        self.log_area = scrolledtext.ScrolledText(root, height=22, width=90, state="disabled", bg="#f8f8f8")
        self.log_area.pack(padx=10, pady=10)

        # Buttons
        self.start_btn = tk.Button(root, text="▶ Start Monitoring", command=self.start_monitoring, bg="green", fg="white", width=20)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="⏹ Stop Monitoring", command=self.stop_monitoring, state="disabled", bg="red", fg="white", width=20)
        self.stop_btn.pack(pady=5)

    def update_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.see(tk.END)

    def show_alert(self, alert_msg):
        messagebox.showwarning("🚨 Ransomware Alert", alert_msg)
        self.update_log(alert_msg)

    def start_monitoring(self):
        if self.observer is None:
            self.update_log(f"👁️ Started monitoring folder:\n{path_to_watch}")
            event_handler = RansomwareEventHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, path=path_to_watch, recursive=True)
            self.observer.start()

            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")

            threading.Thread(target=self.monitor_runtime_limit).start()

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer = None
            self.update_log("⏹️ Monitoring stopped.")
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

    def monitor_runtime_limit(self):
        max_runtime = 120  # seconds
        start_time = time.time()
        while self.observer:
            if time.time() - start_time > max_runtime:
                self.stop_monitoring()
                break
            time.sleep(1)

# === Run the App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = RansomwareGUI(root)
    root.mainloop()
