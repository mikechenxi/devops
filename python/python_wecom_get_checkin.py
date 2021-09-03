#/usr/bin/python3
import json, time, requests
from datetime import datetime, timedelta


def main():
    sys_date = datetime.now()
    start_time = (sys_date + timedelta(minutes = -60)).strftime('%Y-%m-%d %H:%M:%S')
    end_time = sys_date.strftime('%Y-%m-%d %H:%M:%S')
    user_list = get_wecom_user_list()
    checkin_data = get_wecom_checkin_data(start_time, end_time, user_list)
    print(checkin_data)


# start_time / end_time format: '2020-01-01' / '2020-01-01 01:01:01'
def get_wecom_checkin_data(start_time, end_time, user_list):
    ret = []
    token = get_wecom_token('checkin')
    start_time = time.mktime(time.strptime(start_time + ' 00:00:00' if len(start_time) == 10 else start_time, "%Y-%m-%d %H:%M:%S"))
    end_time = time.mktime(time.strptime(end_time + ' 00:00:00' if len(end_time) == 10 else end_time, "%Y-%m-%d %H:%M:%S"))
    url = 'https://qyapi.weixin.qq.com/cgi-bin/checkin/getcheckindata?access_token=%s' % (token)
    req_data = {
        'opencheckindatatype': 1, # 上下班打卡
        'starttime': start_time,
        'endtime': end_time
    }
    user_ids = sorted(user_list.keys())
    for count in range(len(user_ids) // 100 + 1):
        req_data['useridlist'] = user_ids[100 * count: 100 * (count + 1)]
        res = json.loads(requests.post(url, json.dumps(req_data)).text)
        if res['errcode'] == 0:
            checkin_data = res['checkindata']
            if checkin_data is not None and len(checkin_data) > 0:
                for data in checkin_data:
                    if data['location_detail'] == '' or data['groupname'] == '':
                        continue
                    data['name'] = user_list[data['id']]
                    data['checkin_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['checkin_time']))
                    ret.append(data)
    return ret


def get_wecom_user_list():
    ret = {}
    token = get_wecom_token('org')
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=%s&department_id=%s&fetch_child=1' % (token, department_id)
    res = requests.get(url).text
    user_list = json.loads(res)['userlist']
    if user_list is not None and len(user_list) > 0:
        for user in user_list:
            ret[user['userid']] = user['name']
    return ret


def get_wecom_token(source):
    corpid = 'xxxx'
    if source == 'checkin':
        corpsecret = 'xxxx'
    elif source == 'org':
        corpsecret = 'xxxx'
    else:
        corpsecret = ''
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    res = requests.get(url).text
    return json.loads(res)['access_token']


if __name__ == '__main__':
    main()
