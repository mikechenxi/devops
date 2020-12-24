import java.io.*;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.URL;

public class java_call_http {
    public static void main(String[] args) {
        String result = CallHttp("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=xxxx&corpsecret=XXXX", "", "GET", true);
        System.out.println(result);
    }

    public static String CallHttp(String url, String data, String method, boolean userProxy){
        OutputStreamWriter out = null;
        BufferedReader br = null;
        String result = "";
        try {
            URL httpUrl = new URL(url);
            Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("xx.xx.xx.xx", 88));
            HttpURLConnection conn;
            if (userProxy == false)
                conn = (HttpURLConnection) httpUrl.openConnection();
            else
                conn = (HttpURLConnection) httpUrl.openConnection(proxy);

            conn.setConnectTimeout(10);
            conn.setReadTimeout(60);
            conn.setRequestMethod(method);

            conn.setRequestProperty("Accept", "application/json");
            conn.setRequestProperty("Connection", "Keep-Alive");
            conn.setRequestProperty("Accept-Charset", "UTF-8");
            conn.setRequestProperty("Content-Type", "application/json");

            conn.setUseCaches(false);
            conn.setDoOutput(true);
            conn.setDoInput(true);

            out = new OutputStreamWriter(conn.getOutputStream(), "UTF-8");
            out.write(data);
            out.flush();

            InputStream is = conn.getInputStream();
            br = new BufferedReader(new InputStreamReader(is));
            String str = "";
            while ((str = br.readLine()) != null){
                result += str;
            }
            is.close();
            conn.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            try {
                if (out != null){
                    out.close();
                }
                if (br != null){
                    br.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return  result;
    }
}
