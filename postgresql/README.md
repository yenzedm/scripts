# 🚀 Running or Packaging `add_user_and_access_to_db.py` on Different OS

This guide covers how to run or package a Python script using a virtual environment, both with and without creating a binary, for **Ubuntu 24.04**, **Windows 10**, and **Astra Linux 1.7**.

---

## 🐧 Ubuntu 24.04

### 🔧 Run Without Binary

```bash
sudo apt-get update -y && \
sudo apt-get install -y python3-pip python3.10-venv && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install docker psycopg2-binary && \
sudo venv/bin/python3 add_user_and_access_to_db.py && \
deactivate && \
rm -rf venv
```

### 🛠️ Create Executable with PyInstaller

```bash
sudo apt-get update -y && \
sudo apt-get install -y python3-pip python3.10-venv && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install docker psycopg2-binary pyinstaller && \
sudo venv/bin/python3 add_user_and_access_to_db.py && \
pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db.py && \
deactivate && \
rm -rf venv
```

---

## 🪟 Windows 10

### 🔧 Run Without Binary

```cmd
python -m venv venv && ^
.\venv\Scripts\activate && ^
pip install docker psycopg2-binary && ^
python add_user_and_access_to_db.py && ^
deactivate && ^
rd /s /q venv
```

### 🛠️ Create Executable with PyInstaller

```cmd
python -m venv venv && ^
.\venv\Scripts\activate && ^
pip install docker psycopg2-binary pyinstaller && ^
pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db.py && ^
deactivate && ^
rd /s /q venv
```

---

## 🛡️ Astra Linux 1.7

### 🛠️ Create Executable with PyInstaller

```bash
sudo apt-get update -y && \
sudo apt-get install -y python3-pip python3-venv python3-dev python-dev && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install docker psycopg2-binary==2.8.3 pyinstaller==3.6 && \
pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db.py && \
deactivate && \
rm -rf venv
```

