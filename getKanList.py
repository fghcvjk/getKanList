# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import re
import chardet

getKanStr = '[]'
getKanList = eval(getKanStr)
url = 'https://zh.kcwiki.org/wiki/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4'

try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    urlData = response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

pattern = re.compile(r'(?<=<img alt=").+?(?=" src=")')
kanNameDataList = pattern.findall(urlData)
errorkanNames = {}
kanNameList = []
for index, kanName in enumerate(kanNameDataList):
    try:
        kanName = kanName.decode('utf-8')
        kanName.encode('gbk') #检验是否能在gbk环境下打印
        if '.jpg' not in kanName and kanName != '未实装':
            if kanName not in kanNameList and kanName not in getKanList:
                kanNameList.append(kanName)
    except:
        errorkanNames[index] = kanName
print 'error data:', errorkanNames
 #获取有问题的手动处理一下
kanNameList.extend([])
for rmName in []:
    kanNameList.remove(rmName)
kanNameList.sort()

print 'kan num:', len(kanNameList)
kanNamesStr = ', '.join(kanNameList)
print 'kan List:'
print kanNamesStr

