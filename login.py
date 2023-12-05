import customtkinter as ctk

class Login(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="#fefefe", corner_radius=10)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.logo = ctk.CTkLabel(master=self, text="LOGO")
        self.logo.grid(row=0, column=0, sticky='we')
        
        # self.
        self.userInput = ctk.CTkEntry(master=self, placeholder_text="Username")
        self.userInput.grid(row=1, column=0, sticky='we', padx=50, pady=10)
        
        self.keyInput = ctk.CTkEntry(master=self, placeholder_text="Password")
        self.keyInput.grid(row=2, column=0, sticky='we', padx=50, pady=10)
        
        self.submit = ctk.CTkButton(master=self, text='Submit')
        self.submit.grid(row=3, column=0, sticky='ns', padx=10, pady=10)
        
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("LOGIN")
    root.geometry("600x400")
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    loginFrame = Login(root)
    loginFrame.grid(row=0, column=0, sticky="nswe", padx=90, pady=60)
    
    # loginFrame.pack()
    
    root.mainloop()