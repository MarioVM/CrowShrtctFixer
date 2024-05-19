# Broken Shortcut Fixer

This Python script is designed to fix broken shortcuts in a Windows environment. It searches for the target files in all drives except the specified excluded drives and updates the shortcuts with the new locations of the target files. It also logs the changes to a `changes.log` file in the root directory of the application.

## 📋 Requirements

- Python 3
- `pylnk3` library

## 🛠️ Installation

1. Install Python 3 if you haven't already. You can download it from the [official website](https://www.python.org/downloads/).
2. Install the `pylnk3` library using pip:

    ```shell
    pip install pylnk3
    ```

## 🚀 Usage

Run the script in your terminal:

```shell
python shrtctfixer.py

The script will prompt you to enter the drives you want to exclude from the search (e.g., C,D). After that, it will start the process of fixing broken shortcuts. It will search for the target files in all drives except the excluded ones and update the shortcuts with the new locations of the target files. The changes will be logged to a changes.log file in the root directory of the application.

📝 Example
Enter the drives to exclude, separated by commas (e.g., 'C,D'): C,D
Scanning for shortcuts...
Found 5 shortcuts.
Checking and fixing shortcuts...
Changed C:\Users\User\Desktop\Example.lnk from E:\OldPath\Example.exe to F:\NewPath\Example.exe
...
Process completed. Check changes.log for details.

This `README.md` provides clear instructions on requirements, installation, usage, and an example of how to run the script, as well as licensing information.

📄 License
This project is licensed under the terms of the GNU General Public License v3.0. See the LICENSE file for details

