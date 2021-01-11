import urllib.request
import requests
import datetime
import json
import sys

def check_time(url):

	# get todays date
	x = datetime.datetime.now()
	
	print(x.year, x.month, x.day)

	# first check if the page was archived today
	with urllib.request.urlopen(url) as response:
		#html = response.read()
		response_dict = json.loads(response.read())
		
		# get the closest archived time for page
		print(response_dict)
		
		if (response_dict.get("archived_snapshots") == {}):
			print("Wayback hasn't archived this yet!")
			return True
		
		val1 = response_dict.get("archived_snapshots")
		val2 = val1.get("closest")
		time = val2.get("timestamp")

		# check year, month, day
		if ((str(x.year) == str(time)[:4]) and (str(x.month) == (str(time)[4:6]).lstrip('0')) and (str(x.day) == (str(time)[6:8]).lstrip('0'))):
			print("same day, don't archive")
			return False
		else:
			print("not same day, archive it")
			return True
		

def archive(target_url):
	# if it hasn't, let's archive it...
	save_url = "https://archive.is/submit/"
	my_url = "https://web.archive.org/save/{}".format(target_url)

	# send archive request to archive.is
	response = requests.get(my_url)

	# print out headers in response
	for x in response.headers:
		print(x + ":  " + response.headers.get(x))


	# check if page was archived
	#if response.status_code == 200:
	

if __name__ == "__main__":
	
	flag = sys.argv[1]
	
	# if a file of links is given
	if flag == '-f':
		file = sys.argv[2]
		f = open(file, "r")
		links = f.read().splitlines()
		
		# loop through all links
		for link in links:
			archived_url = "http://archive.org/wayback/available?url=" + link

			if(check_time(archived_url)):
				print("Archiving...")
				archive(link)
		
				if(~check_time(archived_url)):
					print("updated")
	
	# if just a link is given
	else:
		archived_url = "http://archive.org/wayback/available?url=" + flag

		if(check_time(archived_url)):
			print("Archiving...")
			archive(flag)

			if(~check_time(archived_url)):
				print("updated")