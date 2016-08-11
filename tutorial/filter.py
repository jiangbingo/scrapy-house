#!/usr/bin/env python
#-*-coding:utf-8-*-


import json


class Filter:
	old_name = "data.json"
	urls_name = "urls.json"
	new_name = "new.json"

	def get_data(self):
		fd = open(self.old_name, "r")
		data = fd.read()
		fd.close()
		data = json.loads(data)
		return data

	# def url_filter(self):
	# 	fd = open(self.urls_name, "r")
	# 	old_urls = json.loads(fd.read())
	# 	fd.close()
	# 	data = self.get_data()
	# 	for i in data:
	# 		if i["url"] not in old_urls:
	# 			old_urls.append(i["url"])
	# 	print "urls length", len(old_urls)
	# 	fd = open(self.urls_name, "w")
	# 	fd.write(json.dumps(old_urls))
	# 	fd.close()
	
	def data_filter(self):
		data = self.get_data()

		ufd = open(self.urls_name, "r")
		old_urls = json.loads(ufd.read())
		ufd.close()

		fd = open(self.new_name, "r")
		old_data = json.loads(fd.read())
		fd.close()

		for i in data:
			if i["url"] not in old_urls:
				old_urls.append(i["url"])
				old_data.append(i)

		print "data length", len(old_data)

		nfd = open(self.new_name, "w+")
		nfd.write(json.dumps(old_data))
		nfd.close()

		print "urls length", len(old_urls)
		
		nufd = open(self.urls_name, "w+")
		nufd.write(json.dumps(old_urls))
		nufd.close()

if __name__ == "__main__":
	ft = Filter()
	ft.data_filter()