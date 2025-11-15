import tkinter as tk
from tkinter import messagebox
from ModelsDataBase.User import User
from ModelsDataBase.DataBase import Session

class RegisterWindow:


    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("285x220+800+300")
        self.root.title("SE Login")
        self.root.resizable(False, False)

        self.root.configure(background=self.setColorBackground())

        self.addWidgets()


    def addWidgets(self):
        self.registerPanel()


    def registerPanel(self):

        self.nameLabel = tk.Label(self.root, text="Name:", background=self.setColorBackground())
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.nameEntry = tk.Entry(self.root, width=20,background=self.setColorButtonAndTextField(),justify="left")
        self.nameEntry.grid(row=0, column=1,padx=10, pady=10, sticky="we")

        self.surnameLabel = tk.Label(self.root, text="Surname:", background=self.setColorBackground())
        self.surnameLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.surnameEntry = tk.Entry(self.root, width=20,background=self.setColorButtonAndTextField(),justify="left")
        self.surnameEntry.grid(row=1, column=1,padx=10, pady=10, sticky="we")

        self.emailLabel = tk.Label(self.root, text="E-mail:", background=self.setColorBackground())
        self.emailLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.emailEntry = tk.Entry(self.root,width=20,background=self.setColorButtonAndTextField(),justify="left")
        self.emailEntry.grid(row=2, column=1,padx=10, pady=10, sticky="we")

        self.passwordLabel = tk.Label(self.root, text="Password:", background=self.setColorBackground())
        self.passwordLabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.passwordEntry = tk.Entry(self.root,width=20,show="*",background=self.setColorButtonAndTextField(),justify="left")
        self.passwordEntry.grid(row=3, column=1,padx=10, pady=10, sticky="we")


        self.backToLoginOrRegisterMenuButton = tk.Button(self.root,text="Back",padx=30, pady=5, cursor="hand2",activebackground="grey",background=self.setColorButtonAndTextField(),command=self.backToLoginOrRegister)
        self.backToLoginOrRegisterMenuButton.grid(row=4, column=0,padx=10, pady=10, sticky="sw")
        self.confirmButton = tk.Button(self.root,text="Confirm",padx=24, pady=5, cursor="hand2",activebackground="grey",background=self.setColorButtonAndTextField(),command=self.sendToDataBase)
        self.confirmButton.grid(row=4, column=1,padx=10, pady=10, sticky="se")

        self.showPassword = tk.BooleanVar()
        self.passwordCheckBox = tk.Checkbutton(self.root,background=self.setColorBackground(),variable=self.showPassword,command=self.showPasswordFunc)
        self.passwordCheckBox.grid(row=3, column=2,padx=0, pady=5, sticky="we")

    def showPasswordFunc(self):
        if self.showPassword.get():
            self.passwordEntry.config(show="")
        else:
            self.passwordEntry.config(show="*")


    def backToLoginOrRegister(self):
        from GUI.LoginOrRegister import LoginOrRegister #nie da się na zimportować na górze
        self.root.destroy()
        LoginOrRegister()


    def setColorBackground(self):
        return "PeachPuff2"


    def setColorButtonAndTextField(self):
        return "PeachPuff3"


    def sendToDataBase(self):
        session = Session()

        # email = self.emailEntry.get()
        email = self.emailEntry.get()

        isExist = session.query(User).filter(User.email==email).first()
        #session.query(User) = SELECT * FROM users
        #.filter= WHERE
        #.first -> zwraca None jesli nie ma, jesli jest zwraca istniejący obiekt


        if isExist:
            messagebox.showinfo("Rejestracja", "Ten email jest już zarejestrowany")
            session.close()
            return

        newUser = User(
            name = self.nameEntry.get(),
            surname = self.surnameEntry.get(),
            email = self.emailEntry.get(),
            password = self.passwordEntry.get()
        )
        session.add(newUser)
        session.commit()
        session.close()
        messagebox.showinfo("Rejestracja","Zarejestrowano pomyślnie!")