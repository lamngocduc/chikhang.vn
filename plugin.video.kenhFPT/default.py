import CommonFunctions as common
import urllib
import urllib2
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import urlfetch
import re
import json
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.kenhFPT')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
thumbnails = xbmc.translatePath( os.path.join( home, 'thumbnails\\' ) )

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
			cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader

def make_request(url, headers=None):
	if headers is None:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
								 'Referer' : 'http://www.google.com'}
	try:
			req = urllib2.Request(url,headers=headers)
			f = urllib2.urlopen(req)
			body=f.read()
			return body
	except urllib2.URLError, e:
			print 'We failed to open "%s".' % url
			if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					print 'Reason: ', e.reason
			if hasattr(e, 'code'):
					print 'We failed with error code - %s.' % e.code

def get_categories():
    
	add_link('', '[COLOR lime]salemmax FPT[/COLOR]', 0, 'udp://@225.1.1.2:30120', thumbnails + 'fpt.png', '')
	add_link('', '[COLOR lime]K+NS SD[/COLOR]', 0, 'udp://@225.1.1.142:30120', thumbnails + 'k+nst.png', '')
	add_link('', '[COLOR lime]K+PC SD[/COLOR]', 0, 'udp://@225.1.1.139:30120', thumbnails + 'k+pc.png', '')
	add_link('', '[COLOR lime]SCTV Hai HD[/COLOR]', 0, 'http://hlscache.fptplay.net.vn/livev/sctvhaihd_2000.stream/playlist.m3u8?token=c335VydmVyX3RpbWU9MTQwMjYxNzIyNCZoYXNoX3ZhbHVl&did=NzIyNCZoYXNoX3ZhbHVl', thumbnails + 'sctvhaihd.png', '')
	add_link('', '[COLOR lime]SCTV 14[/COLOR]', 0, 'http://tvod.accessasia.tv:8080/live/sctv14.480p/index.m3u8', thumbnails + 'sctv14.png', '')
	add_link('', '[COLOR lime]SCTV 5[/COLOR]', 0, 'udp://@225.1.1.9:30120', thumbnails + 'sctv5.png', '')
	add_link('', '[COLOR lime]VTV1 HD[/COLOR]', 0, 'udp://@225.1.2.249:30120', thumbnails + 'VTV1 HD.png', '')
	add_link('', '[COLOR lime]VTV2[/COLOR]', 0, 'udp://@225.1.1.249:30120', thumbnails + 'VTV2.png', '')
	add_link('', '[COLOR lime]VTV3 HD[/COLOR]', 0, 'udp://@225.1.2.247:30120', thumbnails + 'VTV3 HD.png', '')
	add_link('', '[COLOR lime]VTV4[/COLOR]', 0, 'udp://@225.1.1.248:30120', thumbnails + 'VTV4.png', '')
	add_link('', '[COLOR lime]VTV5[/COLOR]', 0, 'udp://@225.1.1.247:30120', thumbnails + 'VTV5.png', '')
	add_link('', '[COLOR lime]VTV6 HD[/COLOR]', 0, 'udp://@225.1.2.245:30120', thumbnails + 'VTV6 HD.png', '')
	add_link('', '[COLOR lime]NHÂN DÂN[/COLOR]', 0, 'udp://@225.1.1.91:30120', thumbnails + 'NHAN DAN.png', '')
	add_link('', '[COLOR lime]VTC3 HD[/COLOR]', 0, 'udp://@225.1.2.251:30120', thumbnails + 'vtc3hd.png', '')
	add_link('', '[COLOR lime]VTC HD2[/COLOR]', 0, 'udp://@225.1.2.253:30120', thumbnails + '2vtchd.png', '')
	add_link('', '[COLOR lime]VTC HD3[/COLOR]', 0, 'udp://@225.1.2.252:30120', thumbnails + '3vtchd.png', '')
	add_link('', '[COLOR lime]VTC1 HD[/COLOR]', 0, 'udp://@225.1.2.254:30120', thumbnails + 'vtc1hd.png', '')
	add_link('', '[COLOR lime]VTC2[/COLOR]', 0, 'udp://@225.1.2.202:30120', thumbnails + 'vtc2.png', '')
	add_link('', '[COLOR lime]VTC4 HD[/COLOR]', 0, 'udp://@225.1.2.200:30120', thumbnails + 'vtc4yeah.jpg', '')
	add_link('', '[COLOR lime]VTC5[/COLOR]', 0, 'udp://@225.1.2.199:30120', thumbnails + 'vtc5.png', '')
	add_link('', '[COLOR lime]VTC6[/COLOR]', 0, 'udp://@225.1.2.198:30120', thumbnails + 'vtc6.png', '')
	add_link('', '[COLOR lime]VTC 7 TodayTV[/COLOR]', 0, 'udp://@225.1.2.197:30120', thumbnails + 'vtc7.png', '')
	add_link('', '[COLOR lime]VTC8[/COLOR]', 0, 'udp://@225.1.2.196:30120', thumbnails + 'vtc8.png', '')
	add_link('', '[COLOR lime]VTC9 LETS VIET[/COLOR]', 0, 'udp://@225.1.2.195:30120', thumbnails + 'vtc9.png', '')
	add_link('', '[COLOR lime]VTC10[/COLOR]', 0, 'udp://@225.1.2.194:30120', thumbnails + 'vtc10.png', '')
	add_link('', '[COLOR lime]VTC 11 KIDSTV FAMILY[/COLOR]', 0, 'udp://@225.1.2.193:30120', thumbnails + 'vtc11.png', '')
	add_link('', '[COLOR lime]VTC 12[/COLOR]', 0, 'udp://@225.1.2.192:30120', thumbnails + 'vtc12.png', '')
	add_link('', '[COLOR lime]VTC13-iTV SD[/COLOR]', 0, 'udp://@225.1.2.189:30120', thumbnails + 'vtc13sd.jpg', '')
	add_link('', '[COLOR lime]VTC13-iTV HD[/COLOR]', 0, 'udp://@225.1.2.250:30120', thumbnails + 'vtc13.jpg', '')
	add_link('', '[COLOR lime]VTC 14[/COLOR]', 0, 'udp://@225.1.2.191:30120', thumbnails + 'vtc14.png', '')
	add_link('', '[COLOR lime]VTC 14[/COLOR]', 0, 'udp://@225.1.2.88:30120', thumbnails + 'vtc14hd.png', '')
	add_link('', '[COLOR lime]VTC 16[/COLOR]', 0, 'udp://@225.1.2.190:30120', thumbnails + 'vtc16.png', '')
	add_link('', '[COLOR lime]THETHAO TV HD[/COLOR]', 0, 'udp://@225.1.2.241:30120', thumbnails + 'htvcthethaotvhd.png', '')
	add_link('', '[COLOR lime]THETHAO TV[/COLOR]', 0, 'udp://@225.1.2.158:30120', thumbnails + 'vtvcab3.png', '')
	add_link('', '[COLOR lime]BONGDA TV HD[/COLOR]', 0, 'udp://@225.1.2.243:30120', thumbnails + 'vtccabbongdahd.png', '')
	add_link('', '[COLOR lime]BONGDA TV[/COLOR]', 0, 'udp://@225.1.2.160:30120', thumbnails + 'vtvcab-16.png', '')
	add_link('', '[COLOR lime]VTVCab 1-Giai tri TV[/COLOR]', 0, 'udp://@225.1.2.150:30120', thumbnails + 'vtvcab1.png', '')
	add_link('', '[COLOR lime]VTVCab 2-Phim Viet[/COLOR]', 0, 'udp://@225.1.2.159:30120', thumbnails + 'vtvcab2.png', '')
	add_link('', '[COLOR lime]VTVCab 4-Van Hoa[/COLOR]', 0, 'udp://@225.1.2.153:30120', thumbnails + 'vanhoa.png', '')
	add_link('', '[COLOR lime]VTVCab 5-E channel[/COLOR]', 0, 'udp://@225.1.2.156:30120', thumbnails + 'vtvcab5.png', '')
	add_link('', '[COLOR lime]VTVCab 6-HayTV[/COLOR]', 0, 'udp://@225.1.1.254:30120', thumbnails + 'vtvcab6.png', '')
	add_link('', '[COLOR lime]VTVCab 7-D Dramas[/COLOR]', 0, 'udp://@225.1.2.157:30120', thumbnails + 'vtvcab7.png', '')
	add_link('', '[COLOR lime]VTVCab8-BiBi[/COLOR]', 0, 'udp://@225.1.2.161:30120', thumbnails + 'vtvcab8.png', '')
	add_link('', '[COLOR lime]VTVCab9-InfoTV[/COLOR]', 0, 'udp://@225.1.2.154:30120', thumbnails + 'vtvcab9.png', '')
	add_link('', '[COLOR lime]VTVCab10-O2TV[/COLOR]', 0, 'udp://@225.1.2.152:30120', thumbnails + 'vtvcab10.png', '')
	add_link('', '[COLOR lime]VTVCab11-TV Shopping[/COLOR]', 0, 'udp://@225.1.1.252:30120', thumbnails + 'vtvcab11.png', '')
	add_link('', '[COLOR lime]VTVCab12-StyleTV[/COLOR]', 0, 'udp://@225.1.2.155:30120', thumbnails + 'vtvcab-12.png', '')
	add_link('', '[COLOR lime]VTVCab14-Homeshopping[/COLOR]', 0, 'udp://@225.1.1.253:30120', thumbnails + 'vtvcab14.png', '')
	add_link('', '[COLOR lime]VTVCab15-InvestTV[/COLOR]', 0, 'udp://@225.1.1.251:30120', thumbnails + 'vtvcab-15.png', '')
	add_link('', '[COLOR lime]VTVCab17-Yeah1!TV[/COLOR]', 0, 'udp://@225.1.2.151:30120', thumbnails + 'vtvcab-17.png', '')
	add_link('', '[COLOR lime]VTV CAB 20[/COLOR]', 0, 'udp://@225.1.1.15:30120', thumbnails + 'vtvcab20.png', '')
	add_link('', '[COLOR lime]HANAM[/COLOR]', 0, 'udp://@225.1.1.63:30120', thumbnails + 'hanam.jpg', '')
	add_link('', '[COLOR lime]Hanoicab HiTV[/COLOR]', 0, 'udp://@225.1.2.91:30120', thumbnails + 'hanoicatvhitv.png', '')
	add_link('', '[COLOR lime]HanoiCab MOV HD[/COLOR]', 0, 'udp://@225.1.1.206:30120', thumbnails + 'hanoicatvmov.png', '')
	add_link('', '[COLOR lime]Hanoicab You[/COLOR]', 0, 'udp://@225.1.1.207:30120', thumbnails + 'htvcyoutv.png', '')
	add_link('', '[COLOR lime]HANOICABVNK[/COLOR]', 0, 'udp://@225.1.2.93:30120', thumbnails + 'hanoicabvnk.png', '')
	add_link('', '[COLOR lime]HTV1[/COLOR]', 0, 'udp://@225.1.1.180:30120', thumbnails + 'htv1.png', '')
	add_link('', '[COLOR lime]HTV2 HD[/COLOR]', 0, 'udp://@225.1.1.193:30120', thumbnails + 'htv2hd.png', '')
	add_link('', '[COLOR lime]HTV3[/COLOR]', 0, 'udp://@225.1.1.178:30120', thumbnails + 'htv3.png', '')
	add_link('', '[COLOR lime]HTV4[/COLOR]', 0, 'udp://@225.1.1.177:30120', thumbnails + 'htv4.png', '')
	add_link('', '[COLOR lime]HTV7 HD[/COLOR]', 0, 'udp://@225.1.1.192:30120', thumbnails + 'htv7hd.png', '')
	add_link('', '[COLOR lime]HTV9 HD[/COLOR]', 0, 'udp://@225.1.1.190:30120', thumbnails + 'htv9hd.png', '')
	add_link('', '[COLOR lime]HTVC Thuan Viet HD[/COLOR]', 0, 'udp://@225.1.1.186:30120', thumbnails + 'htvthuanviet_hd.png', '')
	add_link('', '[COLOR lime]HTVC Thuan Viet SD[/COLOR]', 0, 'udp://@225.1.1.174:30120', thumbnails + 'htvthuan_viet.png', '')
	add_link('', '[COLOR lime]HTVC PHIM HD[/COLOR]', 0, 'udp://@225.1.1.184:30120', thumbnails + 'htvc_moviehd.png', '')
	add_link('', '[COLOR lime]FBNC HD[/COLOR]', 0, 'udp://@225.1.1.182:30120', thumbnails + 'htvcfbnc.png', '')
	add_link('', '[COLOR lime]HTVC Shop[/COLOR]', 0, 'udp://@225.1.1.172:30120', thumbnails + 'htvcshopping.png', '')
	add_link('', '[COLOR lime]HTV The Thao[/COLOR]', 0, 'udp://@225.1.1.165:30120', thumbnails + 'htvthethao.png', '')
	add_link('', '[COLOR lime]HTVC Gia dinh[/COLOR]', 0, 'udp://@225.1.1.170:30120', thumbnails + 'htvgiadinh.png', '')
	add_link('', '[COLOR lime]HTVC Phu nu TV[/COLOR]', 0, 'udp://@225.1.1.171:30120', thumbnails + 'htvcphunu.png', '')
	add_link('', '[COLOR lime]HTVC Du lich Cuoc song[/COLOR]', 0, 'udp://@225.1.1.166:30120', thumbnails + 'htvcdulichvacuocsong.png', '')
	add_link('', '[COLOR lime]MTV[/COLOR]', 0, 'udp://@225.1.1.245:30120', thumbnails + 'htvcmtv.png', '')
	add_link('', '[COLOR lime]An Ninh The Gioi[/COLOR]', 0, 'udp://@225.1.1.208:30120', thumbnails + 'ananinhthegioi.jpg', '')
	add_link('', '[COLOR lime]NCM BYV10[/COLOR]', 0, 'udp://@225.1.1.225:30120', thumbnails + 'vag 1.jpg', '')
	add_link('', '[COLOR lime]PHIM HAY[/COLOR]', 0, 'udp://@225.1.1.222:30120', thumbnails + 'phimhay.png', '')
	add_link('', '[COLOR lime]Mien Tay[/COLOR]', 0, 'udp://@225.1.1.221:30120', thumbnails + 'avg 2.jpg', '')
	add_link('', '[COLOR lime]Viet Teen[/COLOR]', 0, 'udp://@225.1.1.223:30120', thumbnails + 'AVGvietteen.jpg', '')
	add_link('', '[COLOR lime]SAM CHANNEL[/COLOR]', 0, 'udp://@225.1.1.224:30120', thumbnails + 'AVGsam.jpg', '')
	add_link('', '[COLOR lime]BTV 1[/COLOR]', 0, 'udp://@225.1.1.150:30120', thumbnails + 'binhduong1.png', '')
	add_link('', '[COLOR lime]BTV 2[/COLOR]', 0, 'udp://@225.1.1.149:30120', thumbnails + 'binhduong2.png', '')
	add_link('', '[COLOR lime]BTV 3[/COLOR]', 0, 'http://112.197.2.135:1935/mslive2/C068_SD_4/chunklist.m3u8?us=7a480a96b3bde30f79227d8a24fe932d2bdec25c4070347c2c604495330ed8f7388fd6886b6ebe81e177d60ab5dd63b4-545681', thumbnails + 'binhduong3.png', '')
	add_link('', '[COLOR lime]BTV 4[/COLOR]', 0, 'udp://@225.1.1.29:30120', thumbnails + 'binhduong4.png', '')
	add_link('', '[COLOR lime]BTV 5[/COLOR]', 0, 'http://112.197.2.135:1935/mslive2/C069_SD_4/chunklist.m3u8?us=7a480a96b3bde30f79227d8a24fe932d2bdec25c4070347c2c604495330ed8f7388fd6886b6ebe81e177d60ab5dd63b4-545681', thumbnails + 'binhduong5.png', '')
	add_link('', '[COLOR lime]QUOC HOI HD[/COLOR]', 0, 'udp://@225.1.2.148:30120', thumbnails + 'Quoc Hoi.png', '')
	add_link('', '[COLOR lime]QPVN HD[/COLOR]', 0, 'udp://@225.1.2.217:30120', thumbnails + 'qpvnhd.png', '')
	add_link('', '[COLOR lime]ANTV[/COLOR]', 0, 'udp://@225.1.2.169:30120', thumbnails + 'anninh.png', '')
	add_link('', '[COLOR lime]VTV Da Nang[/COLOR]', 0, 'udp://@225.1.2.166:30120', thumbnails + 'vtvdn.png', '')
	add_link('', '[COLOR lime]BTV BAC LIEU[/COLOR]', 0, 'udp://@225.1.1.61:30120', thumbnails + 'baclieu.png', '')
	add_link('', '[COLOR lime]HGTV Hau Giang[/COLOR]', 0, 'udp://@225.1.1.62:30120', thumbnails + 'haugiang.png', '')
	add_link('', '[COLOR lime]VTV Hue[/COLOR]', 0, 'udp://@225.1.1.105:30120', thumbnails + 'vtv hue.jpg', '')
	add_link('', '[COLOR lime]VTV Phu Yen[/COLOR]', 0, 'udp://@225.1.1.65:30120', thumbnails + 'vtv Phu Yen.jpg', '')
	add_link('', '[COLOR lime]TTXVN[/COLOR]', 0, 'udp://@225.1.1.167:30120', thumbnails + 'ttxvn.png', '')
	add_link('', '[COLOR lime]Vietnamnet[/COLOR]', 0, 'udp://@225.1.2.96:30120', thumbnails + 'vietnamnet.png', '')
	add_link('', '[COLOR lime]TTV Thanh Hoa[/COLOR]', 0, 'udp://@225.1.2.184:30120', thumbnails + 'thanhhoa.png', '')
	add_link('', '[COLOR lime]CTV Ca Mau[/COLOR]', 0, 'udp://@225.1.1.104:30120', thumbnails + 'camau.png', '')
	add_link('', '[COLOR lime]VOV Viet Nam[/COLOR]', 0, 'udp://@225.1.2.171:30120', thumbnails + 'vovtv.png', '')
	add_link('', '[COLOR lime]LTV LAM DONG[/COLOR]', 0, 'udp://@225.1.2.177:30120', thumbnails + 'lamdong.png', '')
	add_link('', '[COLOR lime]Ha Noi 1[/COLOR]', 0, 'udp://@225.1.2.97:30120', thumbnails + 'hanoi1.png', '')
	add_link('', '[COLOR lime]Ha Noi 2[/COLOR]', 0, 'udp://@225.1.1.125:30120', thumbnails + 'hanoi2.png', '')
	add_link('', '[COLOR lime]LA34 LONG AN[/COLOR]', 0, 'udp://@225.1.1.162:30120', thumbnails + 'longan.png', '')
	add_link('', '[COLOR lime]Vinh Long 1[/COLOR]', 0, 'udp://@225.1.1.155:30120', thumbnails + 'vinhlong1.png', '')
	add_link('', '[COLOR lime]Vinh Long 2[/COLOR]', 0, 'udp://@225.1.1.154:30120', thumbnails + 'vinhlong2.png', '')
	add_link('', '[COLOR lime]Da Nang 1[/COLOR]', 0, 'udp://@225.1.1.147:30120', thumbnails + 'danang1.png', '')
	add_link('', '[COLOR lime]Da Nang 2[/COLOR]', 0, 'udp://@225.1.1.146:30120', thumbnails + 'danang2.png', '')
	add_link('', '[COLOR lime]BRTV Vung Tau[/COLOR]', 0, 'udp://@225.1.2.175:30120', thumbnails + 'vungtau.png', '')
	add_link('', '[COLOR lime]BPTV Binh Phuoc 1[/COLOR]', 0, 'udp://@225.1.2.23:30120', thumbnails + 'binhphuoc1.png', '')
	add_link('', '[COLOR lime]BPTV Binh Phuoc 2[/COLOR]', 0, 'udp://@225.1.2.38:30120', thumbnails + 'binhphuoc2.png', '')
	add_link('', '[COLOR lime]Dong Nai 1[/COLOR]', 0, 'udp://@225.1.1.152:30120', thumbnails + 'dongnai1.png', '')
	add_link('', '[COLOR lime]Dong Nai 2[/COLOR]', 0, 'udp://@225.1.1.151:30120', thumbnails + 'dongnai2.png', '')
	add_link('', '[COLOR lime]Nam Dinh[/COLOR]', 0, 'udp://@225.1.1.120:30120', thumbnails + 'namdinh.png', '')
	add_link('', '[COLOR lime]THLC Lao Cai[/COLOR]', 0, 'udp://@225.1.1.119:30120', thumbnails + 'laocai.png', '')
	add_link('', '[COLOR lime]YTV Yen Bai[/COLOR]', 0, 'udp://@225.1.1.39:30120', thumbnails + 'yenbai.png', '')
	add_link('', '[COLOR lime]QTV Quan Tri[/COLOR]', 0, 'udp://@225.1.1.117:30120', thumbnails + 'quantri.png', '')
	add_link('', '[COLOR lime]Binh Thuan[/COLOR]', 0, 'udp://@225.1.1.124:30120', thumbnails + 'binhthuan.png', '')
	add_link('', '[COLOR lime]BTV Binh Thuan[/COLOR]', 0, 'udp://@225.1.1.145:30120', thumbnails + 'btv.png', '')
	add_link('', '[COLOR lime]KRT Kon Tum[/COLOR]', 0, 'udp://@225.1.1.36:30120', thumbnails + 'konkun.png', '')
	add_link('', '[COLOR lime]Hung Yen[/COLOR]', 0, 'udp://@225.1.1.118:30120', thumbnails + 'hungyen.png', '')
	add_link('', '[COLOR lime]NBTV NINH BINH[/COLOR]', 0, 'udp://@225.1.2.185:30120', thumbnails + 'ninhbinh.png', '')
	add_link('', '[COLOR lime]NTV NGHE AN[/COLOR]', 0, 'udp://@225.1.2.183:30120', thumbnails + 'nghean.png', '')
	add_link('', '[COLOR lime]QTV1 QUANG NINH 1[/COLOR]', 0, 'udp://@225.1.2.181:30120', thumbnails + 'quangninh1.png', '')
	add_link('', '[COLOR lime]QTV3 QUANG NINH 3[/COLOR]', 0, 'udp://@225.1.2.180:30120', thumbnails + 'quangninh3.png', '')
	add_link('', '[COLOR lime]THDT Dong Thap 1[/COLOR]', 0, 'udp://@225.1.1.163:30120', thumbnails + 'dongthap.png', '')
	add_link('', '[COLOR lime]THDT Dong Thap 2[/COLOR]', 0, 'udp://@225.1.1.221:30120', thumbnails + 'dongthap2.png', '')
	add_link('', '[COLOR lime]ATV1 AN GIANG[/COLOR]', 0, 'udp://@225.1.2.173:30120', thumbnails + 'angiang.png', '')
	add_link('', '[COLOR lime]THD 1 HAI DUONG[/COLOR]', 0, 'udp://@225.1.1.158:30120', thumbnails + 'haiduong.png', '')
	add_link('', '[COLOR lime]THGL GIA LAI[/COLOR]', 0, 'udp://@225.1.2.176:30120', thumbnails + 'gialai.PNG', '')
	add_link('', '[COLOR lime]THP HAI PHONG[/COLOR]', 0, 'udp://@225.1.2.187:30120', thumbnails + 'haiphong.png', '')
	add_link('', '[COLOR lime]THTG TIEN GIANG[/COLOR]', 0, 'udp://@225.1.2.170:30120', thumbnails + 'tiengiang.png', '')
	add_link('', '[COLOR lime]TN1 THAI NGUYEN[/COLOR]', 0, 'udp://@225.1.2.179:30120', thumbnails + 'thainguyen.png', '')
	add_link('', '[COLOR lime]TTV Tuyen Quang[/COLOR]', 0, 'udp://@225.1.2.188:30120', thumbnails + 'tuyenquang.png', '')
	add_link('', '[COLOR lime]TRT thua thien hue[/COLOR]', 0, 'udp://@225.1.1.161:30120', thumbnails + 'hue.png', '')
	add_link('', '[COLOR lime]THTV Tra Vinh[/COLOR]', 0, 'udp://@225.1.2.172:30120', thumbnails + 'travinh.png', '')
	add_link('', '[COLOR lime]HBTV HOA BINH[/COLOR]', 0, 'udp://@225.1.2.168:30120', thumbnails + 'HOA BINH.png', '')
	add_link('', '[COLOR lime]PTTH Kien Giang[/COLOR]', 0, 'udp://@225.1.2.182:30120', thumbnails + 'kiengiang.png', '')
	add_link('', '[COLOR lime]lang son[/COLOR]', 0, 'udp://@225.1.1.160:30120', thumbnails + 'langson.png', '')
	add_link('', '[COLOR lime]BGTV Bac Giang[/COLOR]', 0, 'udp://@225.1.1.164:30120', thumbnails + 'bacgiang.png', '')
	add_link('', '[COLOR lime]PTQ1 Quan Ngai[/COLOR]', 0, 'udp://@225.1.2.174:30120', thumbnails + 'quangngai1.png', '')
	add_link('', '[COLOR lime]QRT Quan nam[/COLOR]', 0, 'udp://@225.1.2.50:30120', thumbnails + 'quang-nam.png', '')
	add_link('', '[COLOR lime]HGTV Hau Gian[/COLOR]', 0, 'udp://@225.1.1.157:30120', thumbnails + 'haugiang.png', '')
	add_link('', '[COLOR lime]QBTV Quan Binh[/COLOR]', 0, 'udp://@225.1.2.164:30120', thumbnails + 'quangbinh.png', '')
	add_link('', '[COLOR lime]PTV Phu Tho[/COLOR]', 0, 'udp://@225.1.2.165:30120', thumbnails + 'phutho.png', '')
	add_link('', '[COLOR lime]DTV Dien Bien[/COLOR]', 0, 'udp://@225.1.1.74:30120', thumbnails + 'Dien Bien.png', '')
	add_link('', '[COLOR lime]HTTV Ha Tinh[/COLOR]', 0, 'udp://@225.1.1.75:30120', thumbnails + 'ha tinh.jpg', '')
	add_link('', '[COLOR lime]THTP Can Tho[/COLOR]', 0, 'udp://@225.1.1.132:30120', thumbnails + 'thtpct.png', '')
	add_link('', '[COLOR lime]VTV Can Tho[/COLOR]', 0, 'udp://@225.1.1.131:30120', thumbnails + 'vtvct1.png', '')
	add_link('', '[COLOR lime]TTV 11 Tay Ninh[/COLOR]', 0, 'udp://@225.1.1.130:30120', thumbnails + 'tayninh.png', '')
	add_link('', '[COLOR lime]KTV Khanh Hoa[/COLOR]', 0, 'udp://@225.1.1.133:30120', thumbnails + 'khanhhoa.png', '')
	add_link('', '[COLOR lime]STV 1 Soc Trang[/COLOR]', 0, 'udp://@225.1.1.159:30120', thumbnails + 'soctrang.png', '')
	add_link('', '[COLOR lime]THBT BAC NINH[/COLOR]', 0, 'udp://@225.1.1.156:30120', thumbnails + 'bac ninh.png', '')
	add_link('', '[COLOR lime]DRT DAK LAK[/COLOR]', 0, 'udp://@225.1.1.64:30120', thumbnails + 'daclac.png', '')
	add_link('', '[COLOR lime]Vinh Phuc[/COLOR]', 0, 'udp://@225.1.2.99:30120', thumbnails + 'vinhphuc.png', '')
	add_link('', '[COLOR lime]BTV Binh Dinh[/COLOR]', 0, 'udp://@225.1.1.40:30120', thumbnails + 'binhdinh.png', '')
	add_link('', '[COLOR lime]TBTV Thai Binh[/COLOR]', 0, 'udp://@225.1.1.99:30120', thumbnails + 'thaibinh.png', '')
	add_link('', '[COLOR lime]DISCOVEY[/COLOR]', 0, 'udp://@225.1.1.238:30120', thumbnails + 'discovery.png', '')
	add_link('', '[COLOR lime]Discovery World HD[/COLOR]', 0, 'udp://@225.1.2.223:30120', thumbnails + 'discoveryhd.png', '')
	add_link('', '[COLOR lime]National Geographic[/COLOR]', 0, 'udp://@225.1.1.244:30120', thumbnails + 'natgeo.png', '')
	add_link('', '[COLOR lime]National Geographic HD[/COLOR]', 0, 'udp://@225.1.2.235:30120', thumbnails + 'natgeohd.png', '')
	add_link('', '[COLOR lime]TLC[/COLOR]', 0, 'udp://@225.1.1.236:30120', thumbnails + 'tlc.png', '')
	add_link('', '[COLOR lime]ANIMAL PLANET[/COLOR]', 0, 'udp://@225.1.1.231:30120', thumbnails + 'animal-planet.png', '')
	add_link('', '[COLOR lime]DA VINCI[/COLOR]', 0, 'udp://@225.1.1.197:30120', thumbnails + 'davinci.png', '')
	add_link('', '[COLOR lime]Outdoor Channel HD[/COLOR]', 0, 'udp://@225.1.2.215:30120', thumbnails + 'outdoorchanelhd.png', '')
	add_link('', '[COLOR lime]Cinemax[/COLOR]', 0, 'udp://@225.1.1.230:30120', thumbnails + 'cinemax.png', '')
	add_link('', '[COLOR lime]DISNEY[/COLOR]', 0, 'udp://@225.1.1.232:30120', thumbnails + 'disneychanel.png', '')
	add_link('', '[COLOR lime]DISNEY JUNIOR[/COLOR]', 0, 'udp://@225.1.1.233:30120', thumbnails + 'disneyjunior.png', '')
	add_link('', '[COLOR lime]Channel News Asia[/COLOR]', 0, 'udp://@225.1.1.202:30120', thumbnails + 'ChannelNewsAsia.png', '')
	add_link('', '[COLOR lime]CNN[/COLOR]', 0, 'udp://@225.1.1.242:30120', thumbnails + 'cnn.png', '')
	add_link('', '[COLOR lime]DW[/COLOR]', 0, 'udp://@225.1.1.203:30120', thumbnails + 'dw.png', '')
	add_link('', '[COLOR lime]Arirang[/COLOR]', 0, 'udp://@225.1.1.201:30120', thumbnails + 'arirang.png', '')
	add_link('', '[COLOR lime]NHK WORLD[/COLOR]', 0, 'udp://@225.1.1.196:30120', thumbnails + 'nhk.png', '')
	add_link('', '[COLOR lime]TV5 MONDE[/COLOR]', 0, 'udp://@225.1.1.200:30120', thumbnails + 'tv5.png', '')
	add_link('', '[COLOR lime]BLOOMBERG[/COLOR]', 0, 'udp://@225.1.1.227:30120', thumbnails + 'bloomberg.png', '')
	add_link('', '[COLOR lime]DIVA[/COLOR]', 0, 'udp://@225.1.1.199:30120', thumbnails + 'diva.png', '')
	add_link('', '[COLOR lime]FOX SPORTS 2[/COLOR]', 0, 'udp://@225.1.1.241:30120', thumbnails + 'fox2.png', '')
	add_link('', '[COLOR lime]FOX SPORTS HD[/COLOR]', 0, 'udp://@225.1.2.229:30120', thumbnails + 'foxhd.png', '')
	add_link('', '[COLOR lime]Asian food channel[/COLOR]', 0, 'udp://@225.1.1.198:30120', thumbnails + 'afc.png', '')
	add_link('', '[COLOR lime]Australia Plus[/COLOR]', 0, 'udp://@225.1.2.21:30120 ', thumbnails + 'AustraliaNetwork.png', '')
	add_link('', '[COLOR lime]HBO HD[/COLOR]', 0, 'udp://@225.1.2.233:30120', thumbnails + 'hbohd.png', '')
	add_link('', '[COLOR lime]StarMovies SD[/COLOR]', 0, 'udp://@225.1.1.205:30120', thumbnails + 'starmovies.png', '')
	add_link('', '[COLOR lime]StarMovies HD[/COLOR]', 0, 'udp://@225.1.2.239:30120', thumbnails + 'starmovieshd.png', '')
	add_link('', '[COLOR lime]AXN HD[/COLOR]', 0, 'udp://@225.1.2.225:30120', thumbnails + 'axnhd.png', '')
	add_link('', '[COLOR lime]CARTOON NETWORK HD[/COLOR]', 0, 'udp://@225.1.2.231:30120', thumbnails + 'cartoon_networkhd.png', '')
	add_link('', '[COLOR lime]Star World HD[/COLOR]', 0, 'udp://@225.1.2.237:30120', thumbnails + 'starworldhd.png', '')
	add_link('', '[COLOR lime]Channel [V] HD[/COLOR]', 0, 'udp://@225.1.1.188:30120', thumbnails + '[V]hd.png', '')
	add_link('', '[COLOR lime]FashionTV HD[/COLOR]', 0, 'udp://@225.1.2.227:30120', thumbnails + 'ftvhd.png', '')
	add_link('', '[COLOR lime]BONG DA ANH 1[/COLOR]', 0, 'udp://@225.1.1.97:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 2[/COLOR]', 0, 'udp://@225.1.1.68:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 3[/COLOR]', 0, 'udp://@225.1.1.69:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 4[/COLOR]', 0, 'udp://@225.1.1.70:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 5[/COLOR]', 0, 'udp://@225.1.1.71:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 6[/COLOR]', 0, 'udp://@225.1.1.28:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 7[/COLOR]', 0, 'udp://@225.1.1.33:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 8[/COLOR]', 0, 'udp://@225.1.1.32:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 9[/COLOR]', 0, 'udp://@225.1.2.205:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]BONG DA ANH 10[/COLOR]', 0, 'udp://@225.1.1.10:30120', thumbnails + 'PREMIER LEAGUE.jpg', '')
	add_link('', '[COLOR lime]SKY SPORTS 1[/COLOR]', 0, 'http://02e4.vp9.tv/chn/sks1/v.m3u8', thumbnails + 'SkySports1.jpg', '')
	add_link('', '[COLOR lime]SKY SPORTS 4[/COLOR]', 0, 'http://03e4.vp9.tv/chn/sks4/v.m3u8', thumbnails + 'Skysport4.jpg', '')
	add_link('', '[COLOR lime]SKY SPORTS F1[/COLOR]', 0, 'http://02e4.vp9.tv/chn/sks1f1/v.m3u8', thumbnails + 'SKY SPORT f1.jpg', '')
	add_link('', '[COLOR lime]BEIN SPORTS 1[/COLOR]', 0, 'http://03e4.vp9.tv/chn/bein01hd/v.m3u8', thumbnails + 'BEIN SPORT 1.png', '')
	add_link('', '[COLOR lime]BEIN SPORTS 2[/COLOR]', 0, 'http://03e4.vp9.tv/chn/bein02hd/v.m3u8', thumbnails + 'BEIN SPORT 2.jpg', '')
	add_link('', '[COLOR lime]BT SPORT 1HD[/COLOR]', 0, 'http://02e4.vp9.tv/chn/btsu1/v.m3u8', thumbnails + 'BT SPORT 1HD.jpg', '')
	add_link('', '[COLOR lime]BT SPORT 2HD[/COLOR]', 0, 'http://02e4.vp9.tv/chn/btsu2/v.m3u8', thumbnails + 'BT SPORT 2HD.jpg', '')
	add_link('', '[COLOR lime]ARENA SPORT 1[/COLOR]', 0, 'http://03e4.vp9.tv/chn/arena/v.m3u8', thumbnails + 'ARENA SPORT 1.jpg', '')
	add_link('', '[COLOR lime]LIFETV[/COLOR]', 0, 'http://203.162.121.230:1935/live/live_lifetv/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'lifitv.png', '')
	add_link('', '[COLOR lime]KENH 9 MUSIC[/COLOR]', 0, 'http://203.162.121.230:1935/live/9_music/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'kenh9.png', '')
	add_link('', '[COLOR lime]FITNESS 360[/COLOR]', 0, 'http://203.162.121.230:1935/live/fitness_360/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + '360.png', '')
	add_link('', '[COLOR lime]MODEL CHANNEL[/COLOR]', 0, 'http://203.162.121.230:1935/live/model_channel/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'modechanel.png', '')
	add_link('', '[COLOR lime]Di san Viet[/COLOR]', 0, 'http://203.162.121.230:1935/live/disanviet/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'disanviet.png', '')
	add_link('', '[COLOR lime]4 MEN[/COLOR]', 0, 'http://203.162.121.230:1935/live//4Men/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + '4men.png', '')
	add_link('', '[COLOR lime]Channel Vietnam[/COLOR]', 0, 'http://203.162.121.230:1935/live//2channel/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'Chanel.png', '')
	add_link('', '[COLOR lime]SOTV[/COLOR]', 0, 'http://203.162.121.230:1935/live//sotv/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'sotv.png', '')
	add_link('', '[COLOR lime]TECH CHANNEL[/COLOR]', 0, 'http://203.162.121.230:1935/live//tech/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'tech.png', '')
	add_link('', '[COLOR lime]Kenh 911[/COLOR]', 0, 'http://203.162.121.230:1935/live//911/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + '911.png', '')
	add_link('', '[COLOR lime]Truyen Thong Viet[/COLOR]', 0, 'http://203.162.121.230:1935/live//ttv/index.m3u8?securetoken=#ed%h0#w@1', thumbnails + 'tuyenthonviet.png', '')
	add_link('', '[COLOR lime]Nguoi Lao Dong[/COLOR]', 0, 'http://222.255.27.218:8081/nld.m3u8', thumbnails + 'nguoilaodong.png', '')
	add_link('', '[COLOR lime]NCT HD[/COLOR]', 0, 'rtmp://123.30.134.108/live/nctlive', thumbnails + 'NCT.png', '')

def searchMenu(url, query = '', type='f', page=0):
	add_dir('New Search', url, 2, icon, query, type, 0)
	add_dir('Clear Search', url, 3, icon, query, type, 0)

	searchList=cache.get('searchList').split("\n")
	for item in searchList:
		add_dir(item, url, 2, icon, item, type, 0)
		
def resolve_url(url):
	make_request("http://feed.hdrepo.com/hitcount.php?url=" + url);
	if 'GetChannelStream' in url or 'GetMovieStream' in url:
		content = make_request(url)
		url = content.replace("\"", "")
		url = url[:-5]
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return


def add_link(date, name, duration, href, thumb, desc):
	description = date+'\n\n'+desc
	u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode=4"
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
	if 'zui' in href:
		liz.setProperty('IsPlayable', 'false')
	else:
		liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)



def add_dir(name,url,mode,iconimage,query='',type='f',page=0):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)#+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None
query=None
type='f'
page=0

try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
try:
	page=int(urllib.unquote_plus(params["page"]))
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "type: "+str(type)
print "page: "+str(page)
print "query: "+str(query)

if mode==None:
	get_categories()

elif mode==1:
	searchMenu(url, '', type, page)

elif mode==2:
	search(url, query, type, page)

elif mode==3:
	clearSearch()
elif mode==4:
	resolve_url(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	