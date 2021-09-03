import javax.xml.namespace.QName;
import javax.xml.rpc.ParameterMode;
import org.apache.axis.client.Call;
import org.apache.axis.client.Service;
import org.apache.axis.encoding.XMLType;
import org.apache.axis.message.SOAPHeaderElement;
import java.util.*;


public class call_webservice {
    public static void main(String args[]) {
        String url = "http://ip:port/ormrpc/services/EASLogin?wsdl";
        String soapAction = "http://login.webservice.bos.kingdee.com/";
        String function = "login";
        HashMap<String, Object> params = new LinkedHashMap<String, Object>() {
            {
                put("userName", "xx");
                put("password", "xx");
                put("slnName", "xx");
                put("dcName", "xx");
                put("language", "xx");
                put("dbType", 2);
            }
        };
        HashMap<String, String> headers = new LinkedHashMap<String, String>(){};
        Object[] obj = CallWebService(url, soapAction, function, params, headers);
        System.out.println(Arrays.toString(obj));
    }

    public static Object[] CallWebService(String url, String soapAction, String function, HashMap<String, Object> params, HashMap<String, String> headers) {
        Service service = new Service();
        try {
            Call call = (Call) service.createCall();
            call.setTargetEndpointAddress(url);
            call.setUseSOAPAction(true);
            call.setSOAPActionURI(soapAction + function);
            call.setOperationName(new QName(soapAction, function));  // 设置方法名

            Object[] data = new Object[params.size()];
            int i = 0;
            for (String key : params.keySet()) {
                Object value = params.get(key);
                data[i] = value;
                call.addParameter(new QName(soapAction, key), GetXMLType(value), ParameterMode.IN);  // 设置参数
                i++;
            }

            for (String key : headers.keySet()) {
                String value = headers.get(key);
                SOAPHeaderElement soapHeaderElement = new SOAPHeaderElement(soapAction, function);
                soapHeaderElement.setNamespaceURI(soapAction);
                soapHeaderElement.addChildElement(key).setValue(value);
                call.addHeader(soapHeaderElement);  // 设置header
            }

            try {
                call.setReturnType(XMLType.XSD_STRING); //设置返回的数据类型(标准的类型)
                String res = (String) call.invoke(data);
                return new Object[]{res};
            } catch (Exception e) {
                call.setReturnClass(Object[].class); //设置返回的数据类型(通过Object[]接收自定义对象)
                Object[] res = (Object[]) call.invoke(data);
                return res;
            }
        } catch (Exception e) {
            return new Object[]{};
        }
    }

    public static QName GetXMLType(Object object) {
        HashMap<String, QName> hashMap = new HashMap<String, QName>() {
            {
                put("java.lang.Integer", XMLType.XSD_INT);
                put("java.lang.Float", XMLType.XSD_FLOAT);
                put("java.lang.Double", XMLType.XSD_DOUBLE);
                put("java.lang.Long", XMLType.XSD_LONG);
                put("java.lang.Byte", XMLType.XSD_BYTE);
                put("java.lang.String", XMLType.XSD_STRING);
                put("java.lang.Boolean", XMLType.XSD_BOOLEAN);
                put("java.util.Date", XMLType.XSD_DATE);
            }
        };

        String objectType = object.getClass().getName();
        if (hashMap.containsKey(objectType)) {
            return hashMap.get(object.getClass().getName());
        } else {
            return XMLType.XSD_STRING;
        }
    }
}
