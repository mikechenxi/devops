#!/usr/bin/python
# -*- coding: utf-8 -*-


import json, hashlib, random, string, datetime, xmltodict, requests, xml.etree.cElementTree as ET, sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    send_red_package('xxxx')


# https://work.weixin.qq.com/api/doc/90000/90135/90275
def send_red_package(userid):
    wxappid = 'xxxx'  # 企业id即corpid
    mch_id = 'xxxx'  # 商户号
    agentid = 'xxxx'  # 用于发红包的应用id
    url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendworkwxredpack'
    data = {
        'act_name': '恭喜发财,大吉大利',  # 项目名称
        'mch_billno': datetime.datetime.now().strftime('%Y%m%d') + userid,  # 商户订单号
        'mch_id': mch_id,
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 31)),  # 随机字符串
        're_openid': userid_to_openid(userid),  # 用户openid
        'total_amount': '100',  # 金额，单位分，单笔最小金额默认为1元
        'wxappid': wxappid
    }
    data['workwx_sign'] = get_workwx_sign(data)  # 企业微信签名
    # agentid 和 sender_name + sender_header_media_id 互斥
    data['agentid'] = agentid
    #data['sender_name'] = '开工利是'  # 发送者名称
    #data['sender_header_media_id'] = 'xxxx'  # 发送者头像素材id，通过企业微信开放上传素材接口获取
    data['wishing'] = '恭喜发财,大吉大利'  # 红包祝福语
    data['remark'] = '开工利是'  # 备注
    data['sign'] = get_sign(data)  # 微信支付签名
    data = {'xml': data}
    data = xmltodict.unparse(data).encode('utf-8')
    res = requests.post(url, data = data, headers = {'Content-Type': 'text/xml'}, cert = ('apiclient_cert.pem', 'apiclient_key.pem')).text
    print(res)
    xml_tree = ET.fromstring(res)
    # xml_tree.find("result_code").text  微信单号
    return_code = str(xml_tree.find("return_code").text)
    if return_code == 'SUCCESS':
        result_code = str(xml_tree.find("result_code").text)
        if result_code == 'SUCCESS':
            return True
    return False


# https://work.weixin.qq.com/api/doc/90000/90135/90276
def query_red_package(mch_billno):
    mch_id = 'xxxx'  # 商户号
    app_id = 'xxxx'  # 企业id即corpid
    url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/queryworkwxredpack'
    data = {
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 31)),
        'mch_billno': mch_billno,
        'mch_id': mch_id,
        'appid': app_id
    }
    data['sign'] = get_sign(data)
    data = {'xml': data}
    data = xmltodict.unparse(data).encode('utf-8')
    res = requests.post(url, data = data, headers = {'Content-Type': 'text/xml'}, cert = ('apiclient_cert.pem', 'apiclient_key.pem')).text
    print(res)
    xml_tree = ET.fromstring(res)
    return_code = str(xml_tree.find("return_code").text)
    if return_code == 'SUCCESS':
        result_code = str(xml_tree.find("result_code").text)
        if result_code == 'SUCCESS':
            # SENDING:发放 SENT:已发放待领取 FAILED：发放失败 RECEIVED:已领取 RFUND_ING:退款中 REFUND:已退款
            return str(xml_tree.find("status").text)
    return ''


def userid_to_openid(userid):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/convert_to_openid?access_token=' + token
    data = {
        'userid': userid
    }
    res = requests.post(url, json.dumps(data)).text
    return json.loads(res)['openid']


def get_token():
    corpid = 'xxxx'  # 企业id
    corpsecret = 'xxxx'  # 企业支付应用secret
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    res = requests.get(url).text
    return json.loads(res)['access_token']


def get_workwx_sign(data):
    str = ''
    sign_secret = 'xxxx'  # 企业支付应用secret
    for key in sorted(data.keys()):
        str += (key + '=' + data[key] + '&')
    str = str + 'secret=' + sign_secret
    hash_md5 = hashlib.md5(str.encode('utf8'))
    workwx_sign = hash_md5.hexdigest().upper()
    return workwx_sign


def get_sign(data):
    str = ''
    sign_key = 'xxxx'  # 商户平台API密钥里面设置的key
    for key in sorted(data.keys()):
        str += (key + '=' + data[key] + '&')
    str = str + 'key=' + sign_key
    hash_md5 = hashlib.md5(str.encode('utf8'))
    sign = hash_md5.hexdigest().upper()
    return sign


if __name__ == '__main__':
    main()
