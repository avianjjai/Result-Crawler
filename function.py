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
    return str(int(session[2:4])-(int(sem)-1)//2)+'043'+branch_Code[branch]+'001' if linear == True else str(int(session[2:4])-(int(sem)-1)//2+1)+'043'+branch_Code[branch]+'901'

def create_File_Name(info):
    return info['Roll No']+' '+info['Name']+'.csv'

def evenSemester(r):            
    r = r.find('td',class_='cntr')
    
    p = []
    for i in r.table.find_all('tr')[3].find_all('tr'):
        temp = []
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)
    
    temp = []
    for j in r.table.find_all('tr')[9].find_all('td'):
        temp.append(j.text.strip())
    p.append(temp)
    
    temp = []
    for j in r.table.find_all('tr')[10].find_all('td'):
        temp.append(j.text.strip())
    p.append(temp)

    for i in r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResult').find_all('tr'):
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

    p.append([r.select_one('#ctl00_ContentPlaceHolder1_eSem').text.strip()])

    t = []
    for j in temp[5].find_all('td'):
        t.append(j.text.strip())
    
    for i in range(len(t)):
        if t[i]==':':
            info[t[i-1]]=t[i+1]
    p.append(t)

    t = []
    for j in temp[7].find_all('td'):
        t.append(j.text.strip())
    
    for i in range(len(t)):
        if t[i]==':':
            info[t[i-1]]=t[i+1]
    p.append(t)

    for i in r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResulte').find_all('tr'):
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
        
        for i in range(len(t)):
            if t[i]==':':
                info[t[i-1]]=t[i+1] 
        p.append(t)

    data = []
    for x in p:
        data.append(','.join(x))
    return data,info
    
def oddSemester(r):
    r = r.find('td',class_='cntr')
    p = []
    for i in r.table.find_all('tr')[4:14]:
        temp = []
        for j in i.find_all('td'):
            temp.append(j.text.strip())
        p.append(temp)

    info = {}    
    for x in p:
        for i in range(len(x)):
            if x[i]==':':
                info[x[i-1]]=x[i+1]


    for i in r.find('table',id = 'ctl00_ContentPlaceHolder1_grdResult').find_all('tr'):
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
    
    

def create_result(session,sem,categ,BRANCH):
    website = "http://www.bietjhs.ac.in/studentresultdisplay/frmprintreport.aspx"
    if BRANCH == 'All':
        directory = session+'|'+sem+ '|'+'ALL'+'|'+categ.replace('/',' ')
    else:
        directory = session+'|'+sem+ '|'+BRANCH[:5]+'|'+categ.replace('/',' ')
    create_result_dir(directory)
    all_result = directory + '/' + 'Complete.csv'
    data = {  
        "ctl00$ContentPlaceHolder1$ddlAcademicSession"  :  session,
        "ctl00$ContentPlaceHolder1$ddlSem"              :  sem,
        "ctl00$ContentPlaceHolder1$ddlResultCategory"   :  category_Code[categ],
        "ctl00$ContentPlaceHolder1$cmdPrintTR"          :  "View"
    }
    
    information = []
    if int(sem)%2 == 0:
        head = 'Roll No,Name,Year Total,Marks Obtained,First Year,Second Year,Third Year,Fourth Year,Grant Total,Division,Carry Paper'
    else:
        head = 'Roll No,Name,Marks Obtained,Result,Carry Papers'
    with open(all_result,'w') as f:
            f.write(head+'\n')
    if BRANCH == 'All':
        branch_Code_items = branch_Code
    else:
        branch_Code_items = {BRANCH:branch_Code[BRANCH]}
    
    for branch in branch_Code_items.items():
        roll_No = Create_RollNo(session,sem,branch[0])
        flag = 0
        linear = True
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
                	roll_No = Create_RollNo(session,sem,branch[0],False)
                	linear = False
                	flag = 0
                	continue
                break
            
            if result_page.find_all('td',class_='message')[0].text=='Result Not Declare; Contact to COE Office':
                flag += 1
                roll_No = str(int(roll_No)+1)
                continue
                
            flag = 0
            print(branch[0],'  ',roll_No,'.....')
            if int(sem)%2 == 0:
                result,info = evenSemester(result_page)
            else:
                result,info = oddSemester(result_page)
            
            if BRANCH != 'All':
                file = create_File_Name(info)
                create_result_file(directory,file,result)
            
            
            if int(sem)%2==0:
                t = info['Roll No'] + ',' + info['Name'] + ',' + info['Year Total'] + ',' + info['Marks Obtained'] + ',' + info['First Year'] + ',' + info['Second Year'] + ',' + info['Third Year'] + ',' + info['Fourth Year'] + ',' + info['Grant Total'] + ',' + info['Division'] + ',' + info['Carry Paper'].replace(',','|')
            else:
                t = info['Roll No'] + ',' + info['Name'] + ',' + info['Marks Obtained'] + ','  + info['Result'] + ',' + info['Cary Paper'].replace(',','|')
            information.append(list(t.split(',')))
            roll_No = str(int(roll_No)+1)
            
    t = []
    information.sort(key = lambda x:int(x[2].split('/')[0]),reverse = True)
    for x in information:
        t.append(str(','.join(x)))
        	
    with open(all_result,'a') as f:
        for x in t:
            f.write(x+'\n')

