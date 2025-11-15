import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
from datetime import datetime, timedelta
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Schedule import Schedule
from Services.schedule_exporter import ScheduleExporter
from Services.schedule_importer import ScheduleImporter


class ScheduleWindow:
    ALLOWED_SLOTS = [
        (8,  30, 10,  0),
        (10, 15, 11, 45),
        (12, 15, 13, 45),
        (14,  0, 15, 30),
        (15, 45, 17, 15),
        (17, 30, 19,  0),
        (19, 15, 20, 45),
    ]

    def __init__(self, user_id):
        self.user_id = user_id
        self.current_date = datetime.now().date()
        self.setup_week_dates()
        self.selected_schedule_ids = set()

        self.root = tk.Tk()
        self.root.title("Plan zajęć – Niezbędnik Ucznia")
        self.root.geometry("1000x700")
        self.root.configure(background="white")

        self.create_widgets()
        self.load_schedule()

    def setup_week_dates(self):
        self.week_start = self.current_date - timedelta(days=self.current_date.weekday())
        self.week_dates = [self.week_start + timedelta(days=i) for i in range(5)]

    def create_widgets(self):
        # Nagłówek: nawigacja + akcje
        header = tk.Frame(self.root, bg="white")
        header.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(header, text="< Poprzedni tydzień", command=self.prev_week,
                  bg="PeachPuff3", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(header, text="Następny tydzień >", command=self.next_week,
                  bg="PeachPuff3", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        self.week_label = tk.Label(
            header,
            text=f"{self.week_dates[0].strftime('%d.%m.%Y')} – {self.week_dates[-1].strftime('%d.%m.%Y')}",
            bg="white", font=('Arial', 12, 'bold')
        )
        self.week_label.pack(side=tk.LEFT, padx=20)

        action_frame = tk.Frame(header, bg="white")
        action_frame.pack(side=tk.RIGHT)

        tk.Button(action_frame, text="+ Dodaj zajęcia", command=self.add_schedule,
                  bg="PeachPuff3", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        self.delete_button = tk.Button(action_frame, text="Usuń zajęcia",
                                       command=self.delete_schedule,
                                       bg="salmon", relief=tk.FLAT,
                                       state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        tk.Button(action_frame, text="+ Importuj plan", command=self.import_schedule,
                  bg="lightblue", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="↯ Eksportuj plan", command=self.export_schedule,
                  bg="lightgreen", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        self.schedule_table = tk.Frame(self.root, bg="white")
        self.schedule_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        for col, date in enumerate(self.week_dates, start=1):
            frame = tk.Frame(self.schedule_table, bg="white",
                             highlightthickness=1, highlightbackground="#e0e0e0")
            frame.grid(row=0, column=col, sticky="nsew")
            tk.Label(frame, text=f"{days[col-1][:3]}\n{date.strftime('%d.%m')}",
                     bg="white", font=('Arial', 10, 'bold')).pack(pady=5)

        time_slots = [
            "8:30-10:00", "10:15-11:45", "12:15-13:45",
            "14:00-15:30", "15:45-17:15", "17:30-19:00", "19:15-20:45"
        ]
        for row, label in enumerate(time_slots, start=1):
            tf = tk.Frame(self.schedule_table, bg="white",
                          highlightthickness=1, highlightbackground="#e0e0e0")
            tf.grid(row=row, column=0, sticky="nsew")
            tk.Label(tf, text=label, bg="white", font=('Arial', 9)).pack(pady=2)

            for col in range(1, 6):
                cell = tk.Frame(self.schedule_table, bg="white",
                                highlightthickness=1, highlightbackground="#e0e0e0",
                                width=150, height=40)
                cell.grid(row=row, column=col, sticky="nsew")
                cell.grid_propagate(False)

        for i in range(len(time_slots) + 1):
            self.schedule_table.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.schedule_table.grid_columnconfigure(i, weight=1, minsize=150)

    def load_schedule(self):
        for widget in self.schedule_table.winfo_children():
            info = widget.grid_info()
            if info["row"] > 0 and info["column"] > 0:
                for child in widget.winfo_children():
                    child.destroy()

        session = Session()
        try:
            schedules = session.query(Schedule).filter(
                Schedule.user_id == self.user_id,
                Schedule.date >= self.week_dates[0],
                Schedule.date <= self.week_dates[-1]
            ).all()
        finally:
            session.close()

        self.schedule_labels = []
        tooltip = None

        for sch in schedules:
            d = sch.date.weekday()
            if d > 4:
                continue

            start_min = sch.start_time.hour * 60 + sch.start_time.minute
            end_min   = sch.end_time.hour * 60 + sch.end_time.minute
            row = -1
            for i, (sh, sm, eh, em) in enumerate(self.ALLOWED_SLOTS):
                if start_min >= sh*60 + sm and end_min <= eh*60 + em:
                    row = i + 1
                    break
            if row < 0:
                continue

            target = None
            for w in self.schedule_table.winfo_children():
                info = w.grid_info()
                if info["row"] == row and info["column"] == d + 1:
                    target = w
                    break
            if not target:
                continue

            text = f"{sch.subject}\n{sch.type}\ns. {sch.room}"
            tip = (
                f"Nazwa: {sch.subject}\nKod: {sch.code}\nTyp: {sch.type}\n"
                f"Grupy: {sch.group}\nDydaktyk: {sch.teacher}\n"
                f"Budynek: {sch.building}\nSala: {sch.room}\n"
                f"Godziny: {sch.start_time.strftime('%H:%M')}-"
                f"{sch.end_time.strftime('%H:%M')}\n"
                f"Liczba studentów: {sch.student_count}"
            )

            lbl = tk.Label(target, text=text, bg="#e6f3ff",
                           relief=tk.RIDGE, borderwidth=1,
                           font=('Arial', 8), wraplength=140, justify=tk.LEFT)
            lbl.schedule_id = sch.id
            lbl.pack(fill=tk.BOTH, expand=True)
            self.schedule_labels.append(lbl)

            lbl.bind("<Button-1>", lambda e, l=lbl: self.toggle_selection(l))
            lbl.bind("<Enter>", lambda e, t=tip: self._show_tooltip(e, t))
            lbl.bind("<Leave>", lambda e: self._hide_tooltip())

    def _show_tooltip(self, event, text):
        if hasattr(self, '_tooltip') and self._tooltip:
            self._tooltip.destroy()
        self._tooltip = tk.Toplevel(self.root)
        self._tooltip.wm_overrideredirect(True)
        self._tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
        tk.Label(self._tooltip, text=text, bg="lightyellow",
                 relief=tk.SOLID, borderwidth=1, justify=tk.LEFT).pack()

    def _hide_tooltip(self):
        if hasattr(self, '_tooltip') and self._tooltip:
            self._tooltip.destroy()
            self._tooltip = None

    def toggle_selection(self, label):
        sid = label.schedule_id
        if sid in self.selected_schedule_ids:
            self.selected_schedule_ids.remove(sid)
            label.config(bg="#e6f3ff")
        else:
            self.selected_schedule_ids.add(sid)
            label.config(bg="lightblue")

        self.delete_button.config(
            state=tk.NORMAL if self.selected_schedule_ids else tk.DISABLED
        )

    def delete_schedule(self):
        if not self.selected_schedule_ids:
            messagebox.showwarning("Ostrzeżenie", "Nie wybrano zajęć do usunięcia")
            return

        if not messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno usunąć {len(self.selected_schedule_ids)} zaznaczone zajęcia?"
        ):
            return

        session = Session()
        try:
            session.query(Schedule) \
                   .filter(Schedule.id.in_(list(self.selected_schedule_ids))) \
                   .delete(synchronize_session=False)
            session.commit()
            messagebox.showinfo("Sukces", "Wybrane zajęcia usunięto")
            self.selected_schedule_ids.clear()
            self.delete_button.config(state=tk.DISABLED)
            self.load_schedule()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Błąd", f"Nie udało się usunąć zajęć: {e}")
        finally:
            session.close()

    def prev_week(self):
        self.current_date -= timedelta(weeks=1)
        self.setup_week_dates()
        self.update_dates_display()
        self.load_schedule()

    def next_week(self):
        self.current_date += timedelta(weeks=1)
        self.setup_week_dates()
        self.update_dates_display()
        self.load_schedule()

    def update_dates_display(self):
        self.week_label.config(
            text=f"{self.week_dates[0].strftime('%d.%m.%Y')} – "
                 f"{self.week_dates[-1].strftime('%d.%m.%Y')}"
        )
        short = ["Pon", "Wt", "Śr", "Czw", "Pt"]
        for col, date in enumerate(self.week_dates, start=1):
            for w in self.schedule_table.winfo_children():
                info = w.grid_info()
                if info["row"] == 0 and info["column"] == col:
                    for ch in w.winfo_children():
                        if isinstance(ch, tk.Label):
                            ch.config(text=f"{short[col-1]}\n{date.strftime('%d.%m')}")

    def add_schedule(self):
        dialog = Toplevel(self.root)
        dialog.title("Dodaj zajęcia")
        dialog.geometry("400x500")
        dialog.resizable(False, False)

        fields = [
            "Kod przedmiotu", "Nazwa przedmiotu", "Typ zajęć", "Grupy",
            "Dydaktyk", "Budynek", "Sala", "Liczba studentów",
            "Godzina rozpoczęcia (HH:MM)", "Godzina zakończenia (HH:MM)",
            "Data (YYYY-MM-DD)"
        ]
        entries = {}
        for i, name in enumerate(fields):
            tk.Label(dialog, text=name).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ent = tk.Entry(dialog)
            ent.grid(row=i, column=1, padx=10, pady=5)
            entries[name] = ent

        tk.Label(dialog, text="Powtarzanie:").grid(row=len(fields), column=0, sticky="w", padx=10, pady=5)
        rep_var = tk.StringVar(value="Brak")
        opts = ["Brak", "Co tydzień", "Co 2 tygodnie", "Co miesiąc"]
        tk.OptionMenu(dialog, rep_var, *opts).grid(row=len(fields), column=1, padx=10, pady=5)

        def save():
            try:
                data = {n: e.get().strip() for n, e in entries.items()}
                missing = [n for n, v in data.items() if not v]
                if missing:
                    raise ValueError(f"Brakujące pola: {', '.join(missing)}")

                student_count = int(data["Liczba studentów"])
                if student_count < 0:
                    raise ValueError("Liczba studentów nie może być ujemna")

                start_time = datetime.strptime(data["Godzina rozpoczęcia (HH:MM)"], "%H:%M").time()
                end_time   = datetime.strptime(data["Godzina zakończenia (HH:MM)"], "%H:%M").time()
                date       = datetime.strptime(data["Data (YYYY-MM-DD)"], "%Y-%m-%d").date()
                if end_time <= start_time:
                    raise ValueError("Godzina zakończenia musi być późniejsza niż godzina rozpoczęcia")

                # walidacja slotów
                s_min = start_time.hour*60 + start_time.minute
                e_min = end_time.hour*60 + end_time.minute
                if not any(s_min >= sh*60+sm and e_min <= eh*60+em for sh,sm,eh,em in self.ALLOWED_SLOTS):
                    slots = ", ".join(f"{sh:02d}:{sm:02d}-{eh:02d}:{em:02d}"
                                      for sh,sm,eh,em in self.ALLOWED_SLOTS)
                    raise ValueError(f"Zajęcia muszą odbywać się w jednym z przedziałów:\n{slots}")

                session = Session()
                base = dict(
                    user_id=self.user_id,
                    date=date,
                    day_of_week=date.strftime("%A"),
                    start_time=start_time,
                    end_time=end_time,
                    code=data["Kod przedmiotu"],
                    subject=data["Nazwa przedmiotu"],
                    type=data["Typ zajęć"],
                    group=data["Grupy"],
                    teacher=data["Dydaktyk"],
                    building=data["Budynek"],
                    room=data["Sala"],
                    student_count=student_count
                )
                session.add(Schedule(**base))

                rep = rep_var.get()
                if rep != "Brak":
                    delta = (
                        timedelta(weeks=1) if rep == "Co tydzień" else
                        timedelta(weeks=2) if rep == "Co 2 tygodnie" else
                        timedelta(days=30)
                    )
                    nd = date
                    for _ in range(10):
                        nd += delta
                        base["date"] = nd
                        base["day_of_week"] = nd.strftime("%A")
                        session.add(Schedule(**base))

                session.commit()
                messagebox.showinfo("Sukces", "Zajęcia dodane!")
                dialog.destroy()
                self.load_schedule()

            except ValueError as ve:
                messagebox.showerror("Błąd", f"Nieprawidłowe dane: {ve}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać zajęć: {e}")
            finally:
                try:
                    session.close()
                except:
                    pass

        tk.Button(dialog, text="Zapisz", command=save,
                  bg="PeachPuff3", relief=tk.FLAT) \
            .grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        entries["Kod przedmiotu"].focus_set()

    def export_schedule(self):
        session = Session()
        try:
            schedules = session.query(Schedule).filter(
                Schedule.user_id == self.user_id,
                Schedule.date >= self.week_dates[0],
                Schedule.date <= self.week_dates[-1]
            ).order_by(Schedule.date, Schedule.start_time).all()
        finally:
            session.close()

        if not schedules:
            messagebox.showinfo("Eksport", "Brak zajęć do eksportu.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
        )
        if not path:
            return

        try:
            ScheduleExporter.export_to_csv(schedules, path)
            messagebox.showinfo("Eksport", f"Plan zapisany do:\n{path}")
        except Exception as e:
            messagebox.showerror("Błąd eksportu", str(e))

    def import_schedule(self):
        path = filedialog.askopenfilename(
            title="Wybierz plik CSV z planem",
            filetypes=[("CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
        )
        if not path:
            return

        clear = messagebox.askyesno(
            "Import", "Usunąć istniejące zajęcia tego użytkownika przed importem?"
        )
        try:
            count = ScheduleImporter.import_from_csv(path, self.user_id, clear_existing=clear)
            messagebox.showinfo("Import", f"Zaimportowano {count} zajęć.")
            self.load_schedule()
        except Exception as e:
            messagebox.showerror("Błąd importu", str(e))

    def run(self):
        self.root.mainloop()
