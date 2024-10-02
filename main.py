import os
import customtkinter as ctk
from tkinter import messagebox, filedialog


class RollNumberCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Not Submitted Roll Numbers")

        # Configure the appearance of App Window
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Create a custom font for inputs
        self.input_font = ctk.CTkFont(family="Archivo", size=14)
        self.result_font = ctk.CTkFont(family="JetBrains Mono", size=14)

        # Create input fields and buttons
        self.start_label = ctk.CTkLabel(master, text="Start Roll (Last 3 Digits):", font=self.input_font)
        self.start_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.start_entry = ctk.CTkEntry(master, font=self.input_font)
        self.start_entry.grid(row=0, column=1, padx=10, pady=10)
        self.start_entry.insert(0, "001")  # Default value for start roll

        self.end_label = ctk.CTkLabel(master, text="End Roll (Last 3 Digits):", font=self.input_font)
        self.end_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.end_entry = ctk.CTkEntry(master, font=self.input_font)
        self.end_entry.grid(row=1, column=1, padx=10, pady=10)
        self.end_entry.insert(0, "140")  # Default value for end roll

        # Center the buttons by adjusting their grid layout
        self.browse_button = ctk.CTkButton(master, text="Browse Folder", command=self.browse_folder,
                                           font=self.input_font)
        self.browse_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.submit_button = ctk.CTkButton(master, text="Submit", command=self.check_missing_rolls,
                                           font=self.input_font)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Create a larger result box for displaying results with a custom font
        self.result_box = ctk.CTkTextbox(master, width=480, height=182, font=self.result_font, state="normal")
        self.result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Initialize result box with default text
        self.result_box.insert("1.0", "Not Submitted Roll Numbers:\n")
        self.result_box.configure(state="disabled")  # Disable input

        self.folder_path = ""

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select the folder containing the PDF files")
        if self.folder_path:
            self.browse_button.configure(fg_color="green")
        else:
            self.browse_button.configure(fg_color="red")

    def check_missing_rolls(self):
        base_roll_number = "152427230"

        start_roll_suffix = self.start_entry.get().strip()
        end_roll_suffix = self.end_entry.get().strip()

        if not (start_roll_suffix.isdigit() and end_roll_suffix.isdigit()):
            messagebox.showerror("Error", "Please enter valid last three digits.")
            self.browse_button.configure(fg_color="red")
            return

        try:
            start_roll = int(start_roll_suffix)
            end_roll = int(end_roll_suffix)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid roll numbers.")
            self.browse_button.configure(fg_color="red")
            return

        found_rolls = [0] * (end_roll - start_roll + 1)
        missing_rolls = []

        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            self.browse_button.configure(fg_color="red")
            return

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".pdf"):
                try:
                    roll_number_str = filename[:11]
                    roll_number = int(roll_number_str)
                    roll_suffix = roll_number % 1000

                    if start_roll <= roll_suffix <= end_roll:
                        found_rolls[roll_suffix - start_roll] = 1
                except ValueError:
                    continue

        for i in range(len(found_rolls)):
            if found_rolls[i] == 0:
                missing_rolls.append(start_roll + i)

        if missing_rolls:
            formatted_missing_rolls = [f"{num:03}" for num in missing_rolls]
            result_text = "Not Submitted Roll Numbers:\n" + ", \t".join(formatted_missing_rolls)
        else:
            result_text = "Not Submitted Roll Numbers:\nNone"

        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", ctk.END)
        self.result_box.insert("1.0", result_text)
        self.result_box.configure(state="disabled")

        save_file_path = os.path.join(self.folder_path, "missing_roll_numbers.txt")
        with open(save_file_path, "w") as f:
            f.write(result_text)

        messagebox.showinfo("Info", f"Missing roll numbers saved to {save_file_path}")


if __name__ == "__main__":
    root = ctk.CTk()

    # Set the window size to 500x400
    window_width = 500
    window_height = 400

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window geometry and position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)  # Disable resizing the window

    app = RollNumberCheckerApp(root)
    root.mainloop()
