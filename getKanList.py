# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import re
import chardet

getKanStr = '[]' #已经开图鉴了的船不显示
getKanList = eval(getKanStr)
#日文wiki有谷歌验证所以不使用了
# url = 'https://zh.kcwiki.org/wiki/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4' #舰娘百科
url2 = 'https://zh.moegirl.org/%E8%88%B0%E9%98%9FCollection/%E5%9B%BE%E9%89%B4/%E8%88%B0%E5%A8%98#' #萌娘百科

#获取网页数据
try:
    request = urllib2.Request(url2)
    response = urllib2.urlopen(request)
    urlData = response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

#抓出需要的数据
# pattern = re.compile(r'(?<=<img alt=").+?(?=" src=")') #解析舰娘百科用正则表达式
pattern = re.compile(r'(?<=" title=").+?">No\.[0-9]{3} (.+?)(?=</a>)') #解析萌娘百科用正则表达式
subPattern = re.compile(r'(?<=">).+?(?=</span>)') #萌娘百科的部分数据需要二次解析
kanNameDataList = pattern.findall(urlData)
errorkanNames = {}
kanNameList = []
for index, kanName in enumerate(kanNameDataList):
    try:
        if '</span>' in kanName: #萌娘百科二次解析
            kanName = subPattern.search(kanName).group()
        kanName = kanName.decode('utf-8')
        kanName.encode('gbk') #检验是否能在gbk环境下打印
        if '.jpg' not in kanName and kanName != '未实装':
            if kanName not in kanNameList and kanName not in getKanList:
                kanNameList.append(kanName)
    except:
        errorkanNames[index] = kanName

print 'error data:', errorkanNames
#获取有问题的手动处理一下，目前发现舰娘百科的日中文混杂会有这个问题
# for addName in ['岚', '萩风']:
    # if addName not in kanNameList:
        # kanNameList.append(addName)
# for rmName in ['丸輸', '飛鷹', '青葉']:
    # if rmName in kanNameList:
        # kanNameList.remove(rmName)
kanNameList.sort()

print 'kan num:', len(kanNameList)
kanNamesStr = ', '.join(kanNameList)
print 'kan List:'
print kanNamesStr

