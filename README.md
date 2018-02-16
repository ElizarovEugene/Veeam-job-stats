# Veeam job stats

The script works through the Veeam Backup Enterprise Manager RESTful API and serves to display information about Backup jobs. Displays the name and size of the virtual machine backup (if the "use per-vm backup files" checkbox is set in the repository settings) and the total size of the job.
![use per-vm backup files](https://d1ro8r1rbfn3jf.cloudfront.net/ms_22938/QfYd2NYPC2tRHneAKIKt407FHJ1HIg/veeam%2Boncloud%2B%2528RDP%2529%2B2018-02-16%2B08-52-38.png?Expires=1518846794&Signature=D8Ddw-NxrwaANDT0W9nxtS6Y~5BDOj2Od4F9tud1C1-vE0FlCf1QbGWwo1MBsunGaTanGTtezMJXjD5zAvGHfNeIU7C-Cq~f7Es1hs4x-AlUvkNltTU3T~6aWWqpNQWYdS7hz6ByoxlQKP5WRUWuJPaI3Co~802Ss2K0V5JU-PPx9N3OehHRhw9ZvxopVRiw1BwIkQnwCivbxQ39GNuSd5ceJ49kl5d3TxihIH21CE-NsIK169aWYHaGJonEeQQBSf9AHQf9QE5TFwyrp9xteqk1G4id-eaoIjFfSTTx9dPYD8Gz-mtEWsI1v49yFTKS1Ian3A77wqUvWyKCbqAdlg__&Key-Pair-Id=APKAJHEJJBIZWFB73RSA)


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
