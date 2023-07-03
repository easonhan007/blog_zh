---
title: "你应该知道的python自动化脚本"
date: 2023-07-03T11:31:49+08:00
draft: false
---

www.freecodecamp.org是我密切关注的免费学习编程的网站，里面不定期会有高质量且最新的各种编程以及技术教程，今天偶然在freecodecap看到一篇讲python进行日常自动化的帖子，原文在这里https://www.freecodecamp.org/news/python-automation-scripts/，觉得有点意思，顺便就把里面的内容拿出来分享和评论一下。

### 自动校对

```python
# Python Proofreading
# pip install lmproof
import lmproof
def proofread(text):
    proofread = lmproof.load("en")
    correction = proofread.proofread(text)
    print("Original: {}".format(text))
    print("Correction: {}".format(correction))
    
proofread("Your Text")
```

说实话，似乎用不上。

### 自动随机播放音乐

```python
import random, os
music_dir = 'E:\\music diretory'
songs = os.listdir(music_dir)

song = random.randint(0,len(songs))

# Prints The Song Name
print(songs[song])  

os.startfile(os.path.join(music_dir, songs[0])) 
```

思路很好，不过似乎也用不上。


### pdf转csv

```python

import tabula

filename = input("Enter File Path: ")
df = tabula.read_pdf(filename, encoding='utf-8', spreadsheet=True, pages='1')

df.to_csv('output.csv')

```

需要```pip install tabula```，在做数据处理的时候就很有用了，因为有些站点的收据下载的格式默认就是pdf的。

### 自动压缩照片

```python
import PIL
from PIL import Image
from tkinter.filedialog import *

fl=askopenfilenames()
img = Image.open(fl[0])
img.save("output.jpg", "JPEG", optimize = True, quality = 10)
```

需要安装PIL(Python Imaging Library) ，在归档的时候应该有些用处。

### 自动下载YouTube视频

```python

import pytube

link = input('Youtube Video URL')
video_download = pytube.Youtube(link)
video_download.streams.first().download()
print('Video Downloaded', link)
```

需要安装pytube，国内的话用处不大，推荐一个替代的命令行工具**you-get**，可以下载b站视频，有兴趣的同学可以研究一下。

### 自动文本转语音

```python
from pygame import mixer
from gtts import gTTS

def main():
   tts = gTTS('Like This Article')
   tts.save('output.mp3')
   mixer.init()
   mixer.music.load('output.mp3')
   mixer.music.play()
   
if __name__ == "__main__":
   main()

```
这里用的是Google Text to Speech API，国内用不上。


### 图片转pdf

```python
from fpdf import FPDF
Pdf = FPDF()

list_of_images = ["wall.jpg", "nature.jpg","cat.jpg"]
for i in list_of_images:
   Pdf.add_page()
   Pdf.image(i,x,y,w,h)
   Pdf.output("result.pdf", "F")
```

可以批量转，应该有用。

### 抄袭检测

```python
from difflib import SequenceMatcher
def plagiarism_checker(f1,f2):
    with open(f1,errors="ignore") as file1,open(f2,errors="ignore") as file2:
        f1_data=file1.read()
        f2_data=file2.read()
        res=SequenceMatcher(None, f1_data, f2_data).ratio()
        
print(f"These files are {res*100} % similar")
f1=input("Enter file_1 path: ")
f2=input("Enter file_2 path: ")
plagiarism_checker(f1, f2)
```
其实就是比较两个文件的相似性，不知道对中文的支持如何。

### 生成短链接

```python
from __future__ import with_statement
import contextlib
try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen
import sys

def make_tiny(url):
	request_url = ('http://tinyurl.com/app-index.php?' + 
	urlencode({'url':url}))
	with contextlib.closing(urlopen(request_url)) as response:
		return response.read().decode('utf-8')

def main():
	for tinyurl in map(make_tiny, sys.argv[1:]):
		print(tinyurl)

if __name__ == '__main__':
	main()
    

'''

-----------------------------OUTPUT------------------------
python url_shortener.py https://www.wikipedia.org/
https://tinyurl.com/bif4t9

'''
```
    
调用第三方服务生成短链接，其实也可以自己写个短链接的生成服务，用flask+redis就可以了。


### 网络测速

```python
# Internet Speed tester
# pip install speedtest-cli
import speedtest as st

# Set Best Server
server = st.Speedtest()
server.get_best_server()

# Test Download Speed
down = server.download()
down = down / 1000000
print(f"Download Speed: {down} Mb/s")

# Test Upload Speed
up = server.upload()
up = up / 1000000
print(f"Upload Speed: {up} Mb/s")

# Test Ping
ping = server.results.ping
print(f"Ping Speed: {ping}")

```

这个很有用的，可以保存一下。


### 总结

这些自动化脚本其实都很不错，短小精悍，属于入门级，尽管跟离提升工作效率的目的还有点距离，不过却可以很好的向初学者进行python自动化概念的展示，很不错的帖子。


