package com.xxx.util;

import java.io.*;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class PropertyUtil {
    public PropertyUtil(){
    
    }

    public static String GetProperty(String key) {
        String value = "";
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(FCUtil.class.getClassLoader().getResourceAsStream("xxx.properties"), "utf-8");
            Properties properties = new Properties();
            properties.load(inputStreamReader);
            if(properties.containsKey(key))
                value = properties.get(key).toString();
            inputStreamReader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return value;
    }

    public static Map<String, String> GetProperties(Map<String, String> properties) {
        if (properties.size() > 0) {
            for (Map.Entry<String, String> entry : properties.entrySet()) {
                String key = entry.getKey();
                String value = GetProperty(key);
                entry.setValue(value);
            }
        }
        return properties;
    }

    public static void SetProperty(String key, String value) {
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(FCUtil.class.getClassLoader().getResourceAsStream("xxx.properties"), "utf-8");
            Properties properties = new Properties();
            properties.load(inputStreamReader);

            FileOutputStream fileOutputStream = new FileOutputStream(FCUtil.class.getClassLoader().getResource("xxx.properties").getPath());
            properties.setProperty(key, value);
            properties.store(fileOutputStream, "");

            fileOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void SetProperties(Map<String, String> properties) {
        if (properties.size() > 0) {
            for (Map.Entry<String, String> entry : properties.entrySet()) {
                String key = entry.getKey();
                String value = entry.getValue();
                SetProperty(key, value);
            }
        }
    }

    public static void RemoveProperty(String key) {
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(FCUtil.class.getClassLoader().getResourceAsStream("xxx.properties"), "utf-8");
            Properties properties = new Properties();
            properties.load(inputStreamReader);

            FileOutputStream fileOutputStream = new FileOutputStream(FCUtil.class.getClassLoader().getResource("xxx.properties").getPath());
            if(properties.containsKey(key))
                properties.remove(key);
            properties.store(fileOutputStream, "");

            fileOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void RemoveProperties(List<String> keys) {
        if (keys.size() > 0) {
            for (String key: keys) {
                RemoveProperty(key);
            }
        }
    }
}
