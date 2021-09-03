from ldap3 import Server, Connection
import json, string, random


def auth(username, password):
    if len(username) > 0 and len(password) > 0:
        ldap_host = 'xxx.xxx.xxx.xxx'
        ldap_port = 389
        ldap_user_format = 'cn=%s,ou=xx users,dc=xx,dc=com'
        try:
            server = Server(ldap_host, ldap_port, False)
            connection = Connection(server, ldap_user_format % username, password)
            ret = connection.bind()
            if ret == True:
                connection.unbind()
            return ret
        except Exception as e:
            print(e)
            return False
    else:
        return False

#根据userAccountControl标志：
#512-普通帐户（512），
#514-停用帐户（2 + 512），
#66048-普通帐户+不要过期密码（65536 + 512）
# https://www.pythonheidong.com/blog/article/342515/02fbc41c30859e81cfbd/
def get_state(username):
    if len(username):
        ldap_host = 'xxx.xxx.xxx.xxx'
        ldap_port = 389
        ldap_admin = 'xxxx'
        ldap_admin_password = 'xxxx'
        try:
            server = Server(host = ldap_host, use_ssl = True, get_info = 'ALL')
            connection = Connection(server = server, user = ldap_admin, password = ldap_admin_password, auto_bind = True)
            connection.search('dc=fcbox,dc=com', '(name=%s)' % username, attributes=['userAccountControl'])
            entries = connection.entries
            connection.unbind()
            if len(entries) > 0:
                user_account_control = str(entries[0].userAccountControl.value)
                if user_account_control in ('512', '66048'):
                    return True
                elif user_account_control in ('514', '66050'):
                    return False
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e)
            return None
    else:
        return None
    
def update_password(username, password):
    if len(username) > 0 and len(password) > 0:
        ldap_host = 'xxx.xxx.xxx.xxx'
        ldap_port = 389
        ldap_admin = 'xxxx'
        ldap_admin_password = 'xxxx'
        ldap_user_format = 'cn=%s,ou=xx users,dc=xx,dc=com'
        try:
            server = Server(host = ldap_host, port = ldap_port, use_ssl = True, get_info = 'ALL')
            connection = Connection(server = server, user = ldap_admin, password = ldap_admin_password, auto_bind = True)
            ret = connection.extend.microsoft.modify_password(ldap_user_format % username, password)
            connection.unbind()
            return ret
        except Exception as e:
            print(e)
            return False
    else:
        return False
