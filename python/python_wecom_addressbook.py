#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, requests, sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_token():
    corpid = 'xxxx' # 企业id
    corpsecret = 'xxxx' # 应用secret
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    res = requests.get(url).text
    return json.loads(res)['access_token']


def create_user(user_id, user_name, department_list, position, email, mobile):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=%s' % (token)
    data = {
        'userid': user_id,
        'name': user_name,
        'department': department_list,
        'position': position,
        'email': email,
        'mobile': mobile,
        'enable': 1
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def get_user(user_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s' % (token, user_id)
    res = requests.get(url).text
    user = json.loads(res)
    return fill_user_list_path([user])[0]


def get_user_list_by_keyword(keyword):
    user_list = []
    all_user_list = get_department_user_list('1')
    if all_user_list is not None and len(all_user_list) > 0:
        for user in all_user_list:
            if keyword in user['name'] or keyword in user['userid']:
                user_list.append(user)
    return user_list


def update_user(user_id, user_name = None, department_list = None, position = None, email = None, mobile = None, enable = 1):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token=%s' % (token)
    data = {
        'userid': user_id,
        'enable': enable
    }
    if user_name is not None:
        data['name'] = user_name
    if department_list is not None:
        data['department'] = department_list
    if position is not None:
        data['position'] = position
    if email is not None:
        data['email'] = email
    if mobile is not None:
        data['mobile'] = mobile
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def disable_user(user_id):
    ret = update_user(user_id, None, None, None, None, None, 0)
    return ret


def delete_user(user_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/delete?access_token=%s&userid=%s' % (token, user_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def batch_delete_user(user_id_list):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/batchdelete?access_token=%s' % (token)
    data = {
        'useridlist': user_id_list
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def create_department(department_name, parent_id, department_id = None):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=%s' % (token)
    data = {
        'name': department_name,
        'parentid': parent_id
    }
    if department_id is not None:
        data['id'] = department_id
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return res['id']
    else:
        print(res)
        return None


def get_department_list(department_id, return_path = True):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=%s&id=%s' % (token, department_id)
    res = requests.get(url).text
    department_list = json.loads(res)['department']
    if return_path is True:
        department_list = fill_department_list_path(department_list)
    return department_list


def get_department_list_by_keyword(keyword, fuzzy_search = False, return_path = True):
    department_list = []
    all_department_list = get_department_list(1, return_path)
    if all_department_list is not None and len(all_department_list) > 0:
        for department in all_department_list:
            if fuzzy_search is False and department['name'] == keyword:
                department_list.append(department)
            elif fuzzy_search is True and keyword in department['name']:
                department_list.append(department)
            else:
                pass
    return department_list


def get_department_user_list(department_id, fetch_child = True, simple_list = True):
    token = get_token()
    if simple_list is True:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'
    else:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/list'
    fetch_child = 1 if fetch_child == True else 0
    url = '%s?access_token=%s&department_id=%s&fetch_child=%s' % (url, token, department_id, fetch_child)
    res = interface_util.call_http(url, None, 'GET')
    user_list = json.loads(res)['userlist']
    return fill_user_list_path(user_list)


def fill_user_list_path(user_list):
        if len(user_list) > 2:
        dic = {}
        all_department_list = get_department_list(1, False)
        for department in all_department_list:
            dic[department['id']] = department
        for user in user_list:
            path = []
            for department_id in user['department']:
                department_path = dic[department_id]['name']
                parent_id = dic[department_id]['parentid']
                while parent_id not in (0, 1):
                    department_path = dic[parent_id]['name'] + '/' + department_path
                    parent_id = dic[parent_id]['parentid']
                path.append(department_path)
            user['path'] = path
    else:
        for user in user_list:
            path = []
            for department_id in user['department']:
                department_path = None
                parent_id = None
                departments = get_department_list(department_id)
                for department in departments:
                    if department['id'] == department_id:
                        department_path = department['name']
                        parent_id = department['parentid']
                while parent_id not in (0, 1):
                    parent_departments = get_department_list(parent_id, False)
                    if parent_departments is not None and len(parent_departments) > 0:
                        for parent_department in parent_departments:
                            # parent_departments contains sub department
                            if parent_department['id'] == parent_id:
                                department_path = parent_department['name'] + '/' + department_path
                                parent_id = parent_department['parentid']
                                break
                path.append(department_path)
            user['path'] = path
    return user_list


def fill_department_list_path(department_list):
        if len(department_list) > 2:
        dic = {}
        all_department_list = get_department_list(1, False)
        for department in all_department_list:
            dic[department['id']] = department
        for department in department_list:
            department_path = department['name']
            parent_id = department['parentid']
            while parent_id not in (0, 1):
                department_path = dic[parent_id]['name'] + '/' + department_path
                parent_id = dic[parent_id]['parentid']
            department['path'] = department_path
    else:
        for department in department_list:
            department_path = department['name']
            parent_id = department['parentid']
            while parent_id not in (0, 1):
                parent_departments = get_department_list(parent_id, False)
                if parent_departments is not None and len(parent_departments) > 0:
                    for parent_department in parent_departments:
                        # parent_departments contains sub department
                        if parent_department['id'] == parent_id:
                            department_path = parent_department['name'] + '/' + department_path
                            parent_id = parent_department['parentid']
                            break
            department['path'] = department_path
    return department_list


def update_department(department_id, department_name, parent_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/update?access_token=%s' % (token)
    data = {
        'id': department_id,
        'name': department_name,
        'parentid': parent_id
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def delete_department(department_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/delete?access_token=%s&id=%s' % (token, department_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def create_tag(tag_name, tag_id = None):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/create?access_token=%s' % (token)
    data = {
        'tagname': tag_name
    }
    if tag_id is not None:
        data['tagid'] = tag_id
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return res['tagid']
    else:
        print(res)
        return None


def get_tag_list():
    token = get_token('org')
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/list?access_token=%s' % (token)
    res = requests.get(url).text
    return json.loads(res)['taglist']

  
def get_tag_list_by_keyword(keyword, fuzzy_search = False):
    ret = []
    tag_list = get_tag_list()
    if tag_list is not None and len(tag_list) > 0:
        for tag in tag_list:
            if fuzzy_search == False:
                if tag['tagname'] == keyword:
                    ret.append(tag)
            else:
                if keyword in tag['tagname']:
                    ret.append(tag)
    return ret
  

def get_tag_user_list(tag_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/get?access_token=%s&tagid=%s' % (token, tag_id)
    res = requests.get(url).text
    res = json.loads(res)
    user_list = res['userlist']
    department_list = res['partylist']
    if department_list is not None and len(department_list) > 0:
        for department in department_list:
            department_user_list = get_department_user_list(department)
            if department_user_list is not None and len(department_user_list) > 0:
                for department_user in department_user_list:
                    if department_user['userid'] not in user_list:
                        user_list.append(department_user['userid'])
    return user_list


def add_tag_user_list(tag_id, user_list, department_list):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/addtagusers?access_token=%s' % (token)
    data = {
        'tagid': tag_id,
        'userlist': user_list,
        'partylist': department_list
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def delete_tag_user_list(tag_id, user_list, department_list):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/deltagusers?access_token=%s' % (token)
    data = {
        'tagid': tag_id,
        'userlist': user_list,
        'partylist': department_list
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def update_tag(tag_id, tag_name):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/update?access_token=%s' % (token)
    data = {
        'tagid': tag_id,
        'tagname': tag_name
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def delete_tag(tag_id):
    token = get_token()
    url = 'https://qyapi.weixin.qq.com/cgi-bin/tag/delete?access_token=%s&tagid=%s' % (token, tag_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False  
