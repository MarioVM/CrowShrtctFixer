# Broken Shortcut Fixer

This Python script is designed to fix broken shortcuts in a Windows environment. It searches for the target files in all drives except the C drive and updates the shortcuts with the new locations of the target files. It also logs the changes to a `changes.log` file in the root directory of the application.

## 📋 Requirements

- Python 3
- `pylnk3` library

## 🛠️ Installation

1. Install Python 3 if you haven't already. You can download it from the [official website](https://www.python.org/downloads/).
2. Install the `pylnk3` library using pip:

```shell
pip install pylnk3

🚀 Usage
Run the script in your terminal:

The script will start the process of fixing broken shortcuts. It will search for the target files in all drives except the C drive and update the shortcuts with the new locations of the target files. The changes will be logged to a changes.log file in the root directory of the application.

📄 License
This project is licensed under the terms of the GNU General Public License v3.0. See the LICENSE file for details.

```