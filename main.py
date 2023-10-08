import json
import tkinter as tk
from tkinter import filedialog, ttk, simpledialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprawdzanie plików JSON")

        self.pliki = []

        self.przycisk_wybierz = ttk.Button(root, text="Wybierz pliki JSON", command=self.wybierz_pliki)
        self.przycisk_wybierz.pack(pady=20)

        self.lista = ttk.Treeview(root, columns=("Plik", "Wynik", "Akcja"), show="headings")
        self.lista.heading("Plik", text="Plik")
        self.lista.heading("Wynik", text="Wynik")
        self.lista.heading("Akcja", text="Akcja")
        self.lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.lista.bind("<Button-1>", self.on_item_click)

        self.przycisk_sprawdz = ttk.Button(root, text="Sprawdź wszystkie", command=self.sprawdz_wszystkie)
        self.przycisk_sprawdz.pack(pady=20)

        self.przycisk_usun_wszystkie = ttk.Button(root, text="Usuń wszystkie", command=self.usun_wszystkie)
        self.przycisk_usun_wszystkie.pack(pady=20)

        self.przycisk_o_autorze = ttk.Button(root, text="O autorze", command=self.o_autorze)
        self.przycisk_o_autorze.pack(pady=20)


    def wybierz_pliki(self):
        pliki = filedialog.askopenfilenames(filetypes=[("Pliki JSON", "*.json")])

        for plik in pliki:
            if plik not in [p['nazwa'] for p in self.pliki]:
                self.pliki.append({
                    'nazwa': plik,
                    'wynik': '',
                    'item_id': None
                })
                item_id = self.lista.insert("", tk.END, values=(plik, '', ''))
                for p in self.pliki:
                    if p['nazwa'] == plik:
                        p['item_id'] = item_id

    def sprawdz_wszystkie(self):
        for plik in self.pliki:
            with open(plik['nazwa'], 'r', encoding="utf-8") as f:
                try:
                    json.load(f)
                    plik['wynik'] = "OK"
                except json.JSONDecodeError as e:
                    plik['wynik'] = str(e)

            if plik['wynik'] == "OK":
                self.lista.item(plik['item_id'], values=(plik['nazwa'], "OK", ''))
            else:
                self.lista.item(plik['item_id'], values=(plik['nazwa'], "❌", 'Szczegóły błędu'))

    def on_item_click(self, event):
        item = self.lista.identify_row(event.y)
        column = self.lista.identify_column(event.x)

        if item and column == "#3" and self.lista.item(item, "values")[2] == "Szczegóły błędu":
            plik = next((p for p in self.pliki if p['item_id'] == item), None)
            if plik and plik['wynik'] != "OK":
                self.pokaz_szczegoly(plik['wynik'])

    def pokaz_szczegoly(self, blad):
        simpledialog.messagebox.showinfo("Szczegóły błędu", blad)

    def usun_wszystkie(self):
        # Czyszczenie listy plików i widgetu Treeview
        self.pliki.clear()
        for item in self.lista.get_children():
            self.lista.delete(item)

    def o_autorze(self):
        simpledialog.messagebox.showinfo("O autorze", "Program został stworzony przez Jakuba Sperskiego.\n"
                                                       "Prawa autorskie zastrzeżone.\n"
                                                       "Rozpowszechnianie programu dozwolone jest jedynie przez autora lub osobę wyznaczoną przez autora.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()