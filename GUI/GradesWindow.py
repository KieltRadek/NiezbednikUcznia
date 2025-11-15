import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Grade import Grade
from Services.grade_exporter import grade_exporter
from Services.grade_importer import grade_importer


class GradesWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Moduł ocen")
        self.root.geometry("600x400")
        self.root.configure(bg="white")

        self.selected_ids = set()
        self._build_ui()
        self._load_grades()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="white")
        header.pack(fill=tk.X, pady=5)

        tk.Button(header, text="+ Dodaj ocenę",
                  bg="PeachPuff3", relief=tk.FLAT,
                  command=self._add_grade).pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(header, text="Usuń zaznaczone",
                                    bg="salmon", relief=tk.FLAT,
                                    state=tk.DISABLED,
                                    command=self._delete_selected)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(header, text="+ Importuj oceny",
                  bg="lightblue", relief=tk.FLAT,
                  command=self.import_grades).pack(side=tk.LEFT, padx=5)

        tk.Button(header, text="↯ Eksportuj oceny",
                  bg="lightgreen", relief=tk.FLAT,
                  command=self.export_grades).pack(side=tk.LEFT, padx=5)

        cols = ("date", "subject", "grade", "comment")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", selectmode="extended")
        headings = [
            ("date",    "Data",      80),
            ("subject", "Przedmiot", 200),
            ("grade",   "Ocena",     80),
            ("comment", "Komentarz", 200),
        ]
        for col, txt, w in headings:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="w" if col in ("subject","comment") else "center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_grades(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        self.selected_ids.clear()
        self.delete_btn.config(state=tk.DISABLED)

        session = Session()
        try:
            recs = session.query(Grade) \
                          .filter(Grade.user_id == self.user_id) \
                          .order_by(Grade.date.desc()) \
                          .all()
        finally:
            session.close()

        for gr in recs:
            self.tree.insert("", tk.END, iid=str(gr.id), values=(
                gr.date.strftime("%Y-%m-%d"),
                gr.subject,
                f"{gr.grade_value:.1f}",
                gr.comment
            ))

    def _on_select(self, _):
        self.selected_ids = set(map(int, self.tree.selection()))
        self.delete_btn.config(state=tk.NORMAL if self.selected_ids else tk.DISABLED)

    def _add_grade(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Dodaj ocenę")
        dlg.geometry("400x240")
        dlg.configure(bg="white")

        labels = ["Data (YYYY-MM-DD)", "Przedmiot", "Ocena", "Komentarz"]
        entries = {}
        for i, text in enumerate(labels):
            tk.Label(dlg, text=text, bg="white") \
              .grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ent = tk.Entry(dlg)
            ent.grid(row=i, column=1, sticky="we", padx=10, pady=5)
            entries[text] = ent
        dlg.grid_columnconfigure(1, weight=1)

        def save():
            try:
                dt  = datetime.strptime(entries[labels[0]].get(), "%Y-%m-%d").date()
                sub = entries[labels[1]].get().strip()
                if not sub:
                    raise ValueError("Przedmiot nie może być pusty")
                val = float(entries[labels[2]].get().replace(",", "."))
                com = entries[labels[3]].get().strip()

                session = Session()
                gr = Grade(
                    user_id=self.user_id,
                    date=dt,
                    subject=sub,
                    grade_value=val,
                    comment=com
                )
                session.add(gr)
                session.commit()
                session.close()

                dlg.destroy()
                self._load_grades()
            except Exception as e:
                messagebox.showerror("Błąd", str(e), parent=dlg)

        tk.Button(dlg, text="Zapisz", bg="PeachPuff3", relief=tk.FLAT,
                  command=save) \
          .grid(row=len(labels), column=0, columnspan=2, pady=10)
        entries[labels[0]].focus_set()

    def _delete_selected(self):
        if not messagebox.askyesno("Usuń", f"Czy usunąć {len(self.selected_ids)} ocen?"):
            return
        session = Session()
        try:
            session.query(Grade) \
                   .filter(Grade.id.in_(self.selected_ids)) \
                   .delete(synchronize_session=False)
            session.commit()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Błąd", str(e))
        finally:
            session.close()
        self._load_grades()

    def export_grades(self):
        session = Session()
        try:
            recs = session.query(Grade) \
                          .filter(Grade.user_id == self.user_id) \
                          .order_by(Grade.date) \
                          .all()
        finally:
            session.close()

        if not recs:
            messagebox.showinfo("Eksport", "Brak ocen do eksportu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV","*.csv"), ("Wszystkie pliki","*.*")]
        )
        if not path:
            return

        try:
            grade_exporter.export_to_csv(recs, path)
            messagebox.showinfo("Eksport ocen", f"Zapisano {len(recs)} ocen do:\n{path}")
        except Exception as e:
            messagebox.showerror("Błąd eksportu", str(e))

    def import_grades(self):
        path = filedialog.askopenfilename(
            title="Wybierz plik CSV z ocenami",
            filetypes=[("CSV","*.csv"), ("Wszystkie pliki","*.*")]
        )
        if not path:
            return

        clear = messagebox.askyesno(
            "Import ocen",
            "Usunąć istniejące oceny przed importem?"
        )
        try:
            count = grade_importer.import_from_csv(path, self.user_id, clear_existing=clear)
            messagebox.showinfo("Import ocen", f"Zaimportowano {count} ocen.")
            self._load_grades()
        except Exception as e:
            messagebox.showerror("Błąd importu", str(e))

    def run(self):
        self.root.mainloop()
