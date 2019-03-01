# -*- coding: utf-8 -*-
""" author Caiqm. """

import requests, json, time, platform

class TemplateCls(object):
    # access_token缓存文件
    accessTokenFilePath = '/www/template/access_token.txt'
    # 公众号appid
    appid = 'xxx'
    # 公众号密钥
    secret = 'xxx'
    # 获取access_token链接
    accessTokenUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'
    # 发送模板消息链接
    sendTemplateUrl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'
    # 存储access_token信息字段
    accessTokenMessage = ''
    # 模板ID
    templateId = 'xxx'
    # 发送用户
    openid = 'xxx'
    # 构造函数
    def __init__(self):
        sysstr = platform.system()
        if sysstr == "Windows":
            self.accessTokenFilePath = 'E:\\python\\catch\\access_token.txt'
        elif sysstr == "Linux":
            self.accessTokenFilePath = '/www/template/access_token.txt'

    # 获取access_token函数
    def requestWxToken(self, callback, openid, tplMsg, templateId=None):
        # 拼接请求链接
        reqUrl = self.accessTokenUrl % (self.appid, self.secret)
        # 请求链接
        reqRst = requests.get(reqUrl)
        # 数据格式转json
        resJson = reqRst.json()
        # 获取当前时间戳
        timestamp = int(time.time())
        # 添加到期时间戳
        resJson['timestamp'] = timestamp + int(resJson['expires_in'])
        # 写入文件
        with open(self.accessTokenFilePath, 'w') as f:
            json.dump(resJson, f)
        print('ok')
        # 回调函数
        if callback:
            self.main(openid, tplMsg, templateId=None)

    # 发送模板消息
    def sendTemplate(self, openid, accessToken, tplMsg, templateId):
        # 定义时间显示格式
        fmt = '%Y-%m-%d %a %H:%M:%S'
        # 格式化日期
        date = time.strftime(fmt, time.localtime(time.time()))
        postData = {
            'touser': openid,
            'template_id': templateId,
            'url': tplMsg['url'],
            'data': {
                'first': {
                    'value': tplMsg['first'],
                    'color': '#173177'
                },
                'keyword1':{
                    'value': date,
                    'color': '#173177'
                },
                'keyword2': {
                    'value': tplMsg['keyword'],
                    'color': '#173177'
                },
                'remark':{
                    'value': tplMsg['remark'],
                    'color': '#DC143C'
                }
            }
        }
        # 拼接请求链接
        reqUrl = self.sendTemplateUrl % (accessToken)
        reqRst = requests.post(reqUrl, json = postData)
        rstJson = reqRst.json()
        print(rstJson)
        exit()

    # 主方法
    def main(self, openid, tplMsg, templateId=None):
        # 读取文件
        with open(self.accessTokenFilePath, 'r') as f:
            self.accessTokenMessage = f.read()
        # 判断是否存在access_token信息
        if not self.accessTokenMessage:
            self.requestWxToken(True, openid, tplMsg, templateId=None)
        else:
            # 获取缓存access_token信息
            accessTokenMessage = json.loads(self.accessTokenMessage)
            # access_token信息
            accessToken = accessTokenMessage['access_token']
            # 过期时间
            timestamp = accessTokenMessage['timestamp']
            if not timestamp:
                self.requestWxToken(True, openid, tplMsg, templateId=None)
            # 时间戳转格式
            timestamp = int(timestamp)
            # 获取当前时间戳
            nowStamp = int(time.time())
            # 判断是否过期
            if nowStamp >= timestamp:
                self.requestWxToken(True, openid, tplMsg, templateId=None)
            else:
                # 判断是否存在模板ID
                if templateId is None:
                    templateId = self.templateId
                self.sendTemplate(openid, accessToken, tplMsg, templateId)

# 例子
tpl = TemplateCls()
# 发送人的openid
sendUser = 'xxx'
tplPost = {
    'url': '',
    'first': '抓取数据成功！',
    'keyword': '抓取数据6条',
    'remark': '下次抓取时间30分钟后'
}
tpl.main(sendUser, tplPost)