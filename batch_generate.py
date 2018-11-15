#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-08 20:33:22
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os

def main():
	netease = []
	with open('words.txt', encoding='utf-8-sig') as f:
		for i in f.readlines():
			tmp = i.split('=')
			lrc = tmp[0]
			user = tmp[1][:-1]
			s = f'python txt2img.py -t 6 -w "{lrc}" -u "{user}" -i res/{user}.jpg'
			netease.append(s)
	with open('batch.bat', 'w', encoding='gbk') as f:
		f.write('rd /s /Q img\n')
		for i in netease:
			f.write(i)
			f.write('\n')
	os.system('batch.bat')

if __name__ == '__main__':
	main()
