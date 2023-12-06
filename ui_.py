import customtkinter as ctk
from faceAPI import mainAPI


# import cv2
# import customtkinter as ctk
# cap = cv2.VideoCapture(0)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.grid_columnconfigure(0, minsize=150, weight=1)
        self.grid_rowconfigure(0, minsize=150, weight=1)

        self.label = ctk.CTkLabel(master=self, text="Click to Start Camera", corner_radius=10, text_color="#ffffff",
                                  fg_color="#333333")
        self.label.grid(pady=10, padx=5, row=0, column=0, sticky="we")

        self.fps = ctk.CTkLabel(master=self, text="fps : 0")
        self.fps.grid(row=0, column=0, padx=10, sticky="ne")


class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # topbar
        self.userList = None
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(3, weight=1)
        self.label = ctk.CTkLabel(master=self, text="Records")
        self.label.grid(row=0, column=0, sticky="w", padx=10)

        # horizontal line after topbar
        ctk.CTkFrame(master=self, height=2, fg_color=("#eee", "#333")).grid(row=1, column=0, sticky="we")

        # search Bar
        self.searchBar = SearchBar(master=self)
        self.searchBar.grid(row=2, column=0, sticky="we")

        self.loadSavedPersons()

        self.bottomFrame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.bottomFrame.grid(row=4, column=0, pady=5)
        # self.bottomFrame.grid_columnconfigure((0,1), weight=0)

        self.addImage = ctk.CTkButton(master=self.bottomFrame, text="Add", width=80)
        self.addImage.grid(row=4, column=0, sticky='we', padx=10)
        # self.addImage.pack(side=ctk.LEFT)

        self.trainBtn = ctk.CTkButton(master=self.bottomFrame, text="Train", width=80)
        self.trainBtn.grid(row=4, column=1, sticky='we', padx=10)

    # self.trainBtn.pack(side=ctk.LEFT)

    def loadSavedPersons(self):
        if self.userList:
            self.userList.destroy()
        # list of saved user data
        userListData = set(mainAPI.SavedEncoding.getPersons())

        # List of Saved Users Element
        self.userList = UserList(self, userListData)
        self.userList.grid(row=3, column=0, sticky="ns")


class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        #
        # self.button = ctk.CTkButton(master=self, text="right frame")
        # self.button.grid(row=0, column=0, sticky="e")
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.label = ctk.CTkLabel(master=self, text="Attendance List")
        self.label.grid(row=0, column=0, sticky="w", padx=10)

        ctk.CTkFrame(master=self, height=2, fg_color=("#eee", "#333")).grid(row=1, column=0, sticky="we")

        self.userList = UserList(self)
        self.userList.grid(row=2, column=0, sticky="ns")

        self.reportButton = ctk.CTkButton(master=self, text="Get Report")
        self.reportButton.grid(row=3, column=0, sticky='we', padx=20)

        # horizontal line after topbar
        ctk.CTkFrame(master=self, height=2, fg_color=("#eee", "#333")).grid(row=1, column=0, sticky="we")


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

    def addUser(self, id, name):
        newUser = ctk.CTkLabel(master=self, text=str(id) + " " * (4 - len(str(id))) + str(name))
        newUser.grid(row=len(self.userItems) + 1, column=0, sticky='w')
        self.userItems.append(newUser)

    def __init__(self, master, users=set()):
        super().__init__(master, fg_color="transparent")

        self.users = users
        self.grid_rowconfigure(0, weight=1)

        # list heading
        newUser = ctk.CTkLabel(master=self, text="ID | Name")
        newUser.grid(row=0, column=0, sticky='w')

        row = 1
        for (id, name) in self.users:
            # newUser = ctk.CTkLabel(master=self, text=str(id) + " "*(4-len(str(id))) + str(name))
            # newUser.grid(row=row, column=0, sticky='w')
            self.addUser(id, name)
            row += 1
            print(id, name)


class UserItem(ctk.CTkFrame):
    def __init__(self, master, id, name, row):
        super().__init__(master, fg_color="transparent", height=40)

        self.grid_rowconfigure(0, weight=1)
        self.label = ctk.CTkLabel(master=self, text=str(id) + ".) " + str(name), fg_color="#cccccc")
        self.label.grid(row=0, column=0, sticky="we")

        self.grid(row=row, column=0)
