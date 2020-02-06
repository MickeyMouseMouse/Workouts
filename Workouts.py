from tkinter import Tk, Label, Button, Entry, Toplevel, Menu, font
import webbrowser # for open GitHub
import time

class App():
    global minutesEnd, secondsEnd, mode
    mode = -1 # -1 = timer off; 0 = workout (timer on); 1 = relax (timer on)
    
    def __init__(self):
        # main-window
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.wm_geometry("+%d+%d" % 
                   ((self.window.winfo_screenwidth() - self.window.winfo_reqwidth()) / 3, 
                    (self.window.winfo_screenheight() - self.window.winfo_reqheight()) / 3))
        self.window.geometry("490x280")
        self.window.title("Workouts")
        
        # label with current time
        self.labelCurrentTime = Label(font = ("", 25), pady = 5)
        self.labelCurrentTime.grid(row = 0, column = 0, columnspan = 4)
        
        self.label1 = Label(self.window, text = "Number of minutes for workout:", anchor= 'w', width = 23)
        self.label1.grid(row = 1, column = 0)        
        self.entryMinutesForWork = Entry(self.window, width = 2)
        self.entryMinutesForWork.insert(0, "5")
        self.entryMinutesForWork.grid(row = 1, column = 1)
        
        self.label2 = Label(self.window, text = "Number of seconds for workout:", anchor= 'w', width = 23)
        self.label2.grid(row = 1, column = 2)          
        self.entrySecondsForWork = Entry(self.window, width = 2)
        self.entrySecondsForWork.insert(0, "0")
        self.entrySecondsForWork.grid(row = 1, column = 3)

        self.label3 = Label(self.window, text = "Number of minutes for relax:", anchor= 'w', width = 23)
        self.label3.grid(row = 2, column = 0) 
        self.entryMinutesForRelax = Entry(self.window, width = 2)
        self.entryMinutesForRelax.insert(0, "5")
        self.entryMinutesForRelax.grid(row = 2, column = 1)
        
        self.label4 = Label(self.window, text = "Number of seconds for relax:", anchor= 'w', width = 23)
        self.label4.grid(row = 2, column = 2) 
        self.entrySecondsForRelax = Entry(self.window, width = 2)
        self.entrySecondsForRelax.insert(0, "0")
        self.entrySecondsForRelax.grid(row = 2, column = 3)
        
        # start/stop
        self.buttonStart = Button(self.window, text = "Start", font = ("", 20), pady = 10)
        self.buttonStart.grid(row = 3, column = 0, columnspan = 4)
        self.buttonStart.bind("<Button-1>", self.startStop)  
        
        # timer
        self.labelTimer = Label(text = "Press Start", font = ("", 70), pady = 15)
        self.labelTimer.grid(row = 4, column = 0, columnspan = 4)
        
        # settings menu bar   
        menubar = Menu()
        self.window.config(menu = menubar)
        
        fileMenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "About Minesweeper", command = self.aboutApp)
        fileMenu.add_separator()
        fileMenu.add_command(label = "Exit", command = exit)
        
        self.startTimer()
        
        self.window.mainloop()

    # about-window  
    def aboutApp(self):
        # creation about-window if there is not
        if self.window.winfo_children().__len__() == 12:
            aboutWindow = Toplevel(self.window)
            aboutWindow.title("About Workouts")
            aboutWindow.geometry("260x120")
            aboutWindow.resizable(False, False)
            aboutWindow.wm_geometry("+%d+%d" % 
                                      ((aboutWindow.winfo_screenwidth() / 2 - aboutWindow.winfo_reqwidth()), 
                                       (aboutWindow.winfo_screenheight() / 2 - aboutWindow.winfo_reqheight())))
            
            _ = Label(aboutWindow, text = "Workouts by Andrew Jeus", font=("", 18)).grid(row = 0, column = 0, padx = 10, pady = 10)
            _ = Label(aboutWindow, text = "Version 1.0 (14 July 2019)", font=("", 18)).grid(row = 1, column = 0)
            labelInfo3 = Label(aboutWindow, text = "View code in GitHub", font=("", 14))
            labelInfo3.grid(row = 2, column = 0, padx = 5, pady = 5)
            
            # my font for link to GitHub
            myfont = font.Font(labelInfo3, labelInfo3.cget("font"))
            myfont.configure(underline = True)
            labelInfo3.configure(font = myfont)
            
            labelInfo3.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/MickeyMouseMouse/Workouts"))

    def startTimer(self):
        global minutesEnd, secondsEnd, mode
        
        # update current time
        self.labelCurrentTime.config(text = time.strftime("%H:%M:%S", time.localtime()))
        
        if mode != -1:
            tmpSeconds = secondsEnd - int(time.strftime("%S", time.localtime()))
            tmpMinutes = minutesEnd - int(time.strftime("%M", time.localtime()))
            
            if tmpSeconds == 0 and tmpMinutes == 0:
                if mode == 0:
                    mode = 1
                else:
                    mode = 0
                    
                self.setEndTime()    
            
            if tmpSeconds < 0:
                tmpSeconds = secondsEnd + (60 - int(time.strftime("%S", time.localtime())))
                tmpMinutes -= 1
                
            if tmpMinutes < 0:
                tmpMinutes = minutesEnd + (60 - int(time.strftime("%M", time.localtime())))                    
            
            self.labelTimer.config(text = tmpMinutes.__str__() + " : " + tmpSeconds.__str__())    
        
        # repeat this function after 1 second
        self.window.after(1000, self.startTimer)
    
    def setEndTime(self):
        global secondsEnd, minutesEnd, mode
        
        secondsEnd = int(time.strftime("%S", time.localtime()))
        minutesEnd = int(time.strftime("%M", time.localtime()))

        if mode == 0:
            secondsEnd += int(self.entrySecondsForWork.get())
            minutesEnd += int(self.entryMinutesForWork.get())
            
            self.labelTimer.config(fg = "red")
        else:
            secondsEnd += int(self.entrySecondsForRelax.get())
            minutesEnd += int(self.entryMinutesForRelax.get())  
            
            self.labelTimer.config(fg = "green")                          

        if secondsEnd >= 60:
            secondsEnd %= 60
            minutesEnd += 1
            
        if minutesEnd >= 60:
            minutesEnd %= 60       
    
    # checking the correctness of the input values
    def isInputCorrect(self):
        if not (self.entryMinutesForWork.get().isdigit() 
                and int(self.entryMinutesForWork.get()) in range(60)): return False
        if not (self.entrySecondsForWork.get().isdigit() 
                and int(self.entrySecondsForWork.get()) in range(60)): return False
        if not (self.entryMinutesForRelax.get().isdigit() 
                and int(self.entryMinutesForRelax.get()) in range(60)): return False
        if not (self.entrySecondsForRelax.get().isdigit() 
                and int(self.entrySecondsForRelax.get()) in range(60)): return False
        
        if (self.entryMinutesForWork.get() == "0" and self.entrySecondsForWork.get() == "0"
            and self.entryMinutesForRelax.get() == "0" and self.entrySecondsForRelax.get() == "0"): 
            return False
                                                        
        return True

    # start/stop timer
    def startStop(self, _):
        global mode
        
        if mode == -1:
            if self.isInputCorrect():
                mode = 0
                self.buttonStart.config(text = "Stop")
                self.labelTimer.config(text = "")   
                self.setEndTime()
            else:
                self.entryMinutesForWork.delete(0, 'end')
                self.entrySecondsForWork.delete(0, 'end')
                self.entryMinutesForRelax.delete(0, 'end')
                self.entrySecondsForRelax.delete(0, 'end')
                
                self.labelTimer.config(text = "Incorrect Input")    
        else:
            mode = -1
            self.buttonStart.config(text = "Start")         
            self.labelTimer.config(fg = "black")  
            self.labelTimer.config(text = "Press Start")  
           
app = App()