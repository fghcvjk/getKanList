# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import re
import chardet

getKanStr = u'まるゆ, Z3, Z3 zwei, 伊168, 伊58, 伊8, U-511, 吕500, 三隈, 三隈改, 五十铃, 五十铃改二, 云龙, 云龙改, 羽黑, 羽黑改二, 大井, 大井改, 大井改二, 如月, 如月改二, 妙高, 妙高改二, 龙骧, 龙骧改二, 鸟海, 鸟海改二, 长门, 长门改二, 阿武隈, 阿武隈改二, 金刚, 金刚改二, 吹雪, 吹雪改二, 北上, 北上改, 北上改二, 时雨, 时雨改二, 木曾, 木曾改二, 比睿, 比睿改二, 初霜, 初霜改二, 加古, 加古改二, 睦月, 睦月改二, 衣笠, 衣笠改二, 飞龙, 飞龙改二, 隼鹰, 隼鹰改二, 榛名, 榛名改二, 摩耶, 摩耶改二, 古鹰, 古鹰改二, 那智, 那智改二, 那珂, 那珂改二, 皋月, 皋月改二, 大鲸, 春雨, 晓, 晓改二, 最上, 最上改, 熊野, 浦风, 俾斯麦, 电, 高雄, 鬼怒, 鹿岛, Верный, 俾斯麦改, 龙凤, 龙凤改, 龙田, 雷, 雾岛, 雾岛改二, 铃谷, 铃谷改, 谷风, 赤城, 翔鹤, 速吸, 阿贺野, 陆奥, 雪风, 足柄, 足柄改二, 翔鶴, 瑞鳳, 瑞鳳改, 瑞鶴, 天津风, 夕张, 夕立, 夕立改二, 多摩, 熊野改, 时津风, 明石, 明石改, 日向, 日向改, 天龙, 加贺, 千代田, 千代田改, 千代田甲, 千代田航, 千代田航改二, 加賀, 千歲, 千歲改, 千歲甲, 千歲航, 千歲航改二, 武藏, 武藏改, 大和, 大和改, 大淀, 千岁, 千岁改, 千岁甲, 千岁航, 千岁航改二, 绫波, 绫波改二, 香取, 舞风, 苍龙, 苍龙改二, 伊势, 伊势改, 瑞凤, 瑞凤改, 瑞鹤, 瑞鹤改, 伊19, 初春, 初春改二, Z1, 飞鹰, 扶桑, 扶桑改二, 山城, 野分, 能代, 秋津洲, 秋津洲改, 筑摩, 神通, 神通改二, 滨风, 岛风, 川内, 川内改二, 葛城, 球磨, 利根, 利根改二, 响, 爱宕, 罗马, 利托里奥, 丛云, 丛云改二' #已经开图鉴了的船不显示，中文日文混杂的全部丢进去
getKanList = getKanStr.split(', ')
#日文wiki有谷歌验证所以不使用了
# url = 'https://zh.kcwiki.org/wiki/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4' #舰娘百科
url = 'https://zh.moegirl.org/%E8%88%B0%E9%98%9FCollection/%E5%9B%BE%E9%89%B4/%E8%88%B0%E5%A8%98#' #萌娘百科
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
# pattern = re.compile(r'(?<=<img alt=").+?(?=" src=")') #解析舰娘百科用正则表达式
pattern = re.compile(r'(?<=" title=").+?">No\.[0-9]{3} (.+?)(?=</a>)') #解析萌娘百科用正则表达式
subPattern = re.compile(r'(?<=">).+?(?=</span>)') #萌娘百科的部分数据需要二次解析

#获取网页数据
try:
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    urlData = response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

#抓出需要的数据
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

