import tkinter
from tkinter import filedialog
from ctypes import windll
from PIL import Image
import frame
import controlwindow

import threading
import time

class Win(tkinter.Tk):
    basefilepath = ''
    ind = 0
    filepath = './default.gif'    
    label = None
    frames=[]
    frameCnt = 40
    width='500'
    height='500'
    _offsetx = None
    _offsety = None

    def __init__(self,master=None):
        tkinter.Tk.__init__(self,master)

        self.title("Kim's Simple Widget")
        self.iconbitmap("./iconforsticker.ico")
        self.wm_attributes("-transparent", "white")
        self.configure(bg='')
        self.overrideredirect(True)

        self.label = tkinter.Label(self, bg='white')
        self.label.pack()   

        #add menu
        menubar = tkinter.Menu(self)
        menubar.add_command(label="Open", command=self.openimage)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="Exit", command=self.quit)

        self.setconfigure()
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self.bind("<Button-3>", lambda event: menubar.post(event.x_root, 
        event.y_root))

    def _set_window(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        self.wm_withdraw()
        self.after(0, lambda: self.wm_deiconify())
    
    # Move Sticker
    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

    # Handle File
    def setconfigure(self):
        try:
            f = open("./window.conf","r")
            # get last position
            line = f.readline()
            strs = line.split(',')
            
            self._offsetx=strs[0]
            self._offsety=strs[1][:-1]

            # get last image
            line = f.readline()
            self.filepath = line
            try:
                img = Image.open(self.filepath)
                self.width= str(img.size[0])
                self.height = str(img.size[1])
                self.geometry(self.width+"x"+self.height+"+"+self._offsetx+"+"+self._offsety)
                
                if self.filepath.endswith('gif'):
                    self.frameCnt = frame.get_frameCnt(img)
                    frame.process_frame(img, self.filepath)
                    self.frames = [tkinter.PhotoImage(file=self.filepath,format = 'gif -index %i' %(i))
                        for i in range(self.frameCnt)]
                    self.after(0, self.update, self.frames, 0, self.label)
                
                else:
                    frame.process_frame(img, self.filepath)
                    self.after(0, self.update, tkinter.PhotoImage(file=self.filepath), 0, self.label)

            except:
                print("no configuration")
                self.openimage()
        except:
            f = open("./window.conf","w")
            f.close()
            self.openimage()

    def openimage(self):
        self.frames.clear()

        self.filepath = filedialog.askopenfilename(
            initialdir='./gif',title='파일선택', filetypes=(('gif files','*.gif'),('all files','*.*')))        
        img = Image.open(self.filepath)
        self.width= str(img.size[0])
        self.height = str(img.size[1])
        self.geometry(self.width+"x"+self.height)
        if self.filepath.endswith('gif'):
            self.frameCnt = frame.get_frameCnt(img)
            frame.process_frame(img, self.filepath)
            self.frames = [tkinter.PhotoImage(file=self.filepath,format = 'gif -index %i' %(i))
                for i in range(self.frameCnt)]
        
            self.after(0, self.update, self.frames, 0, self.label)
        else:
            print("test line")
            frame.process_frame(img, self.filepath)
            self.after(0, self.update, tkinter.PhotoImage(file=self.filepath), 0, self.label)
    
    def save(self):
        with open("./window.conf","w") as conf:
            conf.write(str(self._offsetx)+','+str(self._offsety)+'\n')
            conf.write(self.filepath)
 
    def update(self, frames, ind, label):

        if self.filepath.endswith('gif'):
            frame = frames[ind]
            ind = (ind + 1)%(self.frameCnt)
            label.configure(image=frame)
            self.after(100, self.update, frames, ind, label)
        else:
            label.configure(image=frames)
            self.after(1000000, self.update, frames, 0, label)

    # Exit
    def quit(self):
        self.destroy()

def main():
    win = Win()
    win.after(0, win._set_window)
    win.mainloop()

def wincontroller():
    time.sleep(5)
    controlwindow.getWindow()

if __name__=="__main__":
    print("Kim's Simple Widget")
    controlTh = threading.Thread(target=wincontroller, daemon=True)
    controlTh.start()

    main()


    

