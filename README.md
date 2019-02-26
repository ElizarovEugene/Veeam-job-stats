# Veeam job stats

The script works through the Veeam Backup Enterprise Manager RESTful API and serves to display information about Backup jobs. Displays the name and size of the virtual machine backup (if the "use per-vm backup files" checkbox is set in the repository settings) and the total size of the job.

use "per-vm backup files" setting!

Example:
```
./veeam_stats.py -backups
Job name: Exchange
VMs			Size
EX-MAIL1		379.91Gb
SAFE-MAIL1		881.16Gb
EX-DC2			8.85Gb
EX-DC1			14.3Gb
SAFE-DC1		31.01Gb
SAFE-DC2		23.78Gb
Total size: 1339.01Gb
```
Also, the script allows you to get information about the repository and the tasks that are configured for these repositories
Example:
```
./veeam_stats.py -repos
Repository name: Infortrend
Repository size: 2198.82Gb
Repository free size: 1255.58Gb
Repository jobs:
	Zimbra

Repository name: Default Backup Repository
Repository size: 107.0Gb
Repository free size: 56.19Gb
Repository jobs:
	Exchange balancers

Repository name: Local
Repository size: 5497.42Gb
Repository free size: 1534.37Gb
Repository jobs:
	Exchange
	TestOrg_Test
```

As a setting, you must specify variables
```
self.address = 'https://IP:9398/api/'
self.username = 'username'
self.password = 'password'
```
