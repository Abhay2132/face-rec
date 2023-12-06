import customtkinter as ctk
from PIL import ImageTk, Image  
import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])

class LogoFrame (ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent", width=100, height=100)

        logoImage = Image.open(os.path.join(cwd, "assets", "user.png"))
        # logoImage = ImageTk.PhotoImage(logoImage)
        logoImage = ctk.CTkImage(logoImage, size=(100,100))

        self.logo = ctk.CTkLabel(master=self, text="", fg_color="transparent", image=logoImage, height=100, width=100)
        self.logo.grid(row=0, column=0)

class Login(ctk.CTkFrame):
    def __init__(self, master, **kwargs):

        super().__init__(master=master, fg_color="#fefefe")
        self._master = master

        self.logoFrame = LogoFrame(self)
        self.logoFrame.grid(row=0, column=0, padx=10, pady=10)

        self.userInput = ctk.CTkEntry(master=self, placeholder_text="Username", width=300)
        self.userInput.grid(row=1, column=0, sticky='we', padx=50, pady=10)


        self.keyInput = ctk.CTkEntry(master=self, placeholder_text="Password", show="*")
        self.keyInput.grid(row=2, column=0, sticky='we', padx=50, pady=0)

        self.userInput.insert(0,"Abhay")
        self.keyInput.insert(0,"India")

        self.submit = ctk.CTkButton(master=self, text='LOGIN', command=self.onSubmit)
        self.submit.grid(row=3, column=0, sticky='ns', padx=10, pady=10)

    def onLogin(self):
        return 0
    
    def onSubmit(self):
        user = self.userInput.get()
        key = self.keyInput.get()

        # print(f"user:'{user}',key:'{key}'")

        if user == "Abhay" and key == "India":
            self._master.onLogin()
    
    def show(self):
        self.grid(row=0, column=0)
        
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("LOGIN")
    root.geometry("800x600")
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    loginFrame = Login(root)
    loginFrame.show()
    
    # loginFrame.pack()
    
    root.mainloop()