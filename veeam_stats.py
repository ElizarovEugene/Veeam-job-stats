#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import collections
import re
import requests
import sys
import urllib3

class Veeam:
	#Initialize variable and get API authorize token
	def __init__(self):
		urllib3.disable_warnings()
		self.address = 'https://IP:9398/api/'
		self.username = 'username'
		self.password = 'password'
		
		self.session_id = self.get_authorize_token()
		self.headers = {'X-RestSvcSessionId': self.session_id['session_id'], 'Content-Type': 'application/xml'}

	#Get API authorize token
	def get_authorize_token(self):
		try:
			r = requests.post(self.address + 'sessionMngr/?v=latest', auth=(self.username, self.password), verify=False)
			if r.status_code != 201:
				raise Exception('Authorization faileds')
			return {'session_id': r.headers['X-RestSvcSessionId']}
		except Exception:
			sys.exit('Authorization faileds')
			
	def get_backup_list(self, address):
		r = requests.get(address, headers=self.headers, verify=False)
		soup = BeautifulSoup(r.text, 'xml')
		points = soup.findAll('Ref', {'Type':'BackupReference'})
		jobs = []
		for point in points:
			jobs.append(point.get('Name'))
		jobs.sort()
		return jobs
			
	def get_repositorie_info(self, address):
		r = requests.get(address, headers=self.headers, verify=False)
		soup = BeautifulSoup(r.text, 'xml')
		capacity = soup.find('Capacity').get_text()
		free = soup.find('FreeSpace').get_text()
		backups = soup.findAll('Link', {'Type':'BackupReferenceList'})
		link = backups[0].get('Href')
		jobs = self.get_backup_list(link)
		return capacity, free, jobs
			
	def get_repositories(self):
		r = requests.get(self.address + 'repositories', headers=self.headers, verify=False)
		soup = BeautifulSoup(r.text, 'xml')
		points = soup.findAll('Ref', {'Type':'RepositoryReference'})
		for point in points:
			name = point.get('Name')
			if name == 'NetApp SnapShot':
				continue
			else:
				print 'Repository name: ' + name
				links = point.findAll('Link')
				link = links[1].get('Href')
				info = self.get_repositorie_info(link)
				capacity = round(float(info[0]) / 1000 / 1000 / 1000, 2)
				free = round(float(info[1]) / 1000 / 1000 / 1000, 2)
				print 'Repository size: ' + str(capacity) + 'Gb'
				print 'Repository free size: ' + str(free) + 'Gb'
				print 'Repository jobs:'
				for x in info[2]:
					print '\t' + x
				print "\n"

	#Get VM restore points and generate statistic	
	def get_vm_restore_points(self):
		stats = {}
		total_vm = 0
		total_all_size = 0
		r = requests.get(self.address + 'vmRestorePoints', headers=self.headers, verify=False)
		soup = BeautifulSoup(r.text, 'xml')
		points = soup.findAll('Link', {'Type':'BackupFileReference'})
		for point in points:
			pointUrl = point.get('Href')
			pointUrl = pointUrl + '?format=Entity'
			result = self.get_point(pointUrl)
			if len(result) == 3:
				if result[0] in stats:
					pass
				else:
					stats[result[0]] = {}
				if result[1] in stats[result[0]]:
					stats[result[0]][result[1]] += result[2]
				else:
					stats[result[0]][result[1]] = result[2]

		stats = collections.OrderedDict(sorted(stats.items()))
		for k, v in stats.iteritems():
			total_size = 0
			print 'Job name: ' + k
			print 'VMs \t\t\tSize'
			for k1, v1 in v.iteritems():
				if len(k1) > 15:
					delimiter = '\t'
				else:
					delimiter = '\t\t'
				if len(k1) < 8:
					delimiter = '\t\t\t'
				print k1 + delimiter + str(v1) + 'Gb'
				total_size += v1
				
				total_vm += 1
				total_all_size += v1
			print 'Total size: ' + str(total_size) + 'Gb'
			print "\n"
		print '-' * 40
		print 'Total VMs: ' + str(total_vm)
		print 'Total backups size: ' + str(total_all_size) + 'Gb'

	#Get info about restore point: job name, vm name, size
	def get_point(self, url):
		r = requests.get(url, headers=self.headers, verify=False)
		soup = BeautifulSoup(r.text, 'xml')
		job = soup.findAll('Link')[0].get('Name')
		vm = soup.findAll('Link')[2].get('Name')
		result = re.search(r'^(.*)\.vm\-', vm)
		if result is not None:
			vm = result.group(1)
		size = round(float(soup.find('BackupSize').getText()) / 1000 / 1000 / 1000, 2)
		return job, vm, size

if __name__ == "__main__":
	veeam = Veeam()
	if len(sys.argv) == 1:
		print 'Use keys: -backups, -repos'
		sys.exit(0)
	if sys.argv[1] == '-backups':
		veeam.get_vm_restore_points()
	if sys.argv[1] == '-repos':
		veeam.get_repositories()