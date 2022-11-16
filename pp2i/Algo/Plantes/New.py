import sqlite3
import re
from PyPDF2 import PdfReader

reader = PdfReader("Compagnonnage.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

text=text.replace("Bruxelles","bruxelles")
text=text.replace("fraise","fraisier")

pattern = r'\n'
d = re.split(pattern,text)

document =  []
current_line = []
for i in d:
    if re.match(r'[A-Z].*',i):
        document.append(current_line)
        current_line=[]
    current_line.append(i)
document.append(current_line)

for line in document:
    if re.match(r'(\s)+',line[0]):
        document.remove(line)
    if re.match(r'.*\s(et)\s.*',line[0]):
        document.remove(line)

new_doc=[]
new_line=[]
for line in document:
    new_line=re.split(r'(\s\s)',line[0])
    for i in range(1,len(line)):
        new_line.append(line[i])
    for i in new_line:
        if re.match(r'(\s)+',i):
            new_line.remove(i)
    new_doc.append(new_line)
    new_line=[]
document=new_doc

new_doc=[]
new_line=[]
for line in document:
    new_line.append(line[0])
    element=''
    for i in range(1,len(line)):
        element+=line[i]
    new_line.append(element)
    new_doc.append(new_line)
    new_line=[]
document=new_doc

new_doc=[]
new_line=[]
for line in document:
    new_line=re.split(r'(\s\s)',line[1])
    new_line.append(line[0])
    for i in new_line:
        if re.match(r'(\s)+',i):
            new_line.remove(i)
        elif i=='':
            new_line.remove(i)
    new_doc.append(new_line)
    print(len(new_line))
    new_line=[]
document=new_doc



data = sqlite3.connect("Test_DB.db")

def new_value(type,plante1,plante2=1):
    if type=="plante":
        cur = data.cursor()
        cur.execute("select id from plantes where nom like ?",(plante1,))
        if cur.fetchall()==[]:
            cur.execute("insert into plantes (id,nom) values(1+(select max(id) from plantes),?)",(plante1,))
            data.commit()
    elif type=="compagnon":
        cur = data.cursor()
        cur.execute("select id from plantes where nom like ?",(plante1,))
        for i in cur.fetchall():
            id1=i[0]
        cur.execute("select id from plantes where nom like ?",(plante2,))
        for i in cur.fetchall():
            id2=i[0]
        cur.execute("select plante1 from compagnons where plante1 like ? and plante2 like ?",(min(id1,id2),max(id1,id2)))
        if cur.fetchall()==[]:
            cur.execute("""insert into compagnons values(?,?);""",(min(id1,id2),max(id1,id2)))
            data.commit()
    elif type=="ennemi":
        cur = data.cursor()
        cur.execute("select id from plantes where nom like ?",(plante1,))
        for i in cur.fetchall():
            id1=i[0]
        cur.execute("select id from plantes where nom like ?",(plante2,))
        for i in cur.fetchall():
            id2=i[0]
        cur.execute("select plante1 from ennemis where plante1 like ? and plante2 like ?",(min(id1,id2),max(id1,id2)))
        if cur.fetchall()==[]:
            cur.execute("""insert into ennemis values(?,?);""",(min(id1,id2),max(id1,id2)))
            data.commit()

#a="Asperge"
#b="Oignon"
#new_value("plante",a)
#new_value("plante",b)
#new_value("compagnon",a,b)
#new_value("ennemi",a,b)