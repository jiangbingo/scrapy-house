#!/usr/bin/env python
#-*-coding:utf-8-*-


import json
import os, sys
import cv2
import numpy as np

class Find:

	def __init__(self):
		self.path = sys.path[0]
		self.hlevel = 0.35
		self.llevel = 0.09
		self.ok = self.error = 0
		self.logo = cv2.imread("logo.jpg", cv2.IMREAD_COLOR)
		with open("new.json", "r") as fd:
			data = fd.read()
		self.datas = json.loads(data)
		self.mask1 = self._create_mask("flag.jpg", 225)
		self.mask2 = self._create_mask("flag1.jpg", 210)
		self.shape = {"w": 195, "h": 87}

	def _create_mask(self, flagname, masklevel):
		flag = cv2.imread(flagname, cv2.IMREAD_COLOR)
		gray = cv2.cvtColor(flag, cv2.COLOR_BGR2GRAY)
		blur = cv2.bilateralFilter(gray, 3, 5, 5)
		# ret, mask = cv2.threshold(blur, masklevel, 255, cv2.THRESH_BINARY)
		return blur

	def _find(self, filename):
		# import ipdb;ipdb.set_trace()
		try:
			img = cv2.imread(filename.encode("gbk"), cv2.IMREAD_COLOR)
			h, w, channel = img.shape
			imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			ret, igmask = cv2.threshold(imggray, 220, 255, cv2.THRESH_BINARY)
			res = cv2.matchTemplate(igmask, self.mask1, cv2.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
			if (abs(min_val) < self.llevel or max_val > self.hlevel) and max_loc[0]> w/2.0 and max_loc[1] > h/2.0:
				self.ok += 1
				self.write_file(img, filename, max_loc)
			else:
				res = cv2.matchTemplate(igmask, self.mask2, cv2.TM_CCOEFF_NORMED)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
				if (abs(min_val) < self.llevel or max_val > self.hlevel) and max_loc[0]> w/2.0 and max_loc[1] > h/2.0:
					self.ok += 1
					self.write_file(img, filename, max_loc)
				else:
					self.error += 1
					print "error", filename
		except Exception, e:
			print "exception", e
			# import ipdb;ipdb.set_trace()

	def write_file(self, img, filename, max_loc):
		filename = filename.split("\\")[-1]
		# bottom_right = (max_loc[0] + self.shape["w"], max_loc[1] + self.shape["h"])
		# cv2.rectangle(img,max_loc, bottom_right, 255, 2)
		h, w, ch = img.shape
		if w - max_loc[0] < self.shape["w"]:
			w_size = w - max_loc[0]
		else:
			w_size = self.shape["w"]
		if h - max_loc[1] < self.shape["h"]:
			h_size = h - max_loc[1]
		else:
			h_size = self.shape["h"]
		img[max_loc[1]: max_loc[1] + h_size, max_loc[0]: max_loc[0] + w_size] = self.logo[0: h_size, 0: w_size]
		path = os.path.join(self.path, "temp", filename)
		cv2.imwrite(path, img)

	def run(self):
		count = 0
		for i in self.datas[:1000]:
			count += 1
			config_path = os.path.join(self.path, "imgs", i["type_name"], i["city"], i["url"])
			if os.path.exists(config_path):
				with open(os.path.join(config_path, "config.txt"), "r") as fd:
					config = json.loads(fd.read())
				filename = os.path.join(config_path, config["img_name"] + ".jpg")
				if os.path.exists(filename):
					self._find(filename)
		print "ok: {0}, error: {1}".format(self.ok, self.error)
		print "ok%:", float(self.ok)/(self.ok + self.error)

if __name__ == "__main__":
	fd = Find()
	fd.run()