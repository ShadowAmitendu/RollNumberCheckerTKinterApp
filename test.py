import os
import re
import customtkinter as ctk
from tkinter import messagebox, filedialog


class RollNumberCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Not Submitted Roll Numbers")

        # Configure the appearance of App Window
        ctk.set_appearance_mode("auto")
        ctk.set_default_color_theme("green")

        # Fonts
        self.input_font = ctk.CTkFont(family="Supreme", size=14)
        self.result_font = ctk.CTkFont(family="JetBrains Mono", size=14)

        # Start Roll
        self.start_label = ctk.CTkLabel(master, text="Start Roll (Last 3 Digits):", font=self.input_font)
        self.start_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_entry = ctk.CTkEntry(master, font=self.input_font)
        self.start_entry.grid(row=0, column=1, padx=10, pady=5)
        self.start_entry.insert(0, "001")

        # End Roll
        self.end_label = ctk.CTkLabel(master, text="End Roll (Last 3 Digits):", font=self.input_font)
        self.end_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_entry = ctk.CTkEntry(master, font=self.input_font)
        self.end_entry.grid(row=1, column=1, padx=10, pady=5)
        self.end_entry.insert(0, "140")

        # Roll position dropdown
        self.position_label = ctk.CTkLabel(master, text="Roll Number Position:", font=self.input_font)
        self.position_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.position_option = ctk.CTkOptionMenu(master, values=["Start", "Middle", "End"], font=self.input_font)
        self.position_option.grid(row=2, column=1, padx=10, pady=5)
        self.position_option.set("Middle")

        # Ignore field
        self.ignore_label = ctk.CTkLabel(master, text="Ignore Rolls (comma-separated):", font=self.input_font)
        self.ignore_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.ignore_entry = ctk.CTkEntry(master, font=self.input_font)
        self.ignore_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        self.browse_button = ctk.CTkButton(master, text="Browse Folder", command=self.browse_folder,
                                           font=self.input_font)
        self.browse_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.submit_button = ctk.CTkButton(master, text="Check", command=self.check_missing_rolls,
                                           font=self.input_font)
        self.submit_button.grid(row=5, column=0, padx=10, pady=5)

        self.copy_button = ctk.CTkButton(master, text="Copy Results", command=self.copy_results,
                                         font=self.input_font)
        self.copy_button.grid(row=5, column=1, padx=10, pady=5)

        # Result box
        self.result_box = ctk.CTkTextbox(master, width=480, height=240, font=self.result_font, state="normal")
        self.result_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.result_box.insert("1.0", "Results will be shown here...\n")
        self.result_box.configure(state="disabled")

        self.folder_path = ""

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select the folder containing the PDF files")
        if self.folder_path:
            self.browse_button.configure(fg_color="green")
        else:
            self.browse_button.configure(fg_color="red")

    def extract_roll_number(self, filename, position):
        matches = re.findall(r"\d{11}", filename)
        if not matches:
            return None
        if position == "Start":
            return matches[0] if filename.startswith(matches[0]) else None
        elif position == "End":
            name_without_ext = filename.replace(".pdf", "")
            return matches[-1] if name_without_ext.endswith(matches[-1]) else None
        elif position == "Middle":
            underscore_match = re.search(r"_(\d{11})_", filename)
            if underscore_match:
                return underscore_match.group(1)
            return matches[0]
        return None

    def check_missing_rolls(self):
        base_roll_number = "152427230"

        start_roll_suffix = self.start_entry.get().strip()
        end_roll_suffix = self.end_entry.get().strip()
        position = self.position_option.get()

        if not (start_roll_suffix.isdigit() and end_roll_suffix.isdigit()):
            messagebox.showerror("Error", "Please enter valid last three digits.")
            return

        start_roll = int(start_roll_suffix)
        end_roll = int(end_roll_suffix)

        found_rolls = [0] * (end_roll - start_roll + 1)
        found_list = []
        missing_list = []

        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".pdf"):
                roll_number_str = self.extract_roll_number(filename, position)
                if not roll_number_str:
                    continue
                try:
                    roll_number = int(roll_number_str)
                    roll_suffix = roll_number % 1000
                    if start_roll <= roll_suffix <= end_roll:
                        if found_rolls[roll_suffix - start_roll] == 0:
                            found_list.append(f"{roll_suffix:03}")
                        found_rolls[roll_suffix - start_roll] = 1
                except ValueError:
                    continue

        for i in range(len(found_rolls)):
            if found_rolls[i] == 0:
                missing_list.append(f"{start_roll + i:03}")

        # Apply ignore filter
        ignore_input = self.ignore_entry.get().strip()
        if ignore_input:
            ignore_set = {num.strip().zfill(3) for num in ignore_input.split(",") if num.strip().isdigit()}
            found_list = [num for num in found_list if num not in ignore_set]
            missing_list = [num for num in missing_list if num not in ignore_set]
        else:
            ignore_set = set()

        total_found = len(found_list)
        total_missing = len(missing_list)

        # Build result text
        result_text = ""
        result_text += "Found Roll Numbers:\n"
        result_text += ", \t".join(sorted(found_list)) if found_list else "None"
        result_text += "\n\n"

        result_text += "Not Submitted Roll Numbers:\n"
        result_text += ", \t".join(sorted(missing_list)) if missing_list else "None"
        result_text += "\n\n"

        result_text += f"Total Found: {total_found} | Total Missing: {total_missing}"
        if ignore_set:
            result_text += f"\nIgnored: {', '.join(sorted(ignore_set))}"

        # Show in result box
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", ctk.END)
        self.result_box.insert("1.0", result_text)
        self.result_box.configure(state="disabled")

        # Save results
        save_file_path = os.path.join(self.folder_path, "roll_number_results.txt")
        with open(save_file_path, "w") as f:
            f.write(result_text)

        messagebox.showinfo("Info", f"Results saved to {save_file_path}")

    def copy_results(self):
        """Copy results to clipboard."""
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_box.get("1.0", ctk.END).strip())
        self.master.update()
        messagebox.showinfo("Copied", "Results copied to clipboard!")


if __name__ == "__main__":
    root = ctk.CTk()

    # Window size
    window_width = 500
    window_height = 490
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)

    app = RollNumberCheckerApp(root)
    root.mainloop()
