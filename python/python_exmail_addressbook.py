#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, string, random, requests, sys
reload(sys)
sys.setdefaultencoding('utf-8')


# https://exmail.qq.com/qy_mng_logic/doc#10001
def get_token():
    corpid = 'xxxx'
    corpsecret = 'xxxx'
    url = 'https://api.exmail.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    res = requests.get(url).text
    return json.loads(res)['access_token']


def create_user(user_id, user_name, department_list, position = '', mobile = '', ext_id = ''):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/create?access_token=%s' % (token)
    password = ''.join(random.sample(string.ascii_letters + string.digits, 12))
    data = {
        'userid': user_id,
        'name': user_name,
        'department': department_list,
        'position': position,
        'mobile': mobile,
        'extid': ext_id,
        'password':  password
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return password
    else:
        print(res)
        return None


def get_user(user_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/get?access_token=%s&userid=%s' % (token, user_id)
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
    #token = get_token()
    #url = 'https://api.exmail.qq.com/cgi-bin/user/fuzzysearch'?access_token=%s&userid=%s' % (token, keyword)
    #res = requests.get(url).text
    #user_list = json.loads(res)['users']
    #return fill_user_list_path(user_list)


def get_user_state(user):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/batchcheck?access_token=%s' % (token)
    data = {
        'userlist': [user]
    }
    res = requests.post(url, json.dumps(data)).text
    return json.loads(res)['list'][0]['type']  # 帐号类型。-1:帐号号无效; 0:帐号名未被占用; 1:主帐号; 2:别名帐号; 3:邮件群组帐号


def get_user_list_state(user_list):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/batchcheck?access_token=%s' % (token)
    data = {
        'userlist': user_list
    }
    res = requests.post(url, json.dumps(data)).text
    return json.loads(res)['list']


def update_user(user_id, user_name = None, department_list = None, password = None, position = None, mobile = None, ext_id = None, enable = 1):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/update?access_token=%s' % (token)
    data = {
        'userid': user_id,
        'enable': enable
    }
    if user_name is not None:
        data['name'] = user_name
    if department_list is not None:
        data['department'] = department_list
    if password is not None:
        data['password'] = password
    if position is not None:
        data['position'] = position
    if mobile is not None:
        data['mobile'] = mobile
    if ext_id is not None:
        data['extid'] = ext_id
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False

  
def reset_user_password(user_id):
    password = ''.join(random.sample(string.ascii_letters + string.digits, 12))
    result = update_user(user_id, None, None, password, None, None, None, 1)
    result['password'] = password
    return result

    
def disable_user(user_id):
    result = update_user(user_id, None, None, None, None, None, None, 0)
    return result


def delete_user(user_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/user/delete?access_token=%s&userid=%s' % (token, user_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def create_group(group_id, user_list):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/group/create?access_token=%s' % (token)
    data = {
        'groupid': group_id,
        'groupname': group_id,
        'userlist': user_list,
        'allow_type': 1  # 群发权限。0: 企业成员, 1任何人， 2:组内成员，3:自定义成员。
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def get_group_list_by_keyword(keyword):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/group/fuzzysearch'
    if keyword == '':
        url = '%s?access_token=%s' % (url, token)
    else:
        url = '%s?access_token=%s&fuzzy=1&groupid=%s' % (url, token, keyword)
    res = requests.get(url).text
    return json.loads(res)['groups']


# group contains user_list, department_list, tag_list, group_list
def get_group_user_list(group_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/group/get?access_token=%s&groupid=%s' % (token, group_id)
    res = requests.get(url).text
    res = json.loads(res)
    user_list = res['userlist']
    department_list = res['department']
    tag_list = res['taglist']
    group_list = result['grouplist']
    if department_list is not None and len(department_list) > 0:
        for department in department_list:
            department_user_list = get_department_user_list(department)
            if department_user_list is not None and len(department_user_list) > 0:
                for department_user in department_user_list:
                    if department_user['userid'] not in user_list:
                        user_list.append(department_user['userid'])
    if tag_list is not None and len(tag_list) > 0:
        for tag in tag_list:
            tag_user_list = get_tag_user_list(tag)
            if tag_user_list is not None and len(tag_user_list) > 0:
                for tag_user in tag_user_list:
                    if tag_user['userid'] not in user_list:
                        user_list.append(tag_user['userid'])
    if group_list is not None and len(group_list) > 0:
        for group in group_list:
            group_user_list = get_group_user_list(group)
            if group_user_list is not None and len(group_user_list) > 0:
                for group_user in group_user_list:
                    if group_user not in user_list:
                        user_list.append(group_user)
    return user_list


def update_group(group_id, user_list = None, department_list = None, tag_list = None, group_list = None):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/group/update?access_token=%s' % (token)
    data = {
        'groupid': group_id
    }
    if user_list is not None:
        data['userlist'] = user_list
    if department_list is not None:
        data['department'] = department_list
    if tag_list is not None:
        data['taglist'] = tag_list
    if group_list is not None:
        data['grouplist'] = group_list
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def delete_group(group_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/group/delete?access_token=%s&groupid=%s' % (token, group_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False


def create_department(department_name, parent_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/department/create?access_token=%s' % (token)
    data = {
        'name': department_name,
        'parentid': parent_id
    }
    res = requests.post(url, json.dumps(data)).text
    if json.loads(res)['errcode'] == 0:
        return res['id']
    else:
        print(res)
        return None


def get_department_list(department_id, return_path = True):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/department/list?access_token=%s&id=%s' % (token, department_id)
    res = requests.get(url).text
    department_list = json.loads(res)['department']
    if return_path is True:
        department_list = fill_department_list_path(department_list)
    return department_list


def get_department_list_by_keyword(keyword, fuzzy_search = False):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/department/search?access_token=%s' % (token)
    data = {
        'name': keyword,
        'fuzzy': 1 if fuzzy_search is True else 0
    }
    res = requests.post(url, json.dumps(data)).text
    department_list = json.loads(res)['department']
    if department_list is not None and len(department_list) > 0:
        for department in department_list:
            # remove the first dept in path
            department['path'] = '/'.join(str(department['path']).split('/')[1:])
    return department_list


def get_department_user_list(department_id, fetch_child = True, simple_list = True, return_path = True)):
    token = get_token()
    if simple_list == True:
        url = 'https://api.exmail.qq.com/cgi-bin/user/simplelist'
    else:
        url = 'https://api.exmail.qq.com/cgi-bin/user/list'
    fetch_child = 1 if fetch_child == True else 0
    url = '%s?access_token=%s&department_id=%s&fetch_child=%s' % (url, token, department_id, fetch_child)
    res = requests.get(url).text
    user_list = json.loads(res)['userlist']
    if return_path is True:
        user_list = fill_user_list_path(user_list)
    return user_list


def fill_user_list_path(user_list):
    if len(user_list) > 2:
        dic = {}
        all_department_list = get_department_list(0, False)
        for department in all_department_list:
            dic[department['id']] = department
        for user in user_list:
            path = []
            for department_id in user['department']:
                department_path = dic[department_id]['name']
                parent_id = dic[department_id]['parentid']
                while parent_id != 0:
                    if dic[parent_id]['parentid'] != 0:
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
                while parent_id != 0:
                    parent_departments = get_department_list(parent_id, False)
                    if parent_departments is not None and len(parent_departments) > 0:
                        for parent_department in parent_departments:
                            # parent_departments contains sub department
                            if parent_department['id'] == parent_id:
                                if parent_department['parentid'] != 0:
                                    department_path = parent_department['name'] + '/' + department_path if department_path != '' else parent_department['name']
                                parent_id = parent_department['parentid']
                                break
                path.append(department_path)
            user['path'] = path
    return user_list


def fill_department_list_path(department_list):
    if len(department_list) > 2:
        dic = {}
        all_department_list = get_department_list(0, False)
        for department in all_department_list:
            dic[department['id']] = department
        for department in department_list:
            department_path = department['name']
            parent_id = department['parentid']
            while parent_id != 0:
                if dic[parent_id]['parentid'] != 0:
                    department_path = dic[parent_id]['name'] + '/' + department_path
                parent_id = dic[parent_id]['parentid']
            department['path'] = department_path
    else:
        for department in department_list:
            department_path = department['name']
            parent_id = department['parentid']
            while parent_id != 0:
                parent_departments = get_department_list(parent_id, False)
                if parent_departments is not None and len(parent_departments) > 0:
                    for parent_department in parent_departments:
                        # parent_departments contains sub department
                        if parent_department['id'] == parent_id:
                            if parent_department['parentid'] != 0:
                                department_path = parent_department['name'] + '/' + department_path if department_path != '' else parent_department['name']
                            parent_id = parent_department['parentid']
                            break
            department['path'] = department_path
    return department_list


def update_department(department_id, department_name, parent_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/department/update?access_token=%s' % (token)
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
    url = 'https://api.exmail.qq.com/cgi-bin/department/delete?access_token=%s&id=%s' % (token, department_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False

    
def create_tag(tag_name, tag_id = None):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/tag/create?access_token=%s' % (token)
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
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/tag/list?access_token=%s' % (token)
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


# tag contains user_list, department_list
def get_tag_user_list(tag_id):
    token = get_token()
    url = 'https://api.exmail.qq.com/cgi-bin/tag/get?access_token=%s&tagid=%s' % (token, tag_id)
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
    url = 'https://api.exmail.qq.com/cgi-bin/tag/addtagusers?access_token=%s' % (token)
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
    url = 'https://api.exmail.qq.com/cgi-bin/tag/deltagusers?access_token=%s' % (token)
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
    url = 'https://api.exmail.qq.com/cgi-bin/tag/update?access_token=%s' % (token)
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
    url = 'https://api.exmail.qq.com/cgi-bin/tag/delete?access_token=%s&tagid=%s' % (token, tag_id)
    res = requests.get(url).text
    if json.loads(res)['errcode'] == 0:
        return True
    else:
        print(res)
        return False
