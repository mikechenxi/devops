package com.xxx.util;

import java.io.*;
import java.util.*;

public class PropertiesUtil {
    private static String path = "xxxx.properties";
    
    public PropertiesUtil(){
    
    }

    public static String GetProperty(String key) {
        String value = "";
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(PropertiesUtil.class.getClassLoader().getResourceAsStream(path), "utf-8");
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

    public static void SetProperty(String key, String value) {
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(PropertiesUtil.class.getClassLoader().getResourceAsStream(path), "utf-8");
            OrderedProperties orderedProperties = new OrderedProperties();
            orderedProperties.load(inputStreamReader);

            FileOutputStream fileOutputStream = new FileOutputStream(PropertiesUtil.class.getClassLoader().getResource(path).getPath());
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(fileOutputStream);
            orderedProperties.setProperty(key, value);
            orderedProperties.store(outputStreamWriter, "");

            outputStreamWriter.close();
            fileOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void RemoveProperty(String key) {
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(PropertiesUtil.class.getClassLoader().getResourceAsStream(path), "utf-8");
            OrderedProperties orderedProperties = new OrderedProperties();
            orderedProperties.load(inputStreamReader);

            FileOutputStream fileOutputStream = new FileOutputStream(PropertiesUtil.class.getClassLoader().getResource(path).getPath());
            if(orderedProperties.containsKey(key))
                orderedProperties.remove(key);
            orderedProperties.store(fileOutputStream, "");

            fileOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class OrderedProperties extends Properties {
    private File file;
    private final LinkedHashSet<Object> keys = new LinkedHashSet<Object>();

    public OrderedProperties() {
        // TODO Auto-generated constructor stub
    }

    public OrderedProperties(File file) {
        // TODO Auto-generated constructor stub
        this.file = file;
    }

    public File getFile() {
        return file;
    }

    public void setFile(File file) {
        this.file = file;
    }

    public Enumeration<Object> keys() {
        return Collections.enumeration(keys);
    }

    public Object put(Object key, Object value) {
        keys.add(key);
        return super.put(key, value);
    }

    public Set<Object> keySet() {
        return keys;
    }

    public Set<String> stringPropertyNames() {
        Set<String> set = new LinkedHashSet<String>();
        for (Object key : this.keys) {
            set.add((String) key);
        }
        return set;
    }
}
