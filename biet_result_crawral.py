from tkinter import *
from tkinter import messagebox as tkMessageBox
from function2 import *


class result:
    
    def __init__(self,master):
        self.master=master
        master.title('BIET RESULT')
        self.W=master.winfo_screenwidth()
        self.H=master.winfo_screenheight()
        dim = str(self.W)+'x'+str(self.H)
        self.master.geometry(dim)
        self.frame     = Frame(master,width=self.W,height= self.H,bg="#246583")
        self.frame1    = Frame(self.frame,width=self.W, height = self.H/8,bg='#246583')
        self.frame2    = Frame(self.frame,width=self.W-100, height = 7*self.H/8,bg='#FFFFFF')
        f21H           = (4*self.H/16)
        f21W           = (self.W/4)
        self.frame21   = Frame(self.frame2,width=f21W, height = f21H,bg='#FFF7F7',highlightbackground="#246583", highlightcolor="green", highlightthickness=3)
        self.frame211  = Frame(self.frame21,width=f21W-6, height = f21H/5,bg='#FFF7F7')
        self.frame2111 = Frame(self.frame211,width=3*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame2112 = Frame(self.frame211,width=5*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame212  = Frame(self.frame21,width=f21W-6, height = f21H/5,bg='#FFF7F7')
        self.frame2121 = Frame(self.frame212,width=3*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame2122 = Frame(self.frame212,width=5*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame213  = Frame(self.frame21,width=f21W-6, height = f21H/5,bg='#FFF7F7')
        self.frame2131 = Frame(self.frame213,width=3*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame2132 = Frame(self.frame213,width=5*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame214  = Frame(self.frame21,width=f21W-6, height = f21H/5,bg='#FFF7F7')
        self.frame2141 = Frame(self.frame214,width=3*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame2142 = Frame(self.frame214,width=5*f21W/8, height = f21H/5,bg='#FFF7F7')
        self.frame215  = Frame(self.frame21,width=f21W-6, height = f21H/5-6,bg='#FFF7F7')

        self.frame.place(x=0,y=0)
        self.frame1.place(x=0,y=0)
        self.frame2.place(x=20,y=self.H/8)
        self.frame21.place(x=self.W/2-self.W/8,y=10)
        self.frame211.place(x=0,y=0)
        self.frame2111.place(x=0,y=0)
        self.frame2112.place(x=3*f21W/8,y=0)
        self.frame212.place(x=0,y=f21H/5)
        self.frame2121.place(x=0,y=0)
        self.frame2122.place(x=3*f21W/8,y=0)
        self.frame213.place(x=0,y=f21H*2/5)
        self.frame2131.place(x=0,y=0)
        self.frame2132.place(x=3*f21W/8,y=0)
        self.frame214.place(x=0,y=f21H*3/5)
        self.frame2141.place(x=0,y=0)
        self.frame2142.place(x=3*f21W/8,y=0)
        self.frame215.place(x=0,y=f21H*4/5)

        self.L1 = Label(self.frame2111, text="Academic Session",bg='#FFF7F7',fg='#0c3e74',font='Symbol 11 bold').place(x=10,y=f21H/15)
        self.L2 = Label(self.frame2121, text="Semester",bg='#FFF7F7',fg='#0c3e74',font='Symbol 11 bold').place(x=10,y=f21H/15)
        self.L3 = Label(self.frame2131, text='Result Category',bg='#FFF7F7',fg='#0c3e74',font='Symbol 11 bold').place(x=10,y=f21H/15)
        self.L4 = Label(self.frame2141, text='Branch',bg='#FFF7F7',fg='#0c3e74',font='Symbol 11 bold').place(x=10,y=f21H/15)
        
        
        self.choice  = {'2018-2019','2017-2018','2016-2017','2015-2016','2014-2015','2013-2014','2012-2013'}
        self.session = StringVar(self.frame2112)
        self.session.set('--Select--')
        self.sessionMenu = OptionMenu(self.frame2112, self.session, *sorted(self.choice,reverse=True))
        self.sessionMenu.place(x=0,y=f21H/20)
        self.sessionMenu.config(bg = "#f2f1f0",width = int(f21W/14),font='Symbol 10 bold')

        self.choice = {1,2,3,4,5,6,7,8}
        self.sem    = StringVar(self.frame2122)
        self.sem.set('--Select--')
        self.semMenu = OptionMenu(self.frame2122, self.sem, *sorted(self.choice))
        self.semMenu.place(x=0,y=f21H/20)
        self.semMenu.config(bg = "#f2f1f0",width = int(f21W/14),font='Symbol 10 bold')

        
        self.choice = {'Regular/Readmitted','Carry Over','Ex-Student','Special Carry Over'}
        self.categ  = StringVar(self.frame2132)
        self.categ.set('--Select--')
        self.categMenu = OptionMenu(self.frame2132, self.categ, *sorted(self.choice))
        self.categMenu.place(x=0,y=f21H/20)
        self.categMenu.config(bg = "#f2f1f0",width = int(f21W/14),font='Symbol 10 bold')

        
        self.choice = {'All','Computer Science & Engineering','Electrical Engineering','Electronics & Communication Engineering','Civil Engineering','Chemical Engineering','Mechanical Engineering','Information & Technology'}
        self.branch = StringVar(self.frame2142)
        self.branch.set('--Select--')
        self.branchMenu = OptionMenu(self.frame2142, self.branch, *sorted(self.choice))
        self.branchMenu.place(x=0,y=f21H/20)
        self.branchMenu.config(bg = "#f2f1f0",width = int(f21W/14),font='Symbol 10 bold')
        
        
        self.sub=Button(self.frame215,text='Submit',width=14,bg='#f3f3f3',fg='#0c3e74',font='Symbol 11 bold',relief=FLAT,command=lambda: self.Submit()).place(x=(f21W/2-25),y=10)
    
    def Submit(self):
        create_result(self.session.get(),self.sem.get(),self.categ.get(),self.branch.get())
        tkMessageBox.showinfo("Done")

if __name__ == '__main__':
    root= Tk()
    mygui=result(root)
    root.mainloop()


