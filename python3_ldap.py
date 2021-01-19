import json
from ldap3 import Server, Connection


def ldap_auth(username, password):
    if len(username) > 0 and len(password) > 0:
        ldap_host = 'xxx.xxx.xxx.xxx'
        ldap_port = 389
        ldap_user_format = 'cn=%s, ou=xx users, dc=xx, dc=com'
        try:
            server = Server(ldap_host, ldap_port, False)
            conn = Connection(server, ldap_user_format % username, password)
            ret = conn.bind()
            return ret
        except Exception as e:
            return False
    else:
        return False
