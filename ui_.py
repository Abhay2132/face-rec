import customtkinter as ctk
# import cv2
# import customtkinter as ctk
# cap = cv2.VideoCapture(0)

class MainFrame(ctk.CTkFrame) :
	def __init__(self, master):
		super().__init__(master)
		
		self.grid_columnconfigure(0, minsize=150, weight=1)
		self.grid_rowconfigure(0, minsize=150, weight=1)
		
		self.label = ctk.CTkLabel(master=self, text="Starting Camera ...", corner_radius=10, text_color="#ffffff", fg_color="#333333")
		self.label.grid(pady=10, padx=5, row=0, column=0, sticky="we")

		self.fps = ctk.CTkLabel(master=self, text="fps : 0")
		self.fps.grid(row=0, column=0, padx=10, sticky="ne")

class LeftFrame(ctk.CTkFrame) :
	def __init__(self, master):
		super().__init__(master)
		
		self.grid_columnconfigure(0, weight=1)
		self.label = ctk.CTkLabel(master=self, text="Records")
		self.label.grid( row=0, column=0, sticky="w", padx=10)
		
		ctk.CTkFrame(master=self, height=2, fg_color=("#eee", "#333")).grid(row=1, column=0, sticky="we")
		
		self.searchBar = SearchBar(master=self)
		self.searchBar.grid(row=2, column=0, sticky="we")

class RightFrame(ctk.CTkFrame) :
	def __init__(self, master):
		super().__init__(master)
		
		self.button = ctk.CTkButton(master=self, text="right frame")
		self.button.grid(row=0, column=0, sticky="e")
		

class SearchBar(ctk.CTkFrame) :
	def __init__(self, master):
		super().__init__(master, fg_color="transparent" )
		
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		
		self.entry = ctk.CTkEntry(master=self, fg_color="transparent", placeholder_text="Search User")
		self.entry.grid(padx=5, pady=5, row=0, column=0, sticky="we")
		
		# self.submit = ctk.CTkButton(master=self, text="->", width=30)
		# self.submit.grid(padx=(3,0), row=0, column=1)
		
		
		