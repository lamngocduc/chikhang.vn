#!/usr/bin/env python
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

from xbmcswift2 import Plugin, xbmcaddon, xbmc, xbmcgui
import urlfetch
from BeautifulSoup import BeautifulSoup
import json, re

xbmcplugin = Plugin()
__mysettings__ = xbmcaddon.Addon(id='plugin.video.salemmax.fptplay')
__homeUrl__ = 'http://fptplay.net/livetv'

reg = {
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        		   'Content-type': 'application/x-www-form-urlencoded',
        		   'X-Requested-With': 'XMLHttpRequest',
                   'Referer' : 'http://fptplay.net'
            }

@xbmcplugin.route('/')
def main():
    channel = []
    result = urlfetch.fetch(__homeUrl__,headers=reg)
    soup = BeautifulSoup(result.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.findAll('div', {'class' : 'item_view'})
    for item in items:
            
        common = item.find('a', {'class' : 'tv_channel '})
        if common == None :
          common = item.find('a', {'class' : 'tv_channel active'})

        lock = item.find('img', {'class' : 'lock'})
        if lock == None :

          title = common.get('title')       
          url = common.get('data-href')
          thumb = common.find('img',{'class':'img-responsive'}).get('data-original')
          thumb = thumb.split('?')
          if 'giai-tri-tv' in url or 'phim-viet' in url or 'the-thao-tv-hd' in url or 'kenh-17' in url or 'e-channel' in url or 'hay-tv' in url or 'ddramas' in url or 'bibi' in url or 'o2-tv' in url or 'info-tv' in url or 'style-tv' in url or 'invest-tv' in url or 'yeah1' in url:
            pass
          else :		  
            data = {
                'label': title.replace('-',' '),
                'path': xbmcplugin.url_for('plays', id = url.replace('http://fptplay.net/livetv/','')),
                'thumbnail':thumb[0],
                'is_playable': True
                }
            channel.append(data)

    xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)		
    return xbmcplugin . finish ( channel )

def resolveUrl(id = None):
    getUrl = 'http://fptplay.net/show/getlinklivetv?id=%s&type=newchannel&quality=1&mobile=web'
    result = urlfetch.post(
        getUrl,
        data={"id": id,
            "quality": __mysettings__.getSetting('quality'),
            "mobile": "web"
            },
        headers=reg
        )
    jsonObject = json.loads(result.content)
    return jsonObject['stream']

@xbmcplugin.route('/plays/<id>')
def plays(id):
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('ITV Plus', 'Đang tải. Vui lòng chờ trong giây lát...')
    xbmcplugin.set_resolved_url(resolveUrl(id))
    dialogWait.close()
    del dialogWait
    
if __name__ == '__main__':
    xbmcplugin.run()
    
