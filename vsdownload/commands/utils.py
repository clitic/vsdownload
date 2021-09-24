import re
import statistics
import threading

  
def find_urls_by_ext(string, ext, commanurls=True):
	regex = re.compile(rf"https?://[a-zA-Z0-9-._%/]*\.{ext}")
	matches = re.findall(regex, string)

	if commanurls:
		return list(matches)
	else:
		urls = []
		for match in matches:
			if match not in urls:
				urls.append(match)

		return urls

def find_baseurl_by_urls(listofurls, ext, static=True):
	regex = re.compile(rf"[^/][a-zA-Z0-9-._%]*\.{ext}")

	possible_base_urls = []
	for link in listofurls:
		matches = re.findall(regex, link)
		for match in matches:
			possible_base_urls.append(link.split(match)[0])

	try:
		if static:
			return statistics.mode(possible_base_urls)
		else:
			return possible_base_urls[0]
	except:
		return []


def convertbytes(bytesval):
	for unit in ["bytes", "KB", "MB", "GB", "TB"]:
		if bytesval < 1024.0:
			return ("{:.2f} {}".format(bytesval, unit), bytesval, unit)
		bytesval /= 1024.0

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
