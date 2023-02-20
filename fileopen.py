from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
 
root = Tk()
root.title('filedialog study')
 
root.filename = filedialog.askopenfilename(initialdir='./png',title='파일선택', filetypes=(('png files','*.png'),('jpg files','*.jpg'),('all files','*.*')))
 
Label(root, text=root.filename).pack()
my_image = ImageTk.PhotoImage(Image.open(root.filename))
Label(image=my_image).pack()
 
root.mainloop()