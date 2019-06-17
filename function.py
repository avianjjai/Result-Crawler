from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox as tkMessageBox
from bs4 import BeautifulSoup as soup
import requests
import os

branch_Code = {
    'Computer Science & Engineering':'10',
    'Electrical Engineering':'20',
    'Electronics & Communication Engineering':'31',
    'Civil Engineering':'00',
    'Chemical Engineering':'51',
    'Mechanical Engineering':'40',
    'Information & Technology':'13'
}

category_Code = {
    'Regular/Readmitted' : 'R',
    'Carry Over' : 'C',
    'Ex-Student' : 'E',
    'Special Carry Over' : 'S'
}

def create_result_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        


def create_result_file(directory,file_name,result):
    file = directory+'/'+file_name
    if not os.path.isfile(file):
        with open(file,'w') as f:
            for x in result:
                f.write(x+'\n')




def Create_RollNo(session,sem,branch,linear=True):
    if linear == True:
        return str(int(session[2:4])-(int(sem)-1)//2)+'043'+branch_Code[branch]+'001'
    else:
        return str(int(session[2:4])-(int(sem)-1)//2+1)+'043'+branch_Code[branch]+'901'



def create_File_Name(info):
    return info['Roll No']+' '+info['Name']+'.csv'



def evenSemester(r):            
    r = r.find('td',class_='cntr')
    p = []
    R1 = r.table.find_all('tr')[3]

    for i in R1.find_all('tr'):
        temp = []
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)

    R1 = r.table.find_all('tr')[9]
    temp = []
    for j in R1.find_all('td'):
        temp.append(j.text.strip())
    p.append(temp)

    R1 = r.table.find_all('tr')[10]
    temp = []
    for j in R1.find_all('td'):
        temp.append(j.text.strip())
    p.append(temp)

    R1 = r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResult')
    for i in R1.find_all('tr'):
        temp = []
        for j in i.find_all('th'):
            temp.append(j.text.strip())
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)

    info = {}    
    for x in p:
        for i in range(len(x)):
            if x[i]==':':
                info[x[i-1]]=x[i+1]

    temp = []
    for tag in r.table.tr.next_siblings:
        temp.append(tag)

    R1 = r.select_one('#ctl00_ContentPlaceHolder1_eSem')
    p.append([R1.text.strip()])

    t = []
    for j in temp[5].find_all('td'):
        t.append(j.text.strip())
    p.append(t)

    t = []
    for j in temp[7].find_all('td'):
        t.append(j.text.strip())
    p.append(t)

    R1 = r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResulte')
    for i in R1.find_all('tr'):
        t = []
        for j in i.find_all('th'):
            t.append(j.text.strip())
        for j in i.find_all('td'):
            t.append(j.text.strip())
        p.append(t)

    for i in range(11,20,2):
        t = []
        for j in temp[i].find_all('td'):
            t.append(j.text.strip())
        p.append(t)

    data = []

    for x in p:
        data.append(','.join(x))
    return data,info
    


def oddSemester(r):
    r = r.find('td',class_='cntr')
    p = []
    R1 = r.table.find_all('tr')[4:14]
    for i in R1:
        temp = []
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)

    info = {}    
    for x in p:
        for i in range(len(x)):
            if x[i]==':':
                info[x[i-1]]=x[i+1]


    R1 = r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResult')
    for i in R1.find_all('tr'):
        temp = []
        for j in i.find_all('th'):
            temp.append(j.text.strip())
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)

    data = []
    for x in p:
        data.append(','.join(x))
    return data,info
    
    


def create_result(session,sem,categ,branch):
    website = "http://www.bietjhs.ac.in/studentresultdisplay/frmprintreport.aspx"
    directory = session+'|'+sem+ '|'+branch[:5]+'|'+categ.replace('/',' ')
    create_result_dir(directory)
    roll_No = Create_RollNo(session,sem,branch)
    flag = 0
    linear = True
    
    data = {  
        "ctl00$ContentPlaceHolder1$ddlAcademicSession"  :  session,
        "ctl00$ContentPlaceHolder1$ddlSem"              :  sem,
        "ctl00$ContentPlaceHolder1$ddlResultCategory"   :  category_Code[categ],
        "ctl00$ContentPlaceHolder1$cmdPrintTR"          :  "View"
    }
    
    while True:
        page = requests.get(website)
        s = soup(page.content,"html.parser")
        data["__VIEWSTATE"]                         = s.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"]                = s.select_one("#__VIEWSTATEGENERATOR")["value"]
        data["__EVENTVALIDATION"]                   = s.select_one("#__EVENTVALIDATION")["value"]
        data["ctl00$ContentPlaceHolder1$txtRollno"] = roll_No
        result_page = requests.post(website,data= data)
        result_page = soup(result_page.content,"html.parser")
        
        if flag >5:
            if int(sem)>2 and linear:
            	roll_No = Create_RollNo(session,sem,branch,False)
            	linear = False
            	flag = 0
            	continue
            break
        
        if result_page.find_all('td',class_='message')[0].text=='Result Not Declare; Contact to COE Office':
            flag += 1
            roll_No = str(int(roll_No)+1)
            continue
            
        flag = 0
        
        if int(sem)%2 == 0:
            result,info = evenSemester(result_page)
        else:
            result,info = oddSemester(result_page)
        file = create_File_Name(info)
        create_result_file(directory,file,result)
        roll_No = str(int(roll_No)+1)

