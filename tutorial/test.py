#!/usr/bin/env python
#-*-coding:utf-8-*-

import json
import os, sys

fd = open("new.json", "r")
data = fd.read()
fd.close()
data = json.loads(data)
base_path = os.path.join(sys.path[0], "imgs")
count = 0
error = 0
for i in data:
	path = os.path.join(base_path, i["type_name"], i["city"], i["url"])
	if os.path.exists(path):
		count += 1
	else:
		error += 1
print "count", count, error
