import customtkinter as ctk
from faceAPI import mainAPI


# import cv2
# import customtkinter as ctk
# cap = cv2.VideoCapture(0)

class MainFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.grid_columnconfigure(0, minsize=150, weight=1)
		self.grid_rowconfigure(0, minsize=150, weight=1)

		self.label = ctk.CTkLabel(master=self, text="Starting Camera ...", corner_radius=10, text_color="#ffffff",
								  fg_color="#333333")
		self.label.grid(pady=10, padx=5, row=0, column=0, sticky="we")

		self.fps = ctk.CTkLabel(master=self, text="fps : 0")
		self.fps.grid(row=0, column=0, padx=10, sticky="ne")


class LeftFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		# topbar
		self.grid_columnconfigure(0, weight=1)

		self.grid_rowconfigure(3, weight=1)
		self.label = ctk.CTkLabel(master=self, text="Records")
		self.label.grid(row=0, column=0, sticky="w", padx=10)


		# horizontal line after topbar
		ctk.CTkFrame(master=self, height=2, fg_color=("#eee", "#333")).grid(row=1, column=0, sticky="we")

		# search Bar
		self.searchBar = SearchBar(master=self)
		self.searchBar.grid(row=2, column=0, sticky="we")

		# List of Saved Users
		self.userList = UserList(master=self)
		self.userList.grid(row=3, column=0, sticky="ns")
	# row = 3
	# for (id, name) in self.users:
	# 	newUser = UserItem(self, id, name, row)
	# 	self.userItems.append(newUser)
	# 	row += 1


class RightFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)

		self.button = ctk.CTkButton(master=self, text="right frame")
		self.button.grid(row=0, column=0, sticky="e")


class SearchBar(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="transparent")

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)

		self.entry = ctk.CTkEntry(master=self, fg_color="transparent", placeholder_text="Search User")
		self.entry.grid(padx=5, pady=5, row=0, column=0, sticky="we")

# self.submit = ctk.CTkButton(master=self, text="->", width=30)
# self.submit.grid(padx=(3,0), row=0, column=1)


class UserList(ctk.CTkScrollableFrame):
	users = {(2, "ABHAY"), (3, 'Saurabh')}
	userItems = []

	def __init__(self, master):
		super().__init__(master, fg_color="transparent")

		self.users = set(mainAPI.SavedEncoding.getPersons())
		self.grid_rowconfigure(0, weight=1)

		# list heading
		newUser = ctk.CTkLabel(master=self, text="ID | Name")
		newUser.grid(row=0, column=0, sticky='w')

		row = 1
		for (id, name) in self.users:
			newUser = ctk.CTkLabel(master=self, text=str(id) + " "*(4-len(str(id))) + str(name))
			newUser.grid(row=row, column=0, sticky='w')
			self.userItems.append(newUser)
			row += 1
			print(id, name)


class UserItem(ctk.CTkFrame):
	def __init__(self, master, id, name, row):
		super().__init__(master, fg_color="transparent", height=40)
		# self.grid_columnconfigure(0, weight=1)
		# self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		#
		# self.idLabel = ctk.CTkLabel(master=self, text=str(id))
		# self.idLabel.grid(row=0, column=0, sticky="w")
		#
		# self.nameLabel = ctk.CTkLabel(master=self, text=str(name))
		# self.nameLabel.grid(row=0, column=1)

		self.label = ctk.CTkLabel(master=self, text=str(id) + ".) " + str(name), fg_color="#cccccc")
		self.label.grid(row=0, column=0, sticky="we")

		self.grid(row=row, column=0)
