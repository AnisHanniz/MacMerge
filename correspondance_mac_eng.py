import pandas as pd
from tkinter import Tk, filedialog, messagebox
import re

def get_file_path(prompt):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("CSV Files", "*.csv")])
    root.destroy()
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return None
    return file_path

def detect_mac_column(df):
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    for column in df.columns:
        if df[column].dropna().apply(lambda x: bool(mac_regex.match(str(x)))).sum() > 0:
            return column
    return None

def compare_mac_addresses(file1, file2):
    try:
        df1 = pd.read_csv(file1, delimiter=';')
        df2 = pd.read_csv(file2, delimiter=';')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read one of the files: {e}")
        return

    mac_column1 = detect_mac_column(df1)
    mac_column2 = detect_mac_column(df2)

    if mac_column1 is None or mac_column2 is None:
        messagebox.showerror("Error", "Unable to detect the MAC address column in one of the files")
        return

    common_macs = pd.merge(df1, df2, left_on=mac_column1, right_on=mac_column2, how='inner')
    if common_macs.empty:
        messagebox.showinfo("Result", "No matching MAC addresses found")
    else:
        print("Matching MAC addresses found:")
        print(common_macs)

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not save_path:
            messagebox.showerror("Error", "No save location selected")
            return
        common_macs.to_csv(save_path, index=False)
        messagebox.showinfo("Result", f"Matching MAC addresses have been saved to '{save_path}'")

def main():
    file1 = get_file_path("Select the first CSV file")
    if file1 is None:
        return
    
    file2 = get_file_path("Select the second CSV file")
    if file2 is None:
        return

    compare_mac_addresses(file1, file2)

if __name__ == "__main__":
    main()
