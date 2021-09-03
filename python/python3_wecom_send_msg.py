#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json, requests


def send_message(tousers, content, msg_type = 'text'):
    if len(tousers) > 0 and len(content) > 0:
        token = get_token()
        agentid = xxxx # 应用agentid
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token)
        for count in range(get_wecom_len(content) // 2040 + 1):  # wecom单条消息长度限制2048 但是传带中文长度2048的字符串过去还是会被截取 可能wecom中还有其他特殊字符长度大于1
            sub_content = get_wecom_substr(content, 2040 * count, 2040)
            data = {
                'touser': tousers,
                'msgtype': msg_type,
                'agentid': agentid
            }
            if msg_type in ['image', 'voice', 'video', 'file']:
                data[msg_type] = {'media_id': upload_temp_material(token, sub_content, msg_type)}
            else:
                data[msg_type] = {'content': sub_content}
            res = requests.post(url, json.dumps(data)).text
            if json.loads(res)['errcode'] == 0:
                return True
            else:
                print(res)
                return False


def get_token():
    corpid = 'xxxx' # 企业id
    corpsecret = 'xxxx' # 应用secret
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    res = requests.get(url)
    return json.loads(res.text)['access_token']


def upload_temp_material(token, file_path, file_type = 'file'):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (token, file_type)
    with open(file_path, 'rb') as f:
        data = {
            'file': f
        }
        res = requests.post(url, files = data).text
        res = json.loads(res)
        if res['errcode'] == 0:
            return res['media_id']
        else:
            print(res)
            return None


def get_wecom_len(str):
    length = len(str)
    for s in str:
        if 0x4E00 <= ord(s) <= 0x9FA5:
            length += 2 # 企业微信一个汉字占三个字节, 而python3一个汉字占一个字节
    return length


# start从0开始
def get_wecom_substr(str, start, count):
    ret = ''
    index = 0
    for s in str:
        if index < start:
            if 0x4E00 <= ord(s) <= 0x9FA5:
                index += 3
            else:
                index += 1
            continue
        if count > 0:
            if 0x4E00 <= ord(s) <= 0x9FA5:
                count -= 3
            else:
                count -= 1
            ret += s
    if ret.startswith('\n'):
        ret = ret[1:]
    if ret.endswith('\n'):
        ret = ret[:-1]
    return ret
