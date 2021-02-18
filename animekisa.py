# importing the libraries
from bs4 import BeautifulSoup
import requests
import os
import webbrowser
#import dmenu

## scan anime kisa for new anime
try:
	page=int(input("page: "))
except:
	page=0
url="https://animekisa.tv/latest/"+str(page)
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
	if name != last and "episode-" not in name:
		last = name
		#temporary until dmenu
		print(" "+str(nEpisode)+": "+name)
		nEpisode+=1
		names.append(name)
	n+=1
# use dmenu here instead to select the anime
try:
	serie=int(input("anime: "))
except :
	serie=0

## scan anime kisa for available anime episode
url="https://animekisa.tv/"+str(names[serie])
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

# use dmenu here instead to select the episode
print("total episodes: "+episode[0])
maxEpisode = int(episode[0])
selectedEpisode = int(input("epidode: "))
while selectedEpisode > maxEpisode or maxEpisode<0:
	print("please enter a valide episode number.")
	selectedEpisode = input("epidode: ")

## scan anime kisa for download link
url="https://animekisa.tv/"+str(names[serie])+"-episode-"+str(selectedEpisode)
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

## scan download page for download
# example "https://gogo-play.net/load.php?id=MTUyNTE4&title=Beastars+2nd+Season&typesub=SUB&sub=&cover=Y292ZXIvYmVhc3RhcnMtMm5kLXNlYXNvbi5wbmc="
url=str(VidStreaming[1])
webbrowser.open(str(url))

##to download
# html_content = requests.get(url).text
# downPage = BeautifulSoup(html_content, "lxml")
# js = downPage.find_all('script')
# links = []
# for index in js:
# 	if "https://gogo-play.net/download?id=" in str(index):
# 		links=str(index)
# links = links.split('"')
# for index in links:
# 	if "https://gogo-play.net/download?id=" in str(index):
# 		downLink=str(index)
# webbrowser.open(str(downLink))




#rawj = soup.find_all('script')
#rawj = rawj.split('var VidStreaming = ')
#print(str(rawj))