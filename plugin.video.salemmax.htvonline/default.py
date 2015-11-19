# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib,urllib2,re,os,sys,json
import xbmcplugin,xbmcgui,xbmcaddon

mysettings=xbmcaddon.Addon(id='plugin.video.salemmax.htvonline')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
dataPath = xbmc.translatePath(os.path.join(home, 'resources'))

	
def main():
    homeUrl = "http://api.htvonline.com.vn/tv_channels"
    reqdata = '{"pageCount":200,"category_id":"-1","startIndex":0}'
    data = makerequest ( homeUrl , reqdata)
    print data
    for item in data ["data"] :
      res = item["link_play"][0]["resolution"]
      res = res.replace('720p','[COLOR yellow]HD[/COLOR]').replace('360p','[COLOR cyan]SD[/COLOR]')	
      thumb = item["image"]
      title = '[UPPERCASE]' + item["name"] + '[/UPPERCASE]'
      link = item["link_play"][0]["mp3u8_link"]
      addLink(title.encode('utf-8'), link,100,thumb)
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.xeebo':
      xbmc.executebuiltin('Container.SetViewMode(52)')  
    else:
      xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)

def resolveUrl(url):
    try:
      mediaUrl=url
      item = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
      item.setPath(mediaUrl)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    except:
      pass
	
def makerequest(url, requestdata):
    req = urllib2 . Request(urllib . unquote_plus(url))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Authorization', 'Basic YXBpaGF5aGF5dHY6NDUlJDY2N0Bk')
    req.add_header('User-Agent', 'Apache-HttpClient/UNAVAILABLE (java 1.4)')
    link = urllib . urlencode({'request': requestdata})
    resp = urllib2 . urlopen(req, link, 120)
    content = resp . read()
    resp . close()
    content = '' . join(content . splitlines())
    data = json . loads(content)
    return data

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
      params=sys.argv[2]
      cleanedparams=params.replace('?','')
      if (params[len(params)-1]=='/'):
        params=params[0:len(params)-2]
      pairsofparams=cleanedparams.split('&')
      param={}
      for i in range(len(pairsofparams)):
        splitparams={}
        splitparams=pairsofparams[i].split('=')
        if (len(splitparams))==2:
          param[splitparams[0]]=splitparams[1]
    return param
				  
def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
   
def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok  
  
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass  
try:mode=int(params["mode"])
except:pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "iconimage: " + str(iconimage)

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
   main()

elif mode==100:
     dialogWait = xbmcgui.DialogProgress()
     dialogWait.create('salemmax.htvonline Plus', 'Đang tải. Vui lòng chờ trong giây lát...')
     resolveUrl(url)
     dialogWait.close()
     del dialogWait
	 
xbmcplugin.endOfDirectory(int(sys.argv[1]))