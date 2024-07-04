import pandas as pd
from tkinter import Tk, filedialog, messagebox
import re

def get_file_path(prompt):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("Fichiers CSV", "*.csv")])
    root.destroy()
    if not file_path:
        messagebox.showerror("Erreur", "Aucun fichier sélectionné")
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
        messagebox.showerror("Erreur", f"Échec de la lecture d'un des fichiers : {e}")
        return

    mac_column1 = detect_mac_column(df1)
    mac_column2 = detect_mac_column(df2)

    if mac_column1 is None or mac_column2 is None:
        messagebox.showerror("Erreur", "Impossible de détecter la colonne des adresses MAC dans un des fichiers")
        return

    common_macs = pd.merge(df1, df2, left_on=mac_column1, right_on=mac_column2, how='inner')
    if common_macs.empty:
        messagebox.showinfo("Résultat", "Aucune adresse MAC correspondante trouvée")
    else:
        print("Les adresses MAC correspondantes trouvées :")
        print(common_macs)

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        if not save_path:
            messagebox.showerror("Erreur", "Aucun emplacement de sauvegarde sélectionné")
            return
        common_macs.to_csv(save_path, index=False)
        messagebox.showinfo("Résultat", f"Les adresses MAC correspondantes ont été enregistrées dans '{save_path}'")

def main():
    file1 = get_file_path("Sélectionnez le premier fichier CSV")
    if file1 is None:
        return
    
    file2 = get_file_path("Sélectionnez le deuxième fichier CSV")
    if file2 is None:
        return

    compare_mac_addresses(file1, file2)

if __name__ == "__main__":
    main()
