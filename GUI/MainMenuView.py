import tkinter as tk

class MainMenuView():


    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.geometry("200x120+800+300")
        self.root.title("Main Menu")
        self.root.resizable(False, False)
        self.root.configure(background=self.setColorBackground())


        self.buttons()

    def addWidgets(self):
        self.buttons()


    def buttons(self):


        self.scheduleWindow = tk.Button(self.root, text="Schedule", cursor="hand2",activebackground="grey",background=self.setColorButtonAndTextField(), command=self.open_schedule)
        self.scheduleWindow.grid(row=1, column=1, padx=15, pady=5, sticky="w")
        self.grades = tk.Button(
        self.root, text="Grades    ", cursor="hand2",activebackground = "grey", background = self.setColorButtonAndTextField(),
        command = self.open_grades)
        self.grades.grid(row=2, column=1, padx=15, pady=5, sticky="w")
        self.statistic = tk.Button(self.root, text="Statistics ", cursor="hand2", activebackground="grey",
                                   background=self.setColorButtonAndTextField(), command=self.open_statistics)
        self.statistic.grid(row=3, column=1, padx=15, pady=5, sticky="w")



    def setColorBackground(self):
        return "PeachPuff2"

    def setColorButtonAndTextField(self):
        return "PeachPuff3"

    def open_schedule(self):
        from GUI.ScheduleWindow import ScheduleWindow
        self.root.destroy()
        ScheduleWindow(self.user_id)
        print("Otwieram plan lekcji...")

    def open_statistics(self):
        from GUI.StatisticWindow import StatisticWindow
        self.root.destroy()
        StatisticWindow(self.user_id)
        print("Otwieram statystyki...")

    def open_grades(self):
        from GUI.GradesWindow import GradesWindow
        self.root.destroy()
        GradesWindow(self.user_id).run()
        print("Otwieram moduł ocen...")
