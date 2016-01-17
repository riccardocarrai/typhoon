__author__ = 'riccardocarrai'


import urllib2, base64
request = urllib2.Request('http://www.doctorvisual.com/Plugins/EasyOneExport/Export/Orders')
base64string = base64.encodestring('%s:%s' % ('support@doctorvisual.com', 'S9pp!rt0')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)
fp=open('prova.xml','w')
fp.write(data)
fp.close()