import java.util.Hashtable;

import javax.naming.AuthenticationException;
import javax.naming.Context;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;

public class LdapAuthentication {
    public static void main(String[] args) {
        String userName = "username";
        String password = "password";
        String host = "xxx.xxx.xxx.xxx";
        String domain = "@xxx.xxx";
        String port = "389"; 
        String url = new String("ldap://" + host + ":" + port);
        String user = userName.indexOf(domain) > 0 ? userName : userName + domain;
        Hashtable env = new Hashtable();
        DirContext ctx = null;
        env.put(Context.SECURITY_AUTHENTICATION, "simple");
        env.put(Context.SECURITY_PRINCIPAL, user);
        env.put(Context.SECURITY_CREDENTIALS, password);
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, url);
        try {
            ctx = new InitialDirContext(env);
            System.out.println("success!");
        } catch (AuthenticationException e) {
            System.out.println("failed!");
            e.printStackTrace();
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
}

/*
bug: it also works when password is empty
*/
