#!/usr/bin/python
# -*- coding: utf-8 -*

import ldap

def ldap_auth(username, password):
    ldap_host = 'xxx.xxx.xxx.xxx'
    ldap_port = '389'
    ldap_domain = '@xxx.com'
    username = username + ldap_domain if username.find(domain) == -1 else username
    conn = ldap.initialize('ldap://' + ldap_host + ':' + ldap_port)
    try:
        conn.simple_bind_s(username, password)
        return True
    except Exception as e:
        return False



'''
- linux needs to install openldap-devel(yum install openldap-devel) 
  before install python-ldap(cd python-ldap-3.2.0 && python setup.py install)
- win just use pip install xxxxx.whl(from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap)
'''
    
