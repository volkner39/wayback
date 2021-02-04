import urllib.request
import requests
import datetime
import json
import sys
import time

def check_time(url):

	# get todays date
	x = datetime.datetime.now()

	try:
		with urllib.request.urlopen(url) as response:
			response_dict = json.loads(response.read())
		
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
			# uncomment if you want pages to be saved regardless if theres a past copy
			# check if page was archived today
			if ((str(x.year) == str(time)[:4]) and (str(x.month) == (str(time)[4:6]).lstrip('0')) and (str(x.day) == (str(time)[6:8]).lstrip('0'))):
				print("Same day, don't archive\n")
				return False
			else:
				print("Not same day, archive it\n")
				return True
			'''

	except urllib.error.HTTPError as e:
		print("Error: ", str(e.code))
		return True
	except urllib.error.URLError as e:
		print("Error: ", str(e.reason))
	except httplib.HTTPException as e:
		print("Error: HTTPException")
	except Exception:
		import traceback
		print(traceback.format_exc())
		

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
		print(response)
	except:
		print("Error: ", sys.exc_info()[0])



if __name__ == "__main__":

	start_time = time.time()
	
	flag = sys.argv[1]
	archived_url = "http://archive.org/wayback/available?url="
	link_count = 0
	
	couldnt_archive = []
	
	# if a file of links is given
	if flag == '-f':
		file = sys.argv[2]
		f = open(file, "r")
		links = f.read().splitlines()
		
		# loop through all links
		for link in links:
			print("\nCurrent Link: " + link)

			try_count = 0
			while (check_time(archived_url + link) and try_count <= 2):
				print("Archiving...\n")
				archive(link)
				time.sleep(100)
				try_count += 1
			link_count += 1
			
			if try_count >= 2:
				couldnt_archive.append(link)
			
			if (link_count % 40 == 0):
				time.sleep(250)
		
		# log urls that couldn't be archived at the end
		if len(couldnt_archive) > 0:
			folder = os.path.dirname(os.path.abspath(__file__))
			file1 = os.path.join(folder, 'couldnt_archive_' + urlsplit(url).netloc + '.txt')
			with open(file1, "w+") as f1:
				for x in sorted(couldnt_archive):
					f1.write(x + '\n')
				f1.close()
		f.close()
	
	# if just a link is given
	else:
		url = sys.argv[1]
		archived_url = "http://archive.org/wayback/available?url=" + url

		try_count = 0
		while (check_time(archived_url + url) and try_count <= 2):
			print("Archiving...\n")
			archive(url)
			time.sleep(100)
			try_count += 1

	print("--- %s seconds ---" % (time.time() - start_time))
