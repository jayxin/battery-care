# Battery Care

A battery monitor and battery level notifier.

## Design

- Use `psutil` to access battery information.
- Use `plyer` to send messages to system.
- Use `tkinter` for GUI.
- Use `threading` for rendering GUI and monitor battery.

## Usage Overview

1. Run this app.
2. Set battery level thresholds and monitor interval. When the battery is lower
   or higher than the thresholds, this app will send message to the system.

## Running

1. **Download the code** in this repo.
2. **Install Python 3**.
3. **Open your terminal in the code directory** and run commands.
4. **Create virtual environment**.
```sh
python -m venv venv
```
5. **Activate virtual environment.**
```sh
# for windows user
venv\Scripts\activate

# for linux bash user
source venv/bin/activate
```
6. **Install dependencies.**
```sh
pip install -r requirements.txt
```
7. **Run this app.**
```sh
python main.py
```
8. **Set your preferred parameters.**
9. **Start monitoring.**
