package com.xxx.util;

import javax.naming.AuthenticationException;
import javax.naming.Context;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;

public class LdapUtil {
    public LdapUtil(){
        
    }
    
    public static bool LdapAuth(String userName, String password) {
        boolean result = false;
        if(!"".equals(userName) && !"".equals(password)){
            String host = "xxx.xxx.xxx.xxx";
            String port = "389"; 
            String url = new String("ldap://" + host + ":" + port);
            String domain = "@xxx.xxx";
            userName = userName.indexOf(domain) > 0 ? userName : userName + domain;
            Hashtable env = new Hashtable();
            DirContext ctx = null;
            env.put(Context.SECURITY_AUTHENTICATION, "simple");
            env.put(Context.SECURITY_PRINCIPAL, userName);
            env.put(Context.SECURITY_CREDENTIALS, password);
            env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
            env.put(Context.PROVIDER_URL, url);
            try {
                ctx = new InitialDirContext(env);
                result = true;
            } catch (AuthenticationException e) {

            } finally{
                if(null!=ctx){
                    try {
                        ctx.close();
                        ctx=null;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        return result;
    }
}

/*
bug: it also works when password is empty
*/
