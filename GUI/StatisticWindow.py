import tkinter as tk
from tkinter import messagebox
import csv
from sqlalchemy import func
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Grade import Grade

class StatisticWindow:

    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.geometry("250x250+800+300")
        self.root.title("Statistics")
        self.root.configure(background="PeachPuff2")
        self.root.resizable(False, False)

        session = Session()
        self.total_grades = session.query(func.count(Grade.id)).filter(Grade.user_id == self.user_id).scalar()
        self.avg_grade = session.query(func.avg(Grade.grade_value)).filter(Grade.user_id == self.user_id).scalar()
        self.max_grade = session.query(func.max(Grade.grade_value)).filter(Grade.user_id == self.user_id).scalar()
        self.min_grade = session.query(func.min(Grade.grade_value)).filter(Grade.user_id == self.user_id).scalar()
        session.close()

        font_label = ("Arial", 15, "bold")
        tk.Label(self.root, text=f"Liczba ocen: {self.total_grades}", background="PeachPuff2", font=font_label).pack(pady=5)
        tk.Label(self.root, text=f"Średnia ocen: {self.avg_grade:.2f}" if self.avg_grade else "Średnia ocen: brak", background="PeachPuff2", font=font_label).pack(pady=5)
        tk.Label(self.root, text=f"Najwyższa ocena: {self.max_grade}" if self.max_grade else "Najwyższa ocena: brak", background="PeachPuff2", font=font_label).pack(pady=5)
        tk.Label(self.root, text=f"Najniższa ocena: {self.min_grade}" if self.min_grade else "Najniższa ocena: brak", background="PeachPuff2", font=font_label).pack(pady=5)
        button_frame = tk.Frame(self.root, background="PeachPuff2")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Export",cursor="hand2", activebackground="grey", background="PeachPuff3",command=self.export_statistics).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Back",cursor="hand2" ,activebackground="grey", background="PeachPuff3", command=self.back).grid(row=0, column=1, padx=5)

        self.root.mainloop()

    def back(self):
        self.root.destroy()
        from GUI.MainMenuView import MainMenuView
        MainMenuView(self.user_id)

    def export_statistics(self):
        with open(f'statistics_user_{self.user_id}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Liczba ocen', 'Średnia ocen', 'Najwyższa ocena', 'Najniższa ocena'])
            writer.writerow([
                self.total_grades,
                f"{self.avg_grade:.2f}" if self.avg_grade else 'brak',
                self.max_grade if self.max_grade else 'brak',
                self.min_grade if self.min_grade else 'brak'
            ])
        messagebox.showinfo("Eksport", f"Dane statystyk zapisane do pliku statistics_user_{self.user_id}.csv!")
