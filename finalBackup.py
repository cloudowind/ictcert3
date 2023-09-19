#!/usr/bin/python3
import os 
import math
import sys
import fileinput
import pathlib
import datetime
import shutil
from pathlib import PurePath
from datetime import datetime
try: 
     from backupconfig import destinationDir
except:  
     userinputconfig = input("Config file does not exist ! do  you want to create one into the cwd ? (type 'yes' , or 'no:' ")
     if userinputconfig == "yes":
            print("creating config file into the current working directory...\n")
            #currentpath = os.getcwd()
            #fullpath = currentpath + "backupconfig.py"
            configdata = 'jobs = {"job700":"/home/ec2-user/environment/file1.txt","job1": "/home/ec2-user/environment/up.py"}\nthisDir = "config.py"\ndestinationDir = "backup"\nlogfile ="logfile.log"\n'
            f = open("backupconfig.py","w")
            f.write(configdata)
            f.close()
     else :
         print("script cannot run without a config file ... sorry. "); sys.exit()
         

from backupconfig import jobs 
from backupconfig import destinationDir
from backupconfig import thisDir


def main():
 
    try:
        argCount = len(sys.argv)
        #print(thisDir)
    
        if argCount !=2:
            print("ERROR JON NOT SPECIFIED")
        else:
            jobname = sys.argv[1]
            if not(jobname in jobs):
                print(f"Error: job: {jobname} is not in job list")
        print("hello")        
        jobsPath = jobs[jobname]
        print(jobsPath)
        if not os.path.exists(jobsPath):
           print("ERROR: file " +jobs[jobname]  + " does not exist to be backed up.")
       
        if os.path.isfile(jobsPath):
            print("it is a file")
        else:
            print("it is a folder")
        
      
        destDir=destinationDir
        print("destination directory:" + destinationDir)
        if not os.path.exists(destDir):
           print("ERROR: Backup  folder: " +destDir  + " unfortunetly does not exists")
           userinput = input("did you want to create one ? (type 'yes' , or 'no:' ")
           if userinput == "yes":
               newbackupPath = input("please specify the fullname to create in the current folder or the full path for thew new backup folder or just folder name for to be created into current folder: ")
               try:      os.mkdir(newbackupPath)
               except    (FileNotFoundError,FileExistsError) as err_o:
                    print("an error occured while trying to create the new back up folder maybe it already exists?but new directory name has been registered in config file "); sys.exit()
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
                      failedentryD =  "from : " + jobsPath + "       to     :" + os.getcwd() + destlock+  "     :  Failed\n"  ; f = open("log.py","a") ; f.write(failedentryD); f.close(); print("File could not been copied, failure notice has been registered to logs and Admin has been alerted");sys.exit()
                  
                 print("Folder has been backed up ")
                 logenteryD = "from : " + jobsPath +"        to:    " + os.getcwd()  + destlock+   "     :  Success\n"
                 try:    f = open("log.py",'a'); f.write(logenteryD);f.close()
                 except  (FileNotFoundError,FileExistsError) as err_o:
                      print("log file could not been processed  but backing up has been accomplished "); sys.exit()
               
                 
           else :
        
                try: shutil.copy2(jobsPath,destlock)
                except (FileNotFoundError,FileExistsError) as err_o:
                    failedentry =  "from :  " + jobsPath + "       to:      " + os.getcwd() + destlock+  "      :   Failed\n"  ; f = open("log.py","a") ; f.write(failedentry); f.close(); print("File could not been copied, failure notice has been registered to logs and Admin has been alerted");sys.exit()
                
                print("file has been backuped up ")
                logentry = "from : " + jobsPath +"        to     :" + os.getcwd()  + destlock+    "      :  Success\n"
                try:      f = open("log.py",'a') ;   f.write(logentry) ; f.close()
                except    (FileNotFoundError,FileExistsError) as err_o:
                    print("log file could not been processed  but backing up has been accomplished "); sys.exit()
            
             
    except:
        print("ERROR: hata")

if __name__ == '__main__':
    main()