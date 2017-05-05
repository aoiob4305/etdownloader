# -*- coding: utf-8 -*-

import urllib, http.cookiejar
from bs4 import BeautifulSoup
import os

URL = 'http://extratorrent.cc/profile/MVGroup/torrents/'
DAY = '1d'
HOST = '192.168.12.102:9091'
#COMMAND = 'ssh kim@'+REMOTE+' "/usr/bin/transmission-remote --add '
COMMAND = '/usr/bin/transmission-remote'
USERNAME = 'kim'
PASSWORD = 'kim9119'

def getHTML(url):
	cj = http.cookiejar.LWPCookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) 
	urllib.request.install_opener(opener)
	
	params = urllib.parse.urlencode({})
	params = params.encode('utf-8')
	req = urllib.request.Request(url, params)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
	res = opener.open(req)
	html = res.read()
	
	return html
	
def getExtraTorrentLinks(html, matching_day):
	soup = BeautifulSoup(html, 'html.parser')
	
	#trz와 trl을 모두 얻는다.
	tlr = soup.find_all('tr','tlr')
	tlz = soup.find_all('tr','tlz')
	links = tlr + tlz
	
	#리스트 중 DAY에 해당하는링크부분만 추출
	torrent_links = []
	for link in links:
		tds = link.find_all('td')
		#유저 토렌트는 2번째 항목이 일자임.
		#검색인 경우 3번째 항목이 일자임.
		if tds[2].text == matching_day:
			torrent_links.append(tds[0].find_all('a')[1]['href'])
		
	return torrent_links
	
lists = getExtraTorrentLinks(getHTML(URL), DAY)

for item in lists:
	print (item)
	os.system ('%s %s --auth %s:%s --add "%s"' % (COMMAND, HOST, USERNAME, PASSWORD, item))
