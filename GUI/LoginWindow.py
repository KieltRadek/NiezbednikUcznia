import tkinter as tk

from ModelsDataBase.DataBase import Session
from ModelsDataBase.User import User


class LoginWindow:


    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("285x140+800+300")
        self.root.title("SE Login")
        self.root.resizable(False, False)

        self.root.configure(background=self.setColorBackground())

        self.addWidgets()


    def addWidgets(self):
       self.loginPanel()


    def loginPanel(self):
        self.loginLabel = tk.Label(self.root, text="Email:", background=self.setColorBackground())
        self.loginLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.loginEntry = tk.Entry(self.root, width=20,background=self.setColorButtonAndTextField(),justify="left")
        self.loginEntry.grid(row=0, column=1,padx=10, pady=10, sticky="we")

        self.passwordLabel = tk.Label(self.root, text="Password:", background=self.setColorBackground())
        self.passwordLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.passwordEntry = tk.Entry(self.root, width=20,show="*",background=self.setColorButtonAndTextField(),justify="left")
        self.passwordEntry.grid(row=1, column=1,padx=10, pady=10, sticky="we")

        self.backToLoginOrRegisterMenuButton = tk.Button(self.root,text="Back",padx=30, pady=5, cursor="hand2",activebackground="grey",background=self.setColorButtonAndTextField(),command=self.backToLoginOrRegister)
        self.backToLoginOrRegisterMenuButton.grid(row=2, column=0,padx=10, pady=10, sticky="w")
        self.confirmButton = tk.Button(self.root,text="Confirm",padx=24, pady=5, cursor="hand2",activebackground="grey",background=self.setColorButtonAndTextField(), command=self.login_user)
        self.confirmButton.grid(row=2, column=1,padx=10, pady=10, sticky="e")

        self.showPassword = tk.BooleanVar()
        self.passwordCheckBox = tk.Checkbutton(self.root,background=self.setColorBackground(),variable=self.showPassword,command=self.showPasswordFunc)
        self.passwordCheckBox.grid(row=1, column=2,padx=0, pady=5, sticky="we")

    def showPasswordFunc(self):
        if self.showPassword.get():
            self.passwordEntry.config(show="")
        else:
            self.passwordEntry.config(show="*")

    def setColorBackground(self):
        return "PeachPuff2"


    def setColorButtonAndTextField(self):
        return "PeachPuff3"


    def backToLoginOrRegister(self):
        from GUI.LoginOrRegister import LoginOrRegister #nie da się na zimportować na górze
        self.root.destroy()
        LoginOrRegister()

    def login_user(self):
        from GUI.ScheduleWindow import ScheduleWindow
        from GUI.MainMenuView import MainMenuView
        session = Session()
        email = self.loginEntry.get()
        password = self.passwordEntry.get()

        user = session.query(User).filter(User.email == email, User.password == password).first()

        if user:
            self.root.destroy()
            main_menu = MainMenuView(user.id)
            # ScheduleWindow(user.id)
        else:
            tk.messagebox.showerror("Błąd", "Nieprawidłowy email lub hasło")
        session.close()




