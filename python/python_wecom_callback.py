#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import random, sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route('/wecom_callback', methods=['GET', 'POST'])
def call_back():
    token = 'xxxx'  # Features -> Receive messages -> Set to receive message via API
    encoding_aes_key = 'xxxx'  # Features -> Receive messages -> Set to receive message via API
    corpid = 'xxxx'
    wxcpt = WXBizMsgCrypt(token, encoding_aes_key, corpid)

    if request.method == 'GET':
        # 验证回调URL
        verify_signature = request.args.get('msg_signature')
        verify_timestamp = request.args.get('timestamp')
        verify_nonce = request.args.get('nonce')
        verify_echostr = request.args.get('echostr')
        ret, echostr = wxcpt.VerifyURL(verify_signature, verify_timestamp, verify_nonce, verify_echostr)
        if(ret != 0):
            # sys.exit(1)
            return ''
        else:
            return echostr
    elif request.method == 'POST':
        # 对用户回复的消息进行解密
        req_data = request.get_data()
        req_msg_signature = request.args.get('msg_signature')
        req_timestamp = request.args.get('timestamp')
        req_nonce = request.args.get('nonce')
        ret, msg = wxcpt.DecryptMsg(req_data, req_msg_signature, req_timestamp, req_nonce)
        if(ret != 0):
            # sys.exit(1)
            return ''

        # 对企业回复用户消息进行加密
        xml_tree = ET.fromstring(msg)
        req_from_user_name = xml_tree.find('FromUserName').text
        req_to_user_name = xml_tree.find('ToUserName').text
        req_agent_id = xml_tree.find('AgentID').text
        resp_msg_id = str(random.getrandbits(64))
        resp_content = 'xxxx'
        resp_data = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>%s</MsgId><AgentID>%s</AgentID></xml>' % (req_to_user_name, req_from_user_name, req_timestamp, resp_content, resp_msg_id, req_agent_id)
        resp_data = str(resp_data)
        ret, encrypt_msg = wxcpt.EncryptMsg(resp_data, req_nonce, req_timestamp)
        if(ret != 0):
            #sys.exit(1)
            return '' 
        else:
            return encrypt_msg
    else:
        return '' 
