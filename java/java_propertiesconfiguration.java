package com.xxx.util;

import org.apache.commons.configuration.PropertiesConfiguration;

public class PropertiesConfigurationUtil {
    private static String path = "xxxx.properties";

    public PropertiesConfigurationUtil(){

    }

    public static String GetProperty(String key) {
        String value = "";
        try {
            PropertiesConfiguration propConfig = new PropertiesConfiguration();
            propConfig.setEncoding("UTF-8");
            propConfig.load(path);
            value = propConfig.getString(key);
        } catch (Exception e){
            e.printStackTrace();
        }
        return value;
    }

    public static void SetProperty(String key, String value) {
        // 中文以unicode格式保存
        try {
            PropertiesConfiguration propConfig = new PropertiesConfiguration();
            propConfig.setEncoding("UTF-8");
            propConfig.load(path);
            propConfig.setFileName(path);
            propConfig.setProperty(key, value);
            propConfig.save();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    public static void RemoveProperty(String key) {
        // 中文以unicode格式保存
        try {
            PropertiesConfiguration propConfig = new PropertiesConfiguration();
            propConfig.setEncoding("UTF-8");
            propConfig.load(path);
            propConfig.setFileName(path);
            propConfig.clearProperty(key);
            propConfig.save();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
