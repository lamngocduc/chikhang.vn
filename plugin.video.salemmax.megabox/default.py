# -*- coding: utf-8 -*-

# Standard libs
import urllib,urllib2,unicodedata,string,re,os

# TODO: Uncomment!
import xbmcplugin,xbmcgui,xbmc,xbmcaddon

# TODO: XBMC - Fake APIs!
# ================================================

# def addDir(name,url,mode,iconimage):
#   print('------------------------')
#   print(name)
#   print('- URL: ' + url)
#   print('- MODE: ' + str(mode))
#   print('- Icon: ' + iconimage)
#   print('------------------------ \n')

# def playMedia(name,url,iconimage):
#   ok=True
#   print('------------Play Media (Mock) ------------')
#   print(name)
#   print('- URL: ' + url)
#   print('- Icon: ' + iconimage)
#   print('------------------------ \n')
#   return ok

# def endOfItemList(isThumbnail=True):
#   if isThumbnail == True:
#     print('endOfItemList(isThumbnail=True)\n')
#   return True

# ================================================


rootURL = "http://phim.megabox.vn/"
browsers = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}
suffixURL = '|' + urllib.urlencode(browsers)
# TODO: Hard code
mediaKindList = [('phim-le/', 'Phim lẻ'), ('phim-bo/', 'Phim bộ'), ('show/', 'Show'), ('clip/', 'Clip')]

# TODO: Uncomment!
mysettings=xbmcaddon.Addon(id='plugin.video.salemmax.megabox')
home=mysettings.getAddonInfo('path')
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
resources=os.path.join(home, 'resources')
tempFilepath=xbmc.translatePath(os.path.join(resources, 'tempfile.txt'))

# ------------------- Utils ----------------------
def encodeURL(url):
  return unicodedata.normalize('NFKD', url.decode('UTF-8')).encode('ascii', 'ignore')

def normalYoutubeLink(url):
  normal = 'https://www.youtube.com/watch?v='
  plugin = 'plugin://plugin.video.youtube/?action=play_video&videoid='
  return url.replace(normal, plugin)

# TODO: Uncomment!
def endOfItemList(showThumbnail=True):
  # Display channels as thumbnail as default.
  if showThumbnail == True:
    xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)
  # End of directory.
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

def readTempfile():
  if os.path.isfile(tempFilepath):
    with open(tempFilepath, "r") as f:
      for line in f:
        # print('----->' + line + '<-----')
        if line != '' and line != '\n':
          # Read just first line (not empty)
          # print('-----> Return: ' + str(line))
          return line
  return 'hcmlike'

def writeTempfile(content='hcmlike'):
  text_file = open(tempFilepath, "w")
  text_file.write(content)
  text_file.close()

# ------------------- FUNCTIONs -----------------------

def getPageContent(url, json=False):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0')
  response = urllib2.urlopen(req)
  if json == True:
    import json
    content = json.load(response)
  else:
    content = response.read()
  response.close()
  return content

def getFilmTypeList(url):
  content = getPageContent(url)
  pattern = '<li><a href="(.+?)" title="">(.+?)</a></li>'
  pageLinks = re.compile(pattern).findall(str(content))
  filmTypeList = []
  for (relativeLink, name) in pageLinks:
    link = url + relativeLink + '/'
    filmTypeList.append((name, link))
  return filmTypeList

# Note: Not include media link now. It will get when user selects a link of film.
def getFilmInfoList(url, isGetPaging=False):
  # print("--------- getFilmInfoList: " + url)
  content = getPageContent(url)
  pattern ='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
  pageLinks = re.compile(pattern).findall(str(content))
  filmInfoList = []
  for (link, title, thumb) in pageLinks:
    # print('- Title : ' + title)
    # print('- URL : ' + link)
    # print('- Thumb: ' + thumb)
    filmInfoList.append((title, link, thumb))
  
  # Paging
  if isGetPaging == True:
    paging = (1, 1)
    pattern = '<span></span>Trang (.+?)/(.+?)</div>'
    pagings = re.compile(pattern).findall(str(content))
    if len(pagings) > 0:
      (startPage, endPage) = pagings[0]
      paging = (int(startPage), int(endPage))
    return (filmInfoList, paging)
  return filmInfoList

def getEpisodeInfoList(pageURL):
  content = getPageContent(pageURL)
  # <li><a id=eps-ID href='PAGE' >TAP-PHIM</a></li>
  pattern = "<li><a id=eps-(.+?) href='(.+?)' >(.+?)</a></li>"
  pageLinks = re.compile(pattern).findall(str(content))
  epsInfoList = []
  for (epsId, link, eps) in pageLinks:
    epsInfoList.append((eps, link))
  return epsInfoList

def getTitle(link, content):
  pattern = '<a href="' + link + '">(.+?)</a>'
  pageLinks = re.compile(pattern).findall(str(content))
  return pageLinks[0]

def getMediaLink(url):
  content = getPageContent(url)
  pattern = 'var iosUrl = "(.+?)";'
  links = re.compile(pattern).findall(str(content))
  mediaLink = ''
  if len(links) > 0:
    mediaLink = links[0]
    if 'youtube' in mediaLink:
      mediaLink = normalYoutubeLink(mediaLink)
    else:
      mediaLink = mediaLink + suffixURL
  return mediaLink

def convertVNChars2NoAccent(str):
  try:
    if str == '': return
    if type(str).__name__ == 'unicode': str = str.encode('utf-8')
    list_pat = ["á|à|ả|ạ|ã|â|ấ|ầ|ẩ|ậ|ẫ|ă|ắ|ằ|ẳ|ặ|ẵ", "Á|À|Ả|Ạ|Ã|Â|Ấ|Ầ|Ẩ|Ậ|Ẫ|Ă|Ắ|Ằ|Ẳ|Ặ|Ẵ",
      "đ", "Đ", "í|ì|ỉ|ị|ĩ", "Í|Ì|Ỉ|Ị|Ĩ", "é|è|ẻ|ẹ|ẽ|ê|ế|ề|ể|ệ|ễ", "É|È|Ẻ|Ẹ|Ẽ|Ê|Ế|Ề|Ể|Ệ|Ễ",
      "ó|ò|ỏ|ọ|õ|ô|ố|ồ|ổ|ộ|ỗ|ơ|ớ|ờ|ở|ợ|ỡ", "Ó|Ò|Ỏ|Ọ|Õ|Ô|Ố|Ồ|Ổ|Ộ|Ỗ|Ơ|Ớ|Ờ|Ở|Ợ|Ỡ",
      "ú|ù|ủ|ụ|ũ|ư|ứ|ừ|ử|ự|ữ", "Ú|Ù|Ủ|Ụ|Ũ|Ư|Ứ|Ừ|Ử|Ự|Ữ", "ý|ỳ|ỷ|ỵ|ỹ", "Ý|Ỳ|Ỷ|Ỵ|Ỹ"]
    list_re = ['a', 'A', 'd', 'D', 'i', 'I', 'e', 'E', 'o', 'O', 'u', 'U', 'y', 'Y']
    for i in range(len(list_pat)):
      str = re.sub(list_pat[i], list_re[i], str)
    return str
  except:
    traceback.print_exc()
  return str

def normalKeyword(keyword):
  keyword = convertVNChars2NoAccent(keyword)
  return re.sub("\s+","-",keyword)

def genTitleByPageNum(currentPageNum, endPageNum):
  return 'Trang ' + str(currentPageNum) + '/' + str(endPageNum)

def getPageNumByTitle(title):
  pattern = 'Trang (\d{,4})/(\d{,4})'
  pagings = re.compile(pattern).findall(str(title))
  (strCurrentPage, strEndPage) = pagings[0]
  return (int(strCurrentPage), int(strEndPage))

def buildPageByPageNum(url, title=''):
  mode = 1 # for both Phim bo & Phim le
  if title == '':
    (filmInfoList, (currentPage, endPage)) = getFilmInfoList(url, True)
  else:
    (currentPage, endPage) = getPageNumByTitle(title)
    pageUrl = url + 'trang-' + str(currentPage)
    filmInfoList = getFilmInfoList(pageUrl)

  # get more pages for a screen.
  # TODO: setting variable
  morePage = 1
  pagesLinkList = []
  pagesLinkList.append(filmInfoList)
  
  if endPage - currentPage >= morePage:
    upperPage = currentPage + morePage
  else:
    upperPage = endPage
  pageIndex = currentPage
  for pageIndex in range(currentPage + 1, upperPage + 1): # skip currentPage
    pageUrl = url + 'trang-' + str(pageIndex)
    filmInfoList = getFilmInfoList(pageUrl)
    pagesLinkList.append(filmInfoList)
  currentPage = pageIndex

  for filmInfoList in pagesLinkList:
    if len(filmInfoList) > 0:
      for (title, link, thumbnail) in filmInfoList:
        addDir(title, link, mode, thumbnail)

  # Add paging
  if currentPage < endPage:
    nextPage = currentPage + 1
    title = genTitleByPageNum(nextPage, endPage)
    mode = 5
    addDir(title, url, mode)
  return True

def buildMediaDir(url):
  mode = 1 # Support all video type.
  filmInfoList = getFilmInfoList(url)
  if len(filmInfoList) <= 0:
    return False
  for (title, link, thumbnail) in filmInfoList:
    addDir(title, link, mode, thumbnail)
  return True

def buildMedia4Eps(dirnameURL, ajaxEpsURL, thumbnail):
  # ajaxEpsURL = 'http://phim.megabox.vn/content/ajax_episode?id=8228&start=631'
  mode = 1
  content = getPageContent(ajaxEpsURL, json=True)
  for item in content:
    name = item['name'].encode('utf-8')
    # bannerImg = 'http://img.phim.megabox.vn/728x409' + item['image_banner']
    url = dirnameURL + '/%s-%s.html' % (item['cat_id'], item['content_id'])
    addDir(name, url, mode, thumbnail)

def buildCategory(url, mediaKind):
  mode = 2
  # print("================================= Category for %s =============================" % mediaKind)
  pattern = "<li><a  title='.+?'.+? href='(%s.+?)'>(.+?)</a></li>" % mediaKind
  content = getPageContent(url)
  infoList = re.compile(pattern).findall(content)
  # flist = []
  tmplinks = []
  for (relativeLink, title) in infoList:
    link = url + relativeLink + '/'
    if link not in tmplinks:
      tmplinks.append(link)
      # flist.append((title, link))
      addDir(title, link, mode)
  # return flist
  return True

# ============================================ SCREENs ===================================================

# mode = 0
def homeScreen(url):
  ok=True
  labels = []
  filmTypeList = getFilmTypeList(url)
  if len(filmTypeList) > 0:
    mode = 2
    for (filmType, filmLink) in filmTypeList:
      labels.append((filmType, filmLink, mode))

    # Tìm phim
    mode = 4
    filmType = "Tìm Phim"
    filmLink = url + "tim-kiem/"
    labels.append((filmType, filmLink, mode))

    # Tìm phim trên Youtube
    #mode = 6
    #filmType = "Tìm phim trên HCMLIKE Youtube"
    #filmLink = 'https://www.youtube.com/results?search_query='
    #labels.append((filmType, filmLink, mode))

  # For labels
  for (title, link, mode) in labels:
    addDir(title, link, mode)

  # For films
  for (title, link, mode) in labels:
    if 'phim-le' in link or 'phim-bo' in link:
      buildMediaDir(link)

  endOfItemList()
  return ok

# mode = 1: Handle all video types: Phim bo, Phim le, Show & Clip
def handleMedia(title, filmLink, thumbnail):
  mediaLink = getMediaLink(filmLink)
  if mediaLink == '':
    return episodesScreen(title, filmLink, thumbnail)
  else:
    return playMedia(title, mediaLink, thumbnail)

# mode = 2
def displayMediaScreen(url):
  # print('----------> ' + url)
  ok = buildPageByPageNum(url)
  for (mediaKind, name) in mediaKindList:
    if mediaKind in url:
      buildCategory(rootURL, mediaKind)
  endOfItemList()
  return ok


# mode = 5
def pagingScreen(url, title=''):
  ok = buildPageByPageNum(url, title)
  endOfItemList()
  return ok

# mode = 3
def episodesScreen(title, url, thumbnail):
  dirnameURL = os.path.dirname(url)
  content = getPageContent(url)
  # <a onclick="getListEps(8228,1, 30,this);" class="active" href='javascript:void(0);'>1-30</a>
  pattern = '<a onclick=.getListEps\((.+?)\).{,25} href=.{,25}>(.+?)</a>'
  links = re.compile(pattern).findall(content)
  showThumbnail = True
  count = 0
  for (epsInfo, currEps) in links:
    count = count + 1
    tmps = epsInfo.split(',')
    epsId = tmps[0].strip()
    epsStart = tmps[1].strip()
    ajaxEpsURL = 'http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s' % (epsId, epsStart)
    buildMedia4Eps(dirnameURL, ajaxEpsURL, thumbnail)
  if count > 1:
    showThumbnail = False
  endOfItemList(showThumbnail)
  return True

# mode = 4
def searchFilm(url):
  ok = True
  searchText = ''
  # TODO: Uncomment!
  try:
    keyb=xbmc.Keyboard('', '[COLOR lime]NHẬP TÊN PHIM CẦN TÌM KIẾM[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
      searchText = normalKeyword(keyb.getText())
  except: pass
  url = url + searchText + '/'
  buildMediaDir(url)

  # For more search
  for (kind, name) in mediaKindList:
    link = url + kind
    mode = 2
    title = 'Tìm kiếm theo ' + name
    addDir(title, link, mode)

  endOfItemList()
  return ok

# mode = 6
def searchFilmOnYoutube(url):
  ok = True
  mode = 7
  keyword = readTempfile()
  searchText = 'hcmlike'
  # TODO: Uncomment!
  try:
    keyb=xbmc.Keyboard(keyword, '[COLOR lime]NHẬP TÊN PHIM CẦN TÌM KIẾM[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
      searchText = keyb.getText()
      writeTempfile(searchText)
      searchText = urllib.quote_plus(searchText)
  except: pass
  url = url + searchText
  base = 'https://www.youtube.com'
  infoList = []
  while len(infoList) <= 0:
    content = getPageContent(url)
    pattern = '<div class=".+"><a .+ href="(.+?)" class=".+".+<img src="(.+?jpg)" .*width="196" height="110"/></div>.+\n.+\n.+\n\n\n.+\n.+\n.+data-sessionlink=".+" title=".+" rel=".+" aria-describedby=".+" dir="ltr">(.+?)</a><span'
    infoList = re.compile(pattern).findall(str(content))
  for (href, img, title) in infoList:
    link = base + href
    data_thumb = '" data-thumb="'
    if data_thumb in img:
      img = img.split(data_thumb)[1]
    thumbnail = 'http:' + img
    addDir(title, link, mode, thumbnail)
  endOfItemList()
  return ok

# mode = 7
def build4SelectedVideo(title, url, thumbnail):
  mode = 8
  addDir(title, url, mode, thumbnail)
  addRelatedVideos(url)
  endOfItemList()
  return True

# support for mode = 7
def addRelatedVideos(url):
  mode = 8
  base = 'https://www.youtube.com'
  content = getPageContent(url)  
  pattern = '<a href="(.+?)" class=".+" title=".+" data-sessionlink=".+" >  <span dir="ltr" class="title" aria-describedby=".+">\n(.+?)\n.*</span>'
  for i in range(17):
    pattern = pattern + '.*\n'
  pattern = pattern + '.*data-thumb="(.+?)"'

  infoList = re.compile(pattern).findall(str(content))
  for (href, title, img) in infoList:
    title = title.strip()
    link = base + href
    thumbnail = 'http:' + img
    addDir(title, link, mode, thumbnail)

# mode = 8
def playYoutubeVideo(title, url, thumbnail):
  mediaLink = normalYoutubeLink(url)
  return playMedia(title, mediaLink, thumbnail)

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

def setResolvedUrl(url):
  item=xbmcgui.ListItem(path=url)
  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

# TODO: Uncomment!
def playMedia(name,url,iconimage):
  # print('----- playMedia: ' + url)
  url = url.replace('media21.megabox.vn', '113.164.28.47')
  url = url.replace('media22.megabox.vn', '113.164.28.48')
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  # setResolvedUrl(url)
  xbmc.Player().play(url, liz)
  return True

def addLink(name,url,iconimage,mode=0):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumbnail="+urllib.quote_plus(iconimage)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
  return ok

# TODO: Uncomment!
def addDir(name,url,mode,iconimage=icon):
  # print('------------------------')
  # print(name)
  # print('- URL: ' + url)
  # print('- MODE: ' + str(mode))
  # print('- Icon: ' + iconimage)
  # print('------------------------ \n')
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumbnail="+urllib.quote_plus(iconimage)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('Fanart_Image',fanart)
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok

# TODO: Uncomment!
params = get_params()

url = None
name = None
mode = None
thumbnail = ''

# TODO: Uncomment!
try:
  url = urllib.unquote_plus(params["url"])
except:
  pass
try:
  name = urllib.unquote_plus(params["name"])
except:
  pass
try:
  mode = int(params["mode"])
except:
  pass
try:
  thumbnail = urllib.unquote_plus(params["thumbnail"])
except:
  pass

# ------------------------------- MODE SELECTION -----------------------------------

# mode = 0
if mode == None or url == None or len(url) < 1:
  homeScreen(rootURL)

elif mode == 1:
  handleMedia(name, url, thumbnail)

# Display media screen for all video types
elif mode == 2:
  displayMediaScreen(url)

# Display all episodes of a "Phim Bo"
elif mode == 3:
  episodesScreen(name, url, thumbnail)

# For searching film
elif mode == 4:
  searchFilm(url)

elif mode == 5:
  pagingScreen(url, name)

# For searching film on Youtube
elif mode == 6:
  searchFilmOnYoutube(url)

elif mode == 7:
  build4SelectedVideo(name, url, thumbnail)

elif mode == 8:
  playYoutubeVideo(name, url, thumbnail)
