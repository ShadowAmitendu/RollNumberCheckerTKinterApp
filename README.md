# Roll Number Checker App

This Python-based desktop application helps identify missing roll numbers from a list of PDFs stored in a specific folder. The app allows you to input a range of roll numbers (based on the last three digits) and automatically checks which roll numbers have not been submitted.
## Features

- Input range of roll numbers (last 3 digits).
- Automatically detects roll numbers from PDF files in the selected folder.
- Displays missing roll numbers in the app.
- Saves missing and submitted roll numbers to text files.
- User-friendly interface using CustomTkinter.
- Provides error messages when input is invalid or if the folder is not selected.
- Default roll number range is 1-140.
- Leading zeroes are added to roll numbers for proper formatting (e.g., 001, 002).
- The app's icon can be customized by adding an `.ico` file.

## Requirements

- Python 3.7 or higher
- The following Python libraries:
  - `customtkinter`
  - `tkinter`

You can install the necessary dependencies by running:

```bash
pip install customtkinter
```
## Installation

1. **Clone or Download the Project:**

   You can clone the repository using the following command:

   ```bash
   git clone https://github.com/ShadowAmitendu/RollNumberCheckerTKinterApp.git
   ```

   Or download the project from the release page.

2. **Run the Application:**

   After cloning/downloading the project, you can run the application using Python:

   ```bash
   python missingRollNumbers.py
   ```

## Usage

1. **Input Roll Number Range:**

   - Enter the starting and ending roll numbers (last 3 digits).
   - If no input is given, the default range will be used (1 to 140).

2. **Browse Folder:**

   - Click the "Browse Folder" button to select the folder containing the PDF files. The folder must contain files named in the format `152427230XX_Subject_StudentName.pdf` (where XX is the roll number).

3. **Submit:**

   - After selecting the folder, click the "Submit" button. The missing roll numbers will be displayed in the app.
   - The missing roll numbers will be saved to a file named `missing_roll_numbers.txt` in the selected folder.
   - Submitted roll numbers will also be saved to a file named `submitted_roll_numbers.txt`.

## Icon Customization

To change the application icon, replace the `icon.ico` file in the project folder with your desired `.ico` file. The icon will be used in the app window and the executable.

## Building the Executable

To distribute the app as an executable, you can use `PyInstaller`. After installing PyInstaller (`pip install pyinstaller`), you can build the executable with the following command:

```bash
pyinstaller --onefile --windowed --icon=icon.ico missingRollNumbers.py
```

This will create a standalone executable file in the `dist` folder that can be distributed without requiring Python to be installed.

## License

This project is open-source, distributed under the MIT License. Feel free to use, modify, and distribute the application.

## Author

**Amitendu Bikash Dhusiya**
