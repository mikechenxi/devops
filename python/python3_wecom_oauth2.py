# https://work.weixin.qq.com/api/doc/90000/90135/91335

# home page: https://open.weixin.qq.com/connect/oauth2/authorize?appid=xxxx&redirect_uri=https://xx.xxxx.com/oauth&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect
# https://xx.xxxx.com/oauth

from flask import Flask, request
import requests, json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/oauth')
def oauth_test():
    code = request.args.get('code')
    token = json.loads(requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=xxxx&corpsecret=xxxx'))['access_token']
    user_id = json.loads(requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s' % (token, code)))['UserId']
    return user_id
