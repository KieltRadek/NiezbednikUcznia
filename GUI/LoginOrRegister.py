import tkinter as tk
from GUI.LoginWindow import LoginWindow
from GUI.RegisterWindow import RegisterWindow

class LoginOrRegister:


    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x120+800+300")
        self.root.title("Student's essential")
        self.root.resizable(False, False)
        self.root.configure(background=self.setColor())

        self.addWidgets()


    def addWidgets(self):
      self.loginComponents()
      self.registerComponents()


    def loginComponents(self):
        textLogin = tk.Label(self.root, text="Have an account?",background=self.setColor())
        loginButton = tk.Button(self.root,text="Login",padx=30,pady=5,cursor="hand2",activebackground="grey",background="PeachPuff3",command=self.openLoginWindow)
        textLogin.pack()
        loginButton.pack()


    def registerComponents(self):
        textRegister = tk.Label(self.root, text="New user?",background=self.setColor())
        registerButton = tk.Button(self.root, text="Register", padx=24, pady=5, cursor="hand2",activebackground="grey",background="PeachPuff3",command=self.openRegisterWindow)
        textRegister.pack()
        registerButton.pack()


    def setColor(self):
        return "PeachPuff2"


    def openLoginWindow(self):
        self.root.destroy()
        LoginWindow()


    def openRegisterWindow(self):
        self.root.destroy()
        RegisterWindow()












