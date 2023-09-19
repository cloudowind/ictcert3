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
try: from backupconfig import jobs 
except : print("error modl")
from backupconfig import destinationDir
from backupconfig import thisDir

def main():
 
 
    try:
        argCount = len(sys.argv)
        print(thisDir)
    
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
        
        print("outside")
        destDir=destinationDir
        print(destinationDir)
        if not os.path.exists(destDir):
           print("ERROR: Backup  folder: " +destDir  + " unfortunetly does not exists")
           userinput = input("did you want to create one ? (type 'yes' , or 'no:' ")
           if userinput == "yes":
               newbackupPath = input("please specify the fullname to create in the current folder or the full path for thew new backup folder or just folder name for to be created into current folder: ")
               os.mkdir(newbackupPath)
               print("New Backup Directory "+newbackupPath+" has succesfully been created and registered in backupconfig.py... please re-run the script\n ")
               f = open("backupconfig.py",'r')
               filedata = f.read()
               f.close()
               newdata = filedata.replace(destDir,newbackupPath)
               f = open("backupconfig.py",'w')
               f.write(newdata)
               f.close()
               
        else:
     
           now = datetime.now() # current date and time
           timestamp = now.strftime("%Y%m%d-%H%M%S")
           print("timestamp:", timestamp)
           srcPath = pathlib.PurePath(jobsPath)
           destlock = destDir + "/" + srcPath.name + "-" + timestamp
           if pathlib.Path(jobsPath).is_dir():
               shutil.copytree(jobsPath,destlock)
           else :
               shutil.copy2(jobsPath,destlock)
               print("copying")
    except:
        print("ERROR: hata")

if __name__ == '__main__':
    main()