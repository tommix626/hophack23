# import statement
from tkinter import *
from PIL import ImageTk, Image

# ---------------------------------------------
# windows
# ---------------------------------------------

# create the main application
root = Tk()
root.title("First_Program")
root.geometry('350x200')

# create a 2nd window + hide till needed
newWindow = Toplevel(root)
newWindow.withdraw() #hide first
newWindow.title("New Window")
newWindow.geometry("200x200")

# A Label widget to show in toplevel
label = Label(newWindow,
        text ="This is a new window")
label.grid()

# ---------------------------------------------
# function clicks
# ---------------------------------------------

def clicked():
    label.configure(text = 'I just got clicked')

def clicked2():
    res = 'You wrote ' + txt.get()
    label.configure(text = res)

def clicked_for_new_window():
    newWindow.deiconify()

# ---------------------------------------------
# widgets
# ---------------------------------------------

# [root]: label
label = Label(root, text ="Hello World !")
label.grid()

# [root]: label with image
img = ImageTk.PhotoImage(Image.open('1.jpeg').resize((280, 300)))
image_label = Label(root, image=img)
image_label.grid(row = 3)

# [root]: user input
txt = Entry(root, width = 10)
txt.grid(column=1, row=0)

# [root]: button
button = Button(root, text = 'Click me', bg= 'white', fg = 'blue', command = clicked_for_new_window)\
    .grid(column=0, row=1)

# [root]: button
button2 = Button(root, text = 'Exit', command=root.destroy).grid(pady = 10, row=2)

# [root]: menu
menu1 = Menu(root)
item = Menu(menu1)
item.add_command(label = 'New')
menu1.add_cascade(label = 'File', menu = item)
root.config(menu=menu1)   

# ---------------------------------------------
# run
# ---------------------------------------------
root.mainloop()
