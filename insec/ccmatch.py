#!/usr/bin/python3
import os
import sys
import csv
import shutil
from pathlib import Path

try:
    path_to_in = sys.argv[1]
    path_to_insec = sys.argv[2]
    path_to_out = sys.argv[3]
except IndexError:
    print("Usage: path/in path/insec path/to/out")
    sys.exit(1)
    
def dev_index():
	pathName="retdec/outhtml/"
	flagFindStart=0
	startHtml = ""
	bodyHtmlTmp=""
	countBody=0
	nameIndex=0
	endHtml="    </table> \n  </div>\n  </body>\n</html>"
	if Path(pathName+"index.html").stat().st_size>1000000:
		with open(pathName+"index.html") as f:
			for line in f:
				if flagFindStart==0 and not "</tr>" in line:
					startHtml +=line
					continue
				if flagFindStart==0:
					startHtml+="\n"+"</tr>"
					flagFindStart=1
					continue
				if countBody>1000:
					countBody=0
					nameIndex+=1
					with open(pathName+"index"+str(nameIndex)+".html","a") as fw:
						fw.write(startHtml)
						fw.write(bodyHtmlTmp)
						fw.write(endHtml)
					bodyHtmlTmp=""
				if not "</table>" in line:
					bodyHtmlTmp+=line
					if "</tr>" in line:
							countBody+=1
				else:
					nameIndex+=1
					with open(pathName+"index"+str(nameIndex)+".html","a") as fw:
						fw.write(startHtml)
						fw.write(bodyHtmlTmp)
						fw.write(endHtml)
					return None


def check_env(end_file,folder_name):

    file_name="noname"
    for file in os.listdir(folder_name):
        if file.endswith(end_file):
            file_name=file
    if file_name == "noname":
        print(end_file+" file not found")
        sys.exit()
    file_name=os.path.splitext(file_name)[0]
    return file_name

def down_git(lname,pname,rname,gcpar):
    foldname = "retdec"
    if os.path.exists(foldname):
        shutil.rmtree(foldname)
    if pname == "nonono":
        os.system("git clone "+gcpar+" https://github.com/"+lname+"/"+rname+".git "+foldname)
    else:
        os.system("git clone "+gcpar+" https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldname)


def gogo_cc(makeline,bl):
    foldname = "retdec"
    outhtml = "outhtml"
    ex1 = ". ~/codechecker/venv/bin/activate&&export PATH=~/codechecker/build/CodeChecker/bin:$PATH"
#    ex2 = "~/codechecker/build/CodeChecker/bin/CodeChecker check -b \""+bl+"\"   --enable-all --enable alpha --enable debug  -o ./reports"
#    ex3 = "~/codechecker/build/CodeChecker/bin/CodeChecker parse  -e html -o "+outhtml+" ./reports/"
    ex2 = "~/codechecker/build/CodeChecker/bin/CodeChecker check -b \""+bl+"\"  -o ./reports"
    ex3 = "~/codechecker/build/CodeChecker/bin/CodeChecker parse  -e html  ./reports/ -o ./"+outhtml
    cmd1 = "cd "+foldname+" && "+makeline
    #cmd11 = "cd "+foldname+" && autoreconf -vi && ./configure"
    cmd2 = "( cd "+foldname+" && "+ex1+" && "+ex2+" && "+ex3+" )"
    os.system(cmd1)
    #os.system(cmd11)
    os.system(cmd2)

def html_7z(lname,rname,upname,opath):    
    foldname = "retdec"  
    outhtml = "outhtml"
    dev_index()
    file7z = lname+"_"+rname + ".7z"  
    if os.path.exists(foldname+"/"+file7z):
        os.remove(foldname+"/"+file7z)
    cmdzip="cd "+foldname+" &&7z a -mhe=on "+file7z+" "+outhtml+" -p"+upname
    os.system(cmdzip)
    if os.path.exists(foldname+"/"+file7z):
        shutil.move(foldname+"/"+file7z, opath+file7z)


def save_repo(lname,pname,rname,ptout):
    os.system("git remote remove origin")
    os.system("git config --global user.name \""+lname+"\"")
    os.system("git config --global user.email "+lname+"@github.com")
    os.system("git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("git checkout master")
    os.system("git add "+ptout)
    os.system("git commit -m \"create 7z\"")
    os.system("git push origin master")





print("check env")    
unzip_name=check_env(".unzip",path_to_insec)
retpo_name=check_env(".repo",path_to_insec)
logi_name=check_env(".login",path_to_insec)
pass_name=check_env(".pass",path_to_insec)
#fretpo_name=check_env(".frepo",path_to_in)
flogi_name=check_env(".flogin",path_to_insec)
fpass_name=check_env(".fpass",path_to_insec)

#for test
#unzip_name="123"
#retpo_name="123"
#logi_name="123"
#pass_name="123"
##fretpo_name=check_env(".frepo",path_to_in)
#flogi_name="123"
#fpass_name="123"   





if os.path.exists(path_to_in+"list.ccmatch"):
    with open(path_to_in+"list.ccmatch") as f:
        content = f.readlines()
    makeline="./autogen.sh && ./configure"
    buildline="make"
    gitclonpar=""
    for i in content:
        if "sudo apt" in i:
            os.system(i)
            continue
        if "makeline " in i:
            makeline=i.split("makeline ")[1]
            continue
        if "buildline " in i:
            buildline=i.split("buildline ")[1]
            continue
        if "gitclonpar " in i:
            gitclonpar=i.split("gitclonpar ")[1]
            continue
        rname = i.split('/')[-1].split(".git")[0]
        lname = i.split('/')[-2]
        if lname== flogi_name:
            pname = fpass_name
        else:
            pname="nonono"
        down_git(lname,pname,rname,gitclonpar)        
        gogo_cc(makeline,buildline)        
        makeline="./autogen.sh && ./configure"
        buildline="make"
        html_7z(lname,rname,unzip_name,path_to_out)        
        save_repo(logi_name,pass_name,retpo_name,path_to_out)
else:
    print("NO LIST.ccMATCH FILE")
    sys.exit()
