#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap

def ldap_auth(username, password):
    if len(username) > 0 and len(password) > 0:
        ldap_host = 'xxx.xxx.xxx.xxx'
        ldap_port = '389'
        ldap_domain = '@xxx.com'
        ldap_url = 'ldap://' + ldap_host + ':' + ldap_port
        username = username if username.find(ldap_domain) > 0 else username + ldap_domain
        conn = ldap.initialize(ldap_url)
        try:
            conn.simple_bind_s(username, password)
            return True
        except Exception as e:
            return False
    else:
        return False


'''
- linux needs to install openldap-devel(yum install openldap-devel) 
  before install python-ldap(cd python-ldap-3.2.0 && python setup.py install)
- win just use pip install xxxxx.whl(from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap)
- it also works when password is empty
'''
