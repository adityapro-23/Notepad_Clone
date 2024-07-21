from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font
import os

fontsizes = ('8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24',
             '26', '28', '36', '48', '72')

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)


def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                      ("Text Documents", "*.txt")])

    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()


def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile="Untitled.txt",
                                 defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])

        if file == "":
            file = None
        else:
            # Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()
            root.title(os.path.basename(file) + " - Notepad")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp():
    root.destroy()


def cut():
    TextArea.event_generate("<<Cut>>")


def copy():
    TextArea.event_generate("<<Copy>>")


def paste():
    TextArea.event_generate("<<Paste>>")


def font_dialog():
    root2 = Toplevel(root)
    root2.geometry("444x444")
    root2.minsize(444, 444)
    root2.maxsize(444, 444)
    root2.title("Font Dialog")

    lbx = Listbox(root2, selectmode=SINGLE, exportselection=0)  # exportselection = 0 is used to select options from multiple listboxes
    for item in sorted(font.families()):
        lbx.insert(END, item)
    lbx.pack(side=LEFT, padx=20)

    lbx2 = Listbox(root2, width=5, height=10, selectmode=SINGLE)
    for size in fontsizes:
        lbx2.insert(END, size)
    lbx2.pack(side=LEFT, padx=20)

    radvar = StringVar()
    radvar.set("Radio")
    radio1 = Radiobutton(root2, text = "Normal", variable = radvar, value = "normal").pack()
    radio2 = Radiobutton(root2, text = "Bold", variable = radvar, value = "bold").pack()
    radio3 = Radiobutton(root2, text = "Italic", variable = radvar, value = "italic").pack()

    def change_font():
        # For selecting an option from first listbox
        for i in lbx.curselection():
            font_name = (lbx.get(i)).replace(" ", "")
        # For selecting an option from second listbox
        for j in lbx2.curselection():
            font_size = int(lbx2.get(j))

        font_style = radvar.get()
        try:
            TextArea.config(font=(f"{font_name} {font_size} {font_style}"))
        except Exception as e:
            showinfo("Error", "Select all three fields!")
        
    btn = Button(root2, text="Apply", width=10, height=1, command=change_font)
    btn.pack(side=BOTTOM, padx=30, pady=30)

    root2.mainloop()


def about():
    showinfo("Notepad", "Notepad by Aditya Patil")


if __name__ == '__main__':
    # Basic tkinter setup
    root = Tk()
    root.title("Untitled - Notepad")
    root.wm_iconbitmap("notepad1.ico")
    root.geometry("644x788")

    # Adding TextArea
    TextArea = Text(root, font="lucida 13")
    file = None
    TextArea.pack(expand=True, fill=BOTH)

    # Creating a menubar
    MenuBar = Menu(root)
    # Creating File Menu
    FileMenu = Menu(MenuBar, tearoff=0)
    # To open new file
    FileMenu.add_command(label="New", command=newFile)

    # To open already existing file
    FileMenu.add_command(label="Open", command=openFile)

    # To save the current file
    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)


    # Creating Edit Menu
    EditMenu = Menu(MenuBar, tearoff=0)
    # To give a features of cut, copy and paste
    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copy)
    EditMenu.add_command(label="Paste", command=paste)
    EditMenu.add_command(label="Font", command=font_dialog)
    MenuBar.add_cascade(label="Edit", menu=EditMenu)


    # Creating Help Menu
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # Menubar configured
    root.config(menu=MenuBar)

    # Adding Scrollbar
    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT, fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    root.mainloop()