import urllib.request
import requests
import datetime
import json
import sys
import time
import re

# Problems
# - what if doesnt archive properly? -> put link in a log file
# - sleep() for how long? -> 5min every 30 links


def check_time(original_url, check_if_url, wayback_url, memento_url):

	headers = {
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/56.0.2924.87 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
	}


	# get todays date
	x = datetime.datetime.now()

	#print("Today's Date: " + str(x.year) + '-' + str(x.month) + '-' + str(x.day))

	# Check if this page exists on the web using Wayback
	res0 = requests.post((check_if_url + original_url).encode('utf-8'), headers=headers)
	print(check_if_url + original_url)
	#print(res0.text)
	print(re.search("This page is not available on the web", res0.text))
	if (re.search("This page is not available on the web", res0.text)):
		print("This page is not available on the web")
		return False


	# Check Memento API
	res = requests.get(memento_url + original_url, allow_redirects=False)
	try:
		res_dict = json.loads(res.text)
		mems = res_dict.get("mementos")

		if res:
			for x in mems:
				if "web.archive.org" in mems[x].get('uri')[0]:
					print("Saved on: " + mems[x].get('datetime') + '\n')
					return False
	except:
		print("Error: ", sys.exc_info()[0])


	# Check Wayback Availability API
	try:
		with urllib.request.urlopen(wayback_url) as response:
			response_dict = json.loads(response.read())

			print(response_dict)
			# find last page archive date
			if (response_dict.get("archived_snapshots") == {}):
				print("Wayback hasn't archived this yet! or theres a problem...\n")
				return True

			val1 = response_dict.get("archived_snapshots")
			val2 = val1.get("closest")
			time = val2.get("timestamp")

			print("Latest save:  " + val2.get("timestamp") + '   -   ' + val2.get("url") + '\n')

			return False
			'''
			# check if page was archived today
			if ((str(x.year) == str(time)[:4]) and (str(x.month) == (str(time)[4:6]).lstrip('0')) and (str(x.day) == (str(time)[6:8]).lstrip('0'))):
				print("Same day, don't archive\n")
				return False
			else:
				print("Not same day, archive it\n")
				return True
			'''
	except:
		print("Error: ", sys.exc_info()[0])
		return True


def archive(target_url):

	my_url = "https://web.archive.org/save/{}".format(target_url)

	headers = {
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/56.0.2924.87 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
	}

	data = {
		'url': target_url
	}

	# send archive POST request to Internet Archive
	try:

		response = requests.post(my_url, headers=headers, data=data)
		cond1 = re.search("This URL has been already captured", response.text)
		cond2 = re.search("The same snapshot had been made", response.text)
		cond3 = re.search("Saving page", response.text)
		cond4 = re.search("You have already reached the limit", response.text)

		print(cond1)
		print(cond2)
		print(cond3)
		print(cond4)

		if not (cond1 or cond2 or cond3 or cond4):
			print(response.text)
		return(cond1 or cond2 or cond4)
	except:
		print("Error: ", sys.exc_info()[0])



if __name__ == "__main__":

	start_time = time.time()

	flag = sys.argv[1]
	archived_url = "http://archive.org/wayback/available?url="
	memento_url = "http://timetravel.mementoweb.org/api/json/2020/"
	check_if_url = "http://web.archive.org/web/2/"
	#link_count = 0

	couldnt_archive = []

	# if a file of links is given
	if flag == '-f':
		file = sys.argv[2]
		f = open(file, "r")
		links = f.read().splitlines()
		f.close()

		# loop through all links
		for link in links:
			print("\nCurrent Link: ", link)

			try_count = 0
			try:
				while (check_time(link, check_if_url, archived_url + link, memento_url) and try_count <= 2):
					print("Archiving...\n")
					if (archive(link)):
						print("This URL has already been captured")
						break
					time.sleep(50)
					try_count += 1
				#link_count += 1

				if try_count >= 2:
					couldnt_archive.append(link)

				#if (link_count % 40 == 0):
					#time.sleep(250)

			except:
				print("Error: ", sys.exec_info()[0])

		# log urls that couldn't be archived
		site_name = (sorted(couldnt_archive)[0]).split(".")[1]


		if len(couldnt_archive) > 0:
			f1 = open("no_" + site_name, "w+")

			for x in sorted(couldnt_archive):
				f1.write(x + '\n')

			f1.close()

	# if just a link is given
	else:
		url = sys.argv[1]
		archived_url = "http://archive.org/wayback/available?url=" + url
		memento_url = "http://timetravel.mementoweb.org/api/json/2020/"
		check_if_url = "https://web.archive.org/web/2/"

		try_count = 0
		while (check_time(url, check_if_url, archived_url + url, memento_url) and try_count <= 2):
			print("Archiving...\n")
			archive(url)
			#time.sleep(100)
			try_count += 1

	print("--- %s seconds ---" % (time.time() - start_time))
