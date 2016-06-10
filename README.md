# VC_support_helper
VC support helper to help debug with VMware vCenter support logs

VC_support_helper is a python script that helps to debug with VMware vCenter support logs. Basically, vCenter support log will be a ZIP file
which contains all the machine or ESXi logs that are attached to that vCenter.

Ex : If I have a vCenter with 4 ESXi hosts attached to it, when we take vc-support log, vc-support log also consists of all the 4 hosts vm-support logs.

Uses of VC_support_helper.py
1. It decopmresses all the compressed files present in vCenter log.
2. If user wants to fetch logs that are only captured between time T1 and T2, it can be done using this script
3. Using this script, one can only fetch the logs he/she wishes to.
4. This script reads content of .gz file without decompressing the .gz files which saves space.
5. You can choose your own list of log files you want to capture the logs of.
6. If you are not sure in which log file (Like vmkernel.log or vmkernel.0 or vmkernel.1) the log is captured between specified times,
  you can just mention "vmkernerl" in the list while enterring the list of logs to capture. It searches all vmkernel* files for specified
  specified log and store the results.
7. The script also fetches the buildinfos of all products that are part of vc-support log. It helps in filing the bug. 

Sample run :

-bash-4.1$ python VC_support_helper.py

This is the helper tool for VC support files. It accepts vmware VC support file and extracts all its contents.
Also, if user wants to capture only logs that have been captured between time X and Y , it can be done with this tool

---------------------------------------------------------------------------------------------------------
Enter the support log file path (full path, in  quotes) : "/dbc/blr-dbc303/mhiremath/Logs/00038221/VMware-vCenter-support-2016-01-20@15-09-01.zip"
---------------------------------------------------------------------------------------------------------
Enter the directory to extract the zip : "/dbc/blr-dbc303/mhiremath/Scripts/test_runs"
---------------------------------------------------------------------------------------------------------

Extracting contents and creating a file Products_buildinfo.txt that has each product's buildInfo...

Created file /dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465541571.21/Products_buildinfo.txt

---------------------------------------------------------------------------------------------------------
Do you wish to fetch the logs captured between certain time ? (Y|N) : "Y"
---------------------------------------------------------------------------------------------------------
Enter the log capture start date and time in the format (dd/mm/yyyy[/hr/min/sec]) : "20/01/2016/13/09"
---------------------------------------------------------------------------------------------------------

Enter the log capture end date and time in the format (dd/mm/yyyy[/hr/min/sec]) : "20/01/2016/13/10"

Logs captured between time 2016-01-20T13:09: and 2016-01-20T13:10: will be saved in /dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465541571.21/Log_snippet.txt

---------------------------------------------------------------------------------------------------------
Default log files that are to be captured are
 vvold vmkernel.log vpxa.log hostd.log sps.log vmware-vpxd.log

Do you want to change the list of log files to captured ? ("Y"|"N") : "Y"

---------------------------------------------------------------------------------------------------------
Enter the new list of log files to capture that are seperated by ',' : "vvold,vpxa,vpxd,vmkernel"
---------------------------------------------------------------------------------------------------------
Execution completed...

-bash-4.1$





Above used VC-support log had 2 ESXi machine (vm-support) logs and VC log. Script has captured VC build info and both the ESXi's build info and stored in Products_buildinfo.txt

-bash-4.1$ cat /dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465537795.08/Products_buildinfo.txt
Product is ESXi
CHANGE:3981216
BRANCH:vsphere60u2
BUILDNUMBER:3434759
/dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465537795.08/VMware-vCenter-support-2016-01-20@15-09-01/esx-l4se2198-2016-01-20--13.15/etc/vmware/.buildInfo


Product is vcenter
CHANGE:3762999
BRANCH:vsphere60u1
BUILDNUMBER:3018512
/dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465537795.08/VMware-vCenter-support-2016-01-20@15-09-01/vc-l4se2227-2016-01-20--20.09/etc/vmware/.buildInfo


Product is ESXi
CHANGE:3981216
BRANCH:vsphere60u2
BUILDNUMBER:3434759
/dbc/blr-dbc303/mhiremath/Scripts/test_runs/Log_fetch_1465537795.08/VMware-vCenter-support-2016-01-20@15-09-01/esx-l4se2196-2016-01-20--13.06/etc/vmware/.buildInfo


-bash-4.1$



