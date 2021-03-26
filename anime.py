#!/usr/bin/env python3
# importing the libraries

# todo: make a search version with /search?q= choice = choice.replace(" ", "+")

from bs4 import BeautifulSoup
import requests
import os
import webbrowser
import dmenu
import sys
import wget
import datetime
import lxml
from pathlib import Path

#replace "user" with your user name
home_user = "/home/user"
#replace with your favorit image viwer
image_viewer = "feh"
source_path = Path(__file__).resolve()
source_dir = source_path.parent

#----------------------------------------------------------------------------------#
# ARGUMENTS                                                                        #
#----------------------------------------------------------------------------------#
pageSelect=False
episodeSelect=True;
download=False;
search=False
if(len(sys.argv)>0):
	for i in range(len(sys.argv)):
		arg = str(sys.argv[i])
		if arg == "-p":
			pageSelect=True
		if arg == "-l":
			#auto select last episode
			episodeSelect=False

entry = dmenu.show(["New","Search"])
if entry == "Search":
	search = True
elif entry == "New":
	search = False
else:
	exit()

entry = dmenu.show(["Download","Stream"])
if entry == "Download":
	download=True
elif entry == "Stream":
	download=False
else:
	exit()

page=0
#----------------------------------------------------------------------------------#
# FUNCTIONS                                                                        #
#----------------------------------------------------------------------------------#
def genList(size,start,befor,after):
	tempList=[]
	if start>0 and befor != None:
		tempList.append(str(befor))
	for x in range(size):
		tempList.append(str(x+start))
	if after != None:
		tempList.append(str(after))
	return tempList

#----------------------------------------------------------------------------------#
# Optional                                                                         #
#----------------------------------------------------------------------------------#
if search == False:
	if pageSelect == True:
		pagesIndex=0
		loop=True
		menuSize=6
		more=">"
		less="<"
		while loop==True:
			options=genList(menuSize,pagesIndex,less,more)
			choice = dmenu.show(options, prompt='select page')
			if str(choice) == less:
				pagesIndex-=menuSize
			elif str(choice) == more:
				pagesIndex+=menuSize
			else: 
				loop=False
				page=int(choice)

	#----------------------------------------------------------------------------------#
	# SCAN                                                                             #
	#----------------------------------------------------------------------------------#
	## scan anime kisa for new anime
	url="https://animekisa.tv/latest/"+str(page)

	if not os.path.isfile(str(source_dir)+'/data/date.txt'):
		os.makedirs(str(source_dir)+'/data')
		with open(str(source_dir)+'/data/date.txt', 'w') as fp: 
		    pass

	#check if page alredy loaded
	# if(page==0):
	# 	date = datetime.datetime.now()
	# 	now = date.strftime("%d")+'-'+date.strftime("%w")
	# 	html = open(os.path.join(sys.path[0], str(source_dir)+"/data/date.txt"), "r")
	# 	lastDate = html.readline()
	# 	if lastDate != now:
	# 		html.close()
	# 		html = open(os.path.join(sys.path[0], str(source_dir)+"/data/date.txt"), "w")
	# 		html.write(now)
	# 		html.close()
	# 		html_content = requests.get(url).text
	# 		html = open(os.path.join(sys.path[0], str(source_dir)+"/data/animekisa.html"), "w")
	# 		html.write(html_content)
	# 		html.close()
	# 	else:
	# 		html = open(os.path.join(sys.path[0], str(source_dir)+"/data/animekisa.html"), "r")
	# 		html_content=html.read()
	# 		html.close()
	# else :
	# 	html_content = requests.get(url).text
	html_content = requests.get(url).text
	frontPage = BeautifulSoup(html_content, "lxml")
	links = frontPage.find_all("a", {"class": "an"})
else :
	search = dmenu.show([], prompt='search:')
	url="https://animekisa.tv/search?q="+search
	html_content = requests.get(url).text
	frontPage = BeautifulSoup(html_content, "lxml")
	links = frontPage.find_all("a", {"class": "an"})
animes = str(links).split('href="/')
animes.pop(0)
n=0
nEpisode=0
last=""
names=[]
#store anime name in a list
for index in animes:
	name = str(animes[n]).split('"', 1)[0]
	if name != last and "episode-" not in name and len(name)>2:
		print(name)
		last = name
		nEpisode+=1
		names.append(name)
	n+=1

#----------------------------------------------------------------------------------#
# OPTIONS                                                                          #
#----------------------------------------------------------------------------------#
goto = True
while goto == True:
	choice = dmenu.show(names[:20], prompt='select anime')
	if choice not in names:
		print("choice not in names")
		exit()
	openChoice = dmenu.show(["episode","image"], prompt='open')

	if openChoice == "image":
		n=0
		imgs=[]
		coverImages = str(links).split('src="/img')
		coverImages.pop(0)
		for index in coverImages:
			img = str(coverImages[n]).split('"', 1)[0]
			if img != last and choice in img:
				last = img
				imgs.append(img)
			else:
				print(img)
			n+=1
		image_url="animekisa.tv/img"+str(imgs[0])
		image_url="https://"+image_url[:-4]
		img_type=image_url[-4:]
		img_data = requests.get(image_url).content
		img_dir = home_user+"/Documents/web/anime/data/cover"+img_type
		with open(img_dir, 'wb') as handler:
			handler.write(img_data)
		#os.system("xdg-open "+img_dir)
		os.system(image_viewer+" "+img_dir)
		#webbrowser.open(image_url)
	elif openChoice == "episode":
		goto=False
	else: 
		exit()


#----------------------------------------------------------------------------------#
# SCAN                                                                             #
#----------------------------------------------------------------------------------#
## scan anime kisa for available anime episode
url="https://animekisa.tv/"+str(choice)
html_content = requests.get(url).text
animePage = BeautifulSoup(html_content, "lxml")
links = animePage.find_all("div", {"class": "centerv"})

episodes =  str(links).split('"')
episode=[]

for index in episodes:
	if "<" in index and ">" in index:
		isIndex=''
		for s in index: 
			if s.isdigit():
				isIndex += str(s);
		if isIndex != '':
			episode.append(isIndex)

#----------------------------------------------------------------------------------#
# Optional                                                                         #
#----------------------------------------------------------------------------------#
# use dmenu here instead to select the episode
selectedEpisode=episode[0]
if episodeSelect == True:
	firstEpisode = 1
	options=genList(int(episode[0]),firstEpisode,None,None)
	#options.append("all")
	selectedEpisode = dmenu.show(options, prompt='select episode')

## scan anime kisa for download link
url="https://animekisa.tv/"+str(choice)+"-episode-"+str(selectedEpisode)
html_content = requests.get(url).text
# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
js = soup.find_all('script')
index = 6
VidStreaming = ""
jss = str(js[index]).split(';')
for lines in jss:
	if "var VidStreaming = " in lines:
		VidStreaming = str(lines).split('"')
url=str(VidStreaming[1])
if download==True:
	##to download
	html_content = requests.get(url).text
	downPage = BeautifulSoup(html_content, "lxml")
	js = downPage.find_all('script')
	links = []
	for index in js:
		if "https://gogo-play.net/download?id=" in str(index):
			links=str(index)
	links = links.split('"')
	for index in links:
		if "https://gogo-play.net/download?id=" in str(index):
			url=str(index)
	#to download video directly
	html_content = requests.get(url).text
	downVideo = BeautifulSoup(html_content, "lxml")
	url=""
	loop=0
	finalRes=""
	res=["(360P - mp4)","(480P - mp4)","(720P - mp4)","(1080P - mp4)","(HDP - mp4)"]
	while url=="" and loop<len(res):
		for index in downVideo.find_all('a', href=True):
			text = str(index.get_text())
			#print(text[-12:])
			if text[-12:] == res[loop]:
				url = index['href']
				finalRes=res[loop]
		loop+=1
	if url == "":
		print("no download available.")
		exit()
webbrowser.open(str(url))
