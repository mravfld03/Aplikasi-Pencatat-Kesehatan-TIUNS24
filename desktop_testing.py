import tkinter as tk
import tkinter.messagebox as msgbox

def main():
    mainWindow = tk.Tk()
    mainWindow.title("Program Utama")
    
    def btnSalamClick(*args):
        msgbox.showinfo("New Message", "Hallo, Selamat siang")
        
    # membuat tombol
    # cara 1 
    btnExit = tk.Button(mainWindow, command=mainWindow.destroy)
    btnExit['text'] = "Keluar"
    btnExit.pack()
    
    # cara 2
    btnSalam = tk.Button(mainWindow, text="Salam")
    btnSalam.pack()
    btnSalam.bind('<Button-1>', btnSalamClick)
    
    # txtNim
    
    mainWindow.mainloop()

if __name__ == "__main__":
    main()