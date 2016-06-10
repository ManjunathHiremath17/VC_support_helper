#---------------------------------------------------------------------------------------
#
#                                      HELP
#
#---------------------------------------------------------------------------------------
#
#  Syntax to execute the script : python VC_support_helper.py 
#
#---------------------------------------------------------------------------------------
#  Uses of VC_support_helper.py
#  1. It decopmresses all the compressed files present in vCenter log.
#  2. If user wants to fetch logs that are only captured between time T1 and T2, it can be done using this script
#  3. Using this script, one can only fetch the logs he/she wishes to.
#  4. This script reads content of .gz file without decompressing the .gz files which saves space.
#  5. You can choose your own list of log files you want to capture the logs of.
#  6. If you are not sure in which log file (Like vmkernel.log or vmkernel.0 or vmkernel.1) the log is captured between specified times,
#    you can just mention "vmkernerl" in the list while enterring the list of logs to capture. It searches all vmkernel* files for specified
#    specified log and store the results.
#  7. The script also fetches the buildinfos of all products that are part of vc-support log. It helps in filing the bug. 
#  
#---------------------------------------------------------------------------------------


# Modules
import zipfile
import tarfile
import os.path
import os
import time
import os, fnmatch
import re
import gzip

print("\nThis is the helper tool for VC support files. It accepts vmware VC support file and extracts all its contents.\nAlso, if user wants to capture only logs that have been captured between time X and Y , it can be done with this tool\n")
# Variables

Log_files = ['vvold','vmkernel.log','vpxa.log','hostd.log','sps.log','vmware-vpxd.log'];
extracted_root_dir = ''
all_files = []

# Subroutines

#-------------------------------------------------------------------------------------
# This subroutine is the main call that extracts all the compressed files from VC support log
#-------------------------------------------------------------------------------------
def extract_all_logs():
      only_zips = []
      other_zips = []
      if not os.path.exists(extracted_root_dir):
            os.makedirs(extracted_root_dir)
      content_before_extract = fetch_compressed_files(extracted_root_dir,1)
      extract_zip(logFile_location,extracted_root_dir)
      content_after_extract = fetch_compressed_files(extracted_root_dir,1)
      extract_subzips(extracted_root_dir,content_before_extract,content_after_extract)
      
           # zfile.extractall(name, dirname)

#-------------------------------------------------------------------------------------
# This subroutine checks the directory name that is being created by extracted file.
#-------------------------------------------------------------------------------------
def check_extract_created_folder(before_content,after_content):
      found = ''
      for check2 in after_content:
           checked = 0
           for check1 in before_content:
                if check1 == check2:
                     checked = 1
           if not checked:
                found = check2
      if not found:
           print("Extraction has not created any directory")
      return(found)

#-------------------------------------------------------------------------------------
# This subroutine checks compressed files and directories created by them
#-------------------------------------------------------------------------------------
def fetch_compressed_files(dirname,want_dir_list):
      files = []
      for name in os.listdir(dirname):
          if want_dir_list and not os.path.isfile(os.path.join(dirname, name)):
              files.append(name)
          elif os.path.isfile(os.path.join(dirname, name)):
              files.append(dirname+'/'+name)
      # fetch list of .zip files in the extracted directory
      return(files)

      
#-------------------------------------------------------------------------------------
# This subroutine decompresses ZIP files
#-------------------------------------------------------------------------------------
def extract_zip(zip_name,dirname):
      zfile = zipfile.ZipFile(zip_name);
      if not os.path.exists(dirname):
           os.makedirs(dirname)
      zfile.extractall(dirname)

#-------------------------------------------------------------------------------------
# This subroutine decompresses .tar and .tar.gz files
#-------------------------------------------------------------------------------------
def extract_tar(tar_name,dirname):
      tar = tarfile.open(tar_name)
      if not os.path.exists(dirname):
           os.makedirs(dirname)
      tar.extractall(dirname)
      #print("Compressed "+tar_name+" in "+dirname)

#-------------------------------------------------------------------------------------
# This subroutine decompresses sub directories compressed files
#-------------------------------------------------------------------------------------
def extract_subzips(dirname,content_before_extract,content_after_extract):
      if content_before_extract or content_after_extract:
           created_dir = check_extract_created_folder(content_before_extract,content_after_extract)
           if created_dir:
                dirname=dirname+'/'+created_dir
      zips = fetch_compressed_files(dirname,0)
      for name in zips:
            if name.endswith(".zip"):
                 cont_bef  = fetch_compressed_files(dirname,1)
                 extract_dir = name.split('.zip')
                 extract_zip(name,dirname)
                 cont_aft = fetch_compressed_files(dirname,1)
                 extract_subzips(dirname,cont_bef,cont_aft)
            if name.endswith(".tar"):
                 cont_bef  = fetch_compressed_files(dirname,1)
                 extract_dir = name.split('.tar')
                 extract_tar(name,dirname)
                 cont_aft = fetch_compressed_files(dirname,1)
                 extract_subzips(dirname,cont_bef,cont_aft)
            if name.endswith(".tar.gz"):
                 cont_bef  = fetch_compressed_files(dirname,1)
                 extract_dir = name.split('.tar.gz')
                 extract_tar(name,dirname)
                 cont_aft = fetch_compressed_files(dirname,1)
                 extract_subzips(dirname,cont_bef,cont_aft)
            if name.endswith(".tgz"):
                 cont_bef  = fetch_compressed_files(dirname,1)
                 extract_dir = name.split('.tgz')
                 extract_tar(name,dirname)
                 cont_aft = fetch_compressed_files(dirname,1)
                 extract_subzips(dirname,cont_bef,cont_aft)
                 
     
#-------------------------------------------------------------------------------------
# This subroutine fetches all the products info present in VC support log.
#-------------------------------------------------------------------------------------
def product_info(root):
     pattern = '.buildInfo'
     buildinfo = []
     for path, dirs, files in os.walk(os.path.abspath(root)):
         for filename in fnmatch.filter(files, pattern):
             buildinfo.append(os.path.join(path, filename))
     content = []
     for name in buildinfo:
         set = 0
         file_info = ["Dummy"]
         with open(name,'r') as f:
             for line in f:
                 line = line.rstrip()
                 if(re.match('vpx',line)):
                     set = 1
                 if(re.match('BUILDNUMBER', line) or re.match('CHANGE:',line) or re.match('BRANCH:',line)):
                     file_info.append(line)
         if(set):
             file_info[0] = "Product is vcenter"
         else:
             file_info[0] = "Product is ESXi"
         file_info.append(name)
         all_files.append(file_info)

#-------------------------------------------------------------------------------------
# This subroutine accepts the times to fetch the logs captured between
#-------------------------------------------------------------------------------------
def get_times(type):
     time_capt = []
     time_log = ''
     while(len(time_capt) < 3):
          time_log = input("Enter the log capture "+type+" date and time in the format (dd/mm/yyyy[/hr/min/sec]) : ")
          time_capt = time_log.split('/')
     times = time_capt[2]+'-'+time_capt[1]+'-'+time_capt[0]+'T'
     for i in range(4,len(time_capt)+1):
          if i != 6:
               times = times+time_capt[i-1]+':'
          else:
               times = times+time_capt[i-1]
     return times

#-------------------------------------------------------------------------------------
# This subroutine searches for the particular file and returns its full path
#-------------------------------------------------------------------------------------
def fetch_log_fullpath(logfilename,root):
     got = []
     for path, dirs, files in os.walk(os.path.abspath(root)):
         for filename in files:
             if re.search(logfilename,filename):
                    got.append(os.path.join(path, filename))
     return(got)

#-------------------------------------------------------------------------------------
# Main Script
#-------------------------------------------------------------------------------------


print("---------------------------------------------------------------------------------------------------------")
logFile_location = input("Enter the support log file path (full path, in " " quotes) : ")
print("---------------------------------------------------------------------------------------------------------")
dirname = input("Enter the directory to extract the zip : ")
print("---------------------------------------------------------------------------------------------------------")
extracted_root_dir = dirname+'/Log_fetch_'+str(time.time())

print("\nExtracting contents and creating a file Products_buildinfo.txt that has each product's buildInfo...")

extract_all_logs();
product_info(extracted_root_dir)
conf_fil = extracted_root_dir+"/"+"Products_buildinfo.txt"
prod = open(extracted_root_dir+"/"+"Products_buildinfo.txt",'a')
print("\nCreated file "+conf_fil)
print("\n---------------------------------------------------------------------------------------------------------")
for all in all_files:
    for content in all:
        prod.write(content)
        prod.write("\n")
    prod.write("\n\n")


time_log = input("Do you wish to fetch the logs captured between certain time ? (Y|N) : ")
print("---------------------------------------------------------------------------------------------------------")
time_start = ''
time_end = ''
files_no_log = []
files_not_found = []
Log_snippet = extracted_root_dir+'/Log_snippet.txt'
snip = open(Log_snippet,'a')
if time_log == "Y":
     time_start = get_times("start");
     print("---------------------------------------------------------------------------------------------------------\n")
     time_end = get_times("end");

     print("\nLogs captured between time "+time_start+" and "+time_end+" will be saved in "+Log_snippet)
     print("\n---------------------------------------------------------------------------------------------------------")

     snip.write("\n---------------------------------------------------------------------------------------------------------\n")
     snip.write("Logs captured between time "+time_start+" and "+time_end+"\n")
     snip.write("\n---------------------------------------------------------------------------------------------------------\n")
     print("Default log files that are to be captured are")
     dfiles = ''
     for i in Log_files:
         dfiles = dfiles+" "+i
     print(dfiles+"\n")

     new_logs = input('Do you want to change the list of log files to captured ? ("Y"|"N") : ')
     if new_logs == "Y":
           print("\n---------------------------------------------------------------------------------------------------------")
           new_logs = input("Enter the new list of log files to capture that are seperated by ',' : ")
           print("---------------------------------------------------------------------------------------------------------")
           Log_files = new_logs.split(',')


     for file in Log_files:
          logPath = fetch_log_fullpath(file,extracted_root_dir)
          if not logPath:
               files_not_found.append(file)
          else:
               for each in logPath:
                   content = []
                   if each.endswith(".gz"):
                       input_file = gzip.open(each, 'rb')
                       content = input_file.readlines()
                   else:    
                       with open(each,'r') as f:
                           for line in f:
                               content.append(line)
                   start = 0
                   end = 0
                   for line in range(0,len(content)):
                           if(content[line].startswith(time_start)):
                                if not start:
                                    start = line
                           if(content[line].startswith(time_end)):
                                end = line
                     
                   if not start or not end:
                           files_no_log.append(each)
                   if start and end:
                           snip.write("\n---------------------------------------------------------------------------------------------------------\n")
                           snip.write(each)
                           snip.write("\n---------------------------------------------------------------------------------------------------------\n")
                           for line in range(start,end):
                                snip.write(content[line])

    
     if files_not_found:
         print("Failed to find below log files in provided support log");
         for file in files_not_found:
              print(file)
     print("Execution completed...\n")
