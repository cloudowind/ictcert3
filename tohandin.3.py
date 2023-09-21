#!/usr/bin/python3
import os 
import math
import sys
import fileinput
import pathlib
import datetime
import shutil
import smtplib
from pathlib import PurePath
from datetime import datetime
try: 
     from backupconfig import destinationDir
except:  
     userinputconfig = input("Config file does not exist ! do  you want to create one into the cwd ? (type 'yes' , or 'no:') ")
     if userinputconfig == "yes":
            print("creating config file into the current working directory...\n")
            #currentpath = os.getcwd()
            #fullpath = currentpath + "backupconfig.py"
            configdata = 'jobs = {"job700":"/home/ec2-user/environment/file1.txt","job1": "/home/ec2-user/environment/up.py"}\nthisDir = "config.py"\ndestinationDir = "backup"\nlogfile ="logfile.log"\nsmtp = {"sender": "3001724@students.sunitafe.edu.au","recipient": "onurcamlidag@gmail.com","server": "smtp.gmail.com","port":587,"user": "haydenstafe@gmail.com","password": "wcqdvocivbpoymaq"}'
            f = open("backupconfig.py","w")
            f.write(configdata)
            f.close()
     else :
         print("script cannot run without a config file ... sorry. "); sys.exit()
         

from backupconfig import jobs 
from backupconfig import destinationDir
from backupconfig import thisDir
from backupconfig import logfile ,smtp

def HandleError(errorMessage,currentime):
    print(errorMessage)
    writeLogMessage(errorMessage, currentime,False)
    sendEmail(errorMessage)
    sys.exit()

def sendEmail(message):
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject:Backup Error\n\n' + message + '\n'
     
    try:
        smtp_server = smtplib.SMTP(smtp["server"],smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login (smtp["user"],smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"],email)
        smtp_server.close()
    except Exception as error:
        print("Error while sending email ")

def writeLogMessage(logMessage,currentime,isSuccess):
    try :
        file = open(logfile,"a")

        if isSuccess:
            file.write(f"SUCCESS {currentime} {logMessage}\n")
            file.close()
            
        
        else:
            file.write(f"FAILURE {currentime}{logMessage}\n")
            file.close()
    except FileNotFoundError:
        print("ERROR :File does not exists")
    except IOError:
        print("file is not accesible")


def main():
 
    try:
        currentime = datetime.now().strftime("%Y%m%d-%H%M%S")
        argCount = len(sys.argv)
        #print(thisDir)
    
        if argCount < 2:
            HandleError("error:Job not specified",currentime)
        else:
          for jobname in sys.argv[1:]:
            if not(jobname in jobs):
                HandleError(f" Error : job {jobname} is not in job list",currentime)
                #print(f"Error: job: {jobname} is not in job list")
                
            jobsPath = jobs[jobname]
            print(jobsPath)
            if not os.path.exists(jobsPath):
               HandleError("Source doesn't exists", currentime)
               print("ERROR: file " +jobs[jobname]  + " does not exist to be backed up.")
       
     
        
      
            destDir=destinationDir
            print("destination directory:" + destinationDir)
            if not os.path.exists(destDir):
              print("ERROR: Backup  folder: " +destDir  + " unfortunetly does not exists")
              userinput = input("did you want to create one ? (type 'yes' , or 'no:') ")
              if userinput == "yes":
               newbackupPath = input("please specify the fullname to create in the current folder or the full path for thew new backup folder or just folder name for to be created into current folder: ")
               try:      os.mkdir(newbackupPath)
               except    (FileNotFoundError,FileExistsError) as err_o:
                    print("an error occured while trying to create the new back up folder maybe it already exists?but new directory name has been registered in config file ");HandleError("Destination doesn't exist and couldn't create one ", currentime); sys.exit()
               print("New Backup Directory "+newbackupPath+" has succesfully been created and registered in backupconfig.py... please re-run the script\n ")
               f = open("backupconfig.py",'r')
               filedata = f.read()
               f.close()
               newdata = filedata.replace(destDir,newbackupPath)
               f = open("backupconfig.py",'w')
               f.write(newdata)
               f.close()
              else:
                print("cannot prooced withouth a backup folder ") 
            else:
                 now = datetime.now() # current date and time
                 timestamp = now.strftime("%Y%m%d-%H%M%S")
                 print("timestamp:", timestamp)
                 srcPath = pathlib.PurePath(jobsPath)
                 destlock = destDir + "/" + srcPath.name + "-" + timestamp
            if pathlib.Path(jobsPath).is_dir():
                 
                try: shutil.copytree(jobsPath,destlock)
                except (FileNotFoundError,FileExistsError) as err_o: 
                      HandleError("an error happend while copying folder", currentime)
                      #failedentryD =  "from : " + jobsPath + "       to     :" + os.getcwd() + destlock+  "     :  Failed\n"  ; f = open("log.py","a") ; f.write(failedentryD); f.close(); print("File could not been copied, failure notice has been registered to logs and Admin has been alerted");sys.exit()
                Fdestlock=os.getcwd()+ "/" + destlock
                writeLogMessage(f"Backed up {jobsPath} to {Fdestlock}", currentime, True) 
                print("Folder has been backed up ")
                #logenteryD = "from : " + jobsPath +"        to:    " + os.getcwd()  + destlock+   "     :  Success\n"
                #try:    f = open("log.py",'a'); f.write(logenteryD);f.close()
                #except  (FileNotFoundError,FileExistsError) as err_o:
                     # print("log file could not been processed  but backing up has been accomplished "); sys.exit()
               
                 
            else :
        
                try: shutil.copy2(jobsPath,destlock)
                except (FileNotFoundError,FileExistsError) as err_o:
                     HandleError("an error happend while copying file", currentime)
                    
                    #failedentry =  "from :  " + jobsPath + "       to:      " + os.getcwd() + destlock+  "      :   Failed\n"  ; f = open("log.py","a") ; f.write(failedentry); f.close(); print("File could not been copied, failure notice has been registered to logs and Admin has been alerted");sys.exit()
                Ddestlock=os.getcwd()+ "/" +destlock
                writeLogMessage(f"Backed up {jobsPath} to {Ddestlock}", currentime, True) 
                print("file has been backuped up ")
                #logentry = "from : " + jobsPath +"        to     :" + os.getcwd()  + destlock+    "      :  Success\n"
                #try:      f = open("log.py",'a') ;   f.write(logentry) ; f.close()
                #except    (FileNotFoundError,FileExistsError) as err_o:
                 #   print("log file could not been processed  but backing up has been accomplished "); sys.exit()
            
             
    except:
        print("Very unexcepted error only")

if __name__ == '__main__':
    main()