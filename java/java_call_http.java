import java.io.*;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.URL;

public class java_call_http {
    public static void main(String[] args) {
        String result = CallHttp("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=xxxx&corpsecret=XXXX", "", "GET", false);
        System.out.println(result);
    }

    public static String CallHttp(String url, String data, String method, boolean userProxy){
        OutputStreamWriter outputStreamWriter = null;
        BufferedReader bufferedReader = null;
        String result = "";
        try {
            URL httpUrl = new URL(url);
            HttpURLConnection httpURLConnection;
            if (userProxy == true) {
                String proxy_url = 'http://proxy.xxxx.com'
                int proxy_port = 88
                Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(proxy_url, proxy_port));
                httpURLConnection = (HttpURLConnection) httpUrl.openConnection(proxy);
            } else {
                httpURLConnection = (HttpURLConnection) httpUrl.openConnection();
            }

            httpURLConnection.setConnectTimeout(10);
            httpURLConnection.setReadTimeout(60);
            httpURLConnection.setRequestMethod(method);

            httpURLConnection.setRequestProperty("Accept", "application/json");
            httpURLConnection.setRequestProperty("Connection", "Keep-Alive");
            httpURLConnection.setRequestProperty("Accept-Charset", "UTF-8");
            httpURLConnection.setRequestProperty("Content-Type", "application/json");

            httpURLConnection.setUseCaches(false);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setDoInput(true);

            data = data == null ? "" : data;
            outputStreamWriter = new OutputStreamWriter(httpURLConnection.getOutputStream(), "UTF-8");
            outputStreamWriter.write(data);
            outputStreamWriter.flush();

            InputStream inputStream = httpURLConnection.getInputStream();
            bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"));
            String str = "";
            while ((str = bufferedReader.readLine()) != null){
                result += str;
            }
            inputStream.close();
            httpURLConnection.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            try {
                if (outputStreamWriter != null){
                    outputStreamWriter.close();
                }
                if (bufferedReader != null){
                    bufferedReader.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return  result;
    }
}
