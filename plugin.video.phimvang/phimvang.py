__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmcaddon,xbmcplugin,xbmcgui
import httplib
from bs4 import BeautifulSoup
# import urlresolver
import xbmcvfs

root_link = 'http://phimvang.org'
logo = 'http://phimvang.com/sites/all/themes/news/logo.png'
searchlink='http://phimvang.org/tim-kiem/tat-ca/'

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
mysettings = xbmcaddon.Addon(id='plugin.video.phimvang')
icon = addon.getAddonInfo('icon')
mysettings = xbmcaddon.Addon(id='plugin.video.phimvang')
home = mysettings.getAddonInfo('path')

addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID).decode('utf-8')
libraryFolder = os.path.join(addonUserDataFolder, "library")
libraryFolderMovies = os.path.join(libraryFolder, "Movies")
libraryFolderTV = os.path.join(libraryFolder, "TV")
custLibFolder = mysettings.getSetting('library_path')
custLibTvFolder = mysettings.getSetting('libraryTV_path')

if not os.path.exists(os.path.join(addonUserDataFolder, "settings.xml")):
    addon.openSettings()
if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)
if not os.path.isdir(libraryFolder):
    os.mkdir(libraryFolder)
if not os.path.isdir(libraryFolderMovies):
    os.mkdir(libraryFolderMovies)
if not os.path.isdir(libraryFolderTV):
    os.mkdir(libraryFolderTV)

def home():
    addDir('[COLOR ffffd700]Search[/COLOR]',searchlink,5,logo,False,None,'')
    link = urllib2.urlopen(root_link).read()
    soup = BeautifulSoup(link)
    li_menu = BeautifulSoup(str(soup('div',{'id':'menu'})[0]))('li')
    for m in li_menu:
        mtitle = BeautifulSoup(str(m))('a')[0].contents[0]
        mlink = BeautifulSoup(str(m))('a')[0]['href']
        addDir(mtitle.encode('utf-8'),root_link+mlink,1,logo,False,None,'')


def index(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    h2s = soup('h2')
    for h in h2s:
        hsoup = BeautifulSoup(str(h))
        hlink = root_link+hsoup('a')[0]['href'].replace('phim','xem-phim')
        himage = hsoup('img')[1]['data-original']
        htitle = hsoup('img')[1]['alt']
        addDir(htitle.encode('utf-8'),hlink,2,himage,False,None,htitle.encode('utf-8'))
    try:
        paging = soup('div',{'class':'paging'})
        pages = BeautifulSoup(str(paging[0]))('a')

        for p in pages:
            psoup = BeautifulSoup(str(p))
            ptitle = psoup('a')[0].contents[0]
            plink = root_link+psoup('a')[0]['href']
            addDir(ptitle.encode('utf-8'),plink,1,logo,False,None,'')
    except:pass

def serverlist(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    epis = soup('p',{'class':'epi'})
    for i in range(0,len(epis)):
        etitle = BeautifulSoup(str(epis[i]))('b')[0].contents[0]
        addDir(etitle.encode('utf-8'),url,3,iconimage,False,i,gname)

def episode(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    epis = soup('p',{'class':'epi'})
    elist = BeautifulSoup(str(epis[inum]))('a')
    for i in range(0,len(elist)):
        esoup = BeautifulSoup(str(elist[i]))
        elink = root_link+esoup('a')[0]['href']
        etitle = esoup('a')[0].contents[0]
        addLink(etitle.encode('utf-8'),elink,4,iconimage,gname)

def videolinks(url):
    url = ''.join(url.split())
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    if newlink.find('youtube')!=-1:
        vlink = re.compile('file : "(.+?)&amp').findall(newlink)[0]
        final_link=vlink
    else:
        try:
            vlinks = re.compile(',\{file: "(.+?)", label:"720p"').findall(newlink)[0]
        except:
            vlinks = re.compile('file: "(.+?)", label').findall(newlink)[0]
        final_link=vlinks

    return final_link


def medialink(url):
    link = urllib2.urlopen(url).read()
    newlink = ''.join(link.splitlines()).replace('\t','')
    myregex = re.escape(url)+r'(.+?){"rel":"alternate"'
    match=re.compile(myregex).findall(newlink)
    if len(match)<=0:
        if url.find('&feat=directlink'):
            url = str(url).replace('&feat=directlink', '')
        myregex=re.escape(url)+r'(.+)'
        match=re.compile(myregex).findall(newlink)
        # if len(match)<=0:
        #     myregex=re.escape(url.replace('&feat=directlink','')+r'(.+)')
        #     match=re.compile(myregex).findall(newlink)
    if len(match)<=0:
        mlink = re.compile(',{"url":"(.+?)","height"').findall(newlink)
    else:
        mlink = re.compile(',{"url":"(.+?)","height"').findall(match[0])
    if len(mlink)>1:
        return mlink[1]
    else:
        return mlink[0]

def play(url,name):
    VideoUrl = videolinks(url)
    if VideoUrl.find('youtube')!=-1:
        match = re.compile('&.+').findall(VideoUrl)
        if len(match)>0:
            VideoUrl= VideoUrl.replace(match[0],'')
        idregex = r'https?://www.youtube.com/(?:embed/|watch\?v=)'+r'(.+?(?=\?)|.+)'
        VideoUrl = re.compile(idregex).findall(VideoUrl)[0]
        VideoUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(VideoUrl).replace('?','')
        # hostedmedia = urlresolver.HostedMediaFile(VideoUrl)
        # print hostedmedia
        # VideoUrl = hostedmedia.resolve()

    listitem = xbmcgui.ListItem(name, path=VideoUrl)
    listitem.setInfo( type="Video", infoLabels={ "Title": name })
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=VideoUrl))

def addToLibrary(url):
    if mysettings.getSetting('cust_Lib_path')=='true':
        newlibraryFolderMovies = custLibFolder
    else:
        newlibraryFolderMovies = libraryFolderMovies
    movieFolderName = (''.join(c for c in unicode(gname, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    newMovieFolderName=''
    finalName=''
    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Title[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        newMovieFolderName=keyb.getText()
    if newMovieFolderName !='':
        dir = os.path.join(newlibraryFolderMovies, newMovieFolderName)
        finalName=newMovieFolderName
    else:
        dir = os.path.join(newlibraryFolderMovies, movieFolderName)
        finalName=movieFolderName
    if not os.path.isdir(dir):
        xbmcvfs.mkdir(dir)
        fh = xbmcvfs.File(os.path.join(dir, finalName+".strm"), 'w')
        fh.write('plugin://'+addonID+'/?mode=4&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(finalName))
        fh.close()

def addSeasonToLibrary(url):
    if mysettings.getSetting('cust_LibTV_path')=='true':
        newlibraryFolderMovies = custLibTvFolder
    else:
        newlibraryFolderMovies = libraryFolderTV
    movieFolderName = (''.join(c for c in unicode(gname, 'utf-8') if c not in '/\\:?"*|<>')).strip(' .')
    newMovieFolderName=''
    finalName=''
    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Title[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        newMovieFolderName=keyb.getText()
    if newMovieFolderName !='':
        dir = os.path.join(newlibraryFolderMovies, newMovieFolderName)
        finalName=newMovieFolderName
    else:
        dir = os.path.join(newlibraryFolderMovies, movieFolderName)
        finalName=movieFolderName

    keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter Season[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
        seasonnum=keyb.getText()

    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    epis = soup('p',{'class':'epi'})
    elist = BeautifulSoup(str(epis[0]))('a')

    if not os.path.isdir(dir):
        xbmcvfs.mkdir(dir)
        for i in range(0,len(elist)):
            esoup = BeautifulSoup(str(elist[i]))
            elink = root_link+esoup('a')[0]['href']
            etitle = esoup('a')[0].contents[0]
            if len(etitle)==1:
                epnum = '0'+etitle
            else:
                epnum=etitle
            epname = ''.join(["S", seasonnum, "E", epnum, ' - ', finalName])
            fh = xbmcvfs.File(os.path.join(dir, epname+".strm"), 'w')
            fh.write('plugin://'+addonID+'/?mode=4&url='+urllib.quote_plus(elink)+'&name='+urllib.quote_plus(''.join(["[", etitle.encode('utf-8'), "] ", gname])))
            fh.close()
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno('TV Show Exists','Update Files?'):
            for i in range(0,len(elist)):
                esoup = BeautifulSoup(str(elist[i]))
                elink = root_link+esoup('a')[0]['href']
                etitle = esoup('a')[0].contents[0]
                if len(etitle)==1:
                    epnum = '0'+etitle
                else:
                    epnum=etitle
                epname = ''.join(["S", seasonnum, "E", epnum, ' - ', finalName])
                fh = xbmcvfs.File(os.path.join(dir, epname+".strm"), 'w')
                fh.write('plugin://'+addonID+'/?mode=4&url='+urllib.quote_plus(elink)+'&name='+urllib.quote_plus(''.join(["[", etitle.encode('utf-8'), "] ", gname])))
                fh.close()

############################################################################
# SEARCH
############################################################################
def loadHistory(url):
    try:
        addDir('[COLOR ffffd700]Search[/COLOR]',url,6,logo,False,None,'')
        if mysettings.getSetting('save_search')=='true':
            searches = getStoredSearch()
            if len(searches)!=0:
                searches = eval(searches)
                idn = 0
                for s in searches:
                    addDir(s,(url+urllib.quote_plus(s).replace('+','-'))+'.html',1,logo,True,idn,s)
                    idn+=1
    except:pass

def deleteSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        del(searches[inum])
        saveStoredSearch(searches)
    except StopIteration:
        pass

def editSearch():
    try:
        searches = getStoredSearch()
        searches = eval(searches)
        keyb = xbmc.Keyboard(name, '[COLOR ffffd700]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            newsearch = keyb.getText()
            searches[inum]=newsearch
        saveStoredSearch(searches)
        newsearch=urllib.quote_plus(newsearch)
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Search(searchlink+newsearch)
    except:pass

def getUserInput():
    try:
        searches = getStoredSearch()
        keyb = xbmc.Keyboard('', '[COLOR ffffd700]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText()).replace('+','-')
            url = searchlink+ searchText+'.html'
            if mysettings.getSetting('save_search')=='true':
                if searchText!='':
                    if len(searches)==0:
                        searches = ''.join(["['",urllib.unquote_plus(searchText.replace('-','+')),"']"])
                        searches = eval(searches)
                    else:
                        searches = eval(searches)
                        searches = [urllib.unquote_plus(searchText.replace('-','+'))] + searches
                    saveStoredSearch(searches)
        return url
    except:pass

def Search(url):
    try:
        if url.find('.html')!=-1:
            url = url.rstrip()
        else:
            url = getUserInput()
        xbmc.executebuiltin("XBMC.Container.Refresh")
        index(url)
    except: pass

def getStoredSearch():
    try:
        searches = mysettings.getSetting('store_searches')
        return searches
    except:pass

def saveStoredSearch(param):
    try:
        mysettings.setSetting('store_searches',repr(param))
    except:pass

##############################################################
# END SEARCH
#############################################################



def addDir(name, url, mode, iconimage,edit,inum,gname):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&inum="+str(inum)+"&gname="+urllib.quote_plus(gname)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    contextmenuitems = []
    if edit:
        contextmenuitems.append(('[COLOR red]Delete[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=8&name=%s&inum=%d)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        contextmenuitems.append(('[COLOR ff00ff00]Edit[/COLOR] [COLOR ffffd700]Search[/COLOR]','XBMC.Container.Update(%s?url=%s&mode=9&name=%s&inum=%d)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(name),inum)))
        liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,gname):
    name = ''.join(["[", name, "] ", gname])
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    contextmenuitems = []
    # contextmenuitems.append(('[COLOR yellow]Download[/COLOR]','XBMC.Container.Update(%s?url=%s&gname=%s&mode=10)'%('plugin://plugin.video.vkool',urllib.quote_plus(url),urllib.quote_plus(gname))))
    contextmenuitems.append(('[COLOR yellow]Add Movie To Library[/COLOR]','XBMC.Container.Update(%s?url=%s&gname=%s&mode=10)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(gname))))
    contextmenuitems.append(('[COLOR yellow]Add Season To Library[/COLOR]','XBMC.Container.Update(%s?url=%s&gname=%s&mode=11)'%('plugin://plugin.video.phimvang',urllib.quote_plus(url),urllib.quote_plus(gname))))
    liz.addContextMenuItems(contextmenuitems,replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok

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

params=get_params()
url=None
name=None
mode=None
iconimage=None
edit=None
inum=None
gname=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        edit = bool(params["edit"])
except:
        pass
try:
        inum=int(params["inum"])
except:
        pass
try:
        gname=urllib.unquote_plus(params["gname"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index(url)
elif mode==2:
    serverlist(url)
elif mode==3:
    episode(url)
elif mode==4:
    play(url,name)
elif mode==5:
    loadHistory(url)
elif mode==6:
    Search(url)
elif mode==7:
    episodes(url)
elif mode==8:
    deleteSearch()
elif mode==9:
    editSearch()
elif mode==10:
    addToLibrary(url)
elif mode==11:
    addSeasonToLibrary(url)

xbmcplugin.endOfDirectory(int(sysarg))