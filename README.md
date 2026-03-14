# 🛡️ Ransomware Detection System (ML Based)

A **Machine Learning based ransomware detection system** that monitors file system activity in real time and detects suspicious behaviour that may indicate a ransomware attack.

The system uses **Python, Watchdog, and a trained ML model** to analyze file activity patterns and alert the user when suspicious activity is detected.

---

# 🚀 Features

• Real-time folder monitoring
• Machine learning based ransomware detection
• GUI interface using Tkinter
• Activity logging system
• Suspicious behaviour alert notifications
• Dataset logging for training
• File activity analysis

---

# 🧠 How It Works

1. The system monitors a selected folder using the **Watchdog library**.
2. Every file activity (create, modify, delete, rename) is recorded.
3. The activity is converted into features.
4. A **trained Machine Learning model** predicts whether the behaviour is suspicious.
5. If suspicious activity exceeds a threshold, the system alerts the user.

---

# 🛠 Tech Stack

Programming Language

* Python

Libraries Used

* Tkinter
* Watchdog
* Joblib
* Plyer
* Scikit-learn
* Pandas
* Numpy

Machine Learning

* Classification Model
* Feature Encoding
* Activity Dataset Training

---

# 📂 Project Structure

```
monitor_folder/
│
├── ransomware_detector.py
├── train_model.py
├── log_activity_dataset.py
│
├── ransomware_model.pkl
├── label_encoder_event.pkl
├── label_encoder_ext.pkl
│
├── activity_dataset.csv
├── activity_log.txt
│
└── test files
```

---

# ⚙️ Installation

Clone the repository

```
git clone https://github.com/yourusername/ransomware-detection-system.git
```

Move into project folder

```
cd ransomware-detection-system
```

Install required libraries

```
pip install watchdog scikit-learn pandas numpy plyer joblib
```

---

# ▶️ Run the Program

Run the main detection system

```
python ransomware_detector.py
```

The GUI window will open and start monitoring the configured folder.

---

# 🧪 Train the Model (Optional)

To retrain the machine learning model:

```
python train_model.py
```

This will generate a new trained model file.

---

# 🔔 Detection Alert

If suspicious behaviour is detected:

• GUI warning message appears
• System notification is triggered
• Activity is logged into log file

---

# 📊 Dataset Logging

The system records file activity events into a dataset that can later be used to improve the ML model.

---

# 🔮 Future Improvements

• Deep learning based detection
• Cloud based monitoring system
• Automatic ransomware blocking
• Web dashboard monitoring
• Multi-folder monitoring

---

# 👨‍💻 Author

Krish Vajar
Computer Engineering Student

GitHub
https://github.com/vajar-krish

---

# ⭐ Support

If you find this project useful please give it a **star ⭐ on GitHub**.
