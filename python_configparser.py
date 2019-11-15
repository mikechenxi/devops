#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

def get_config(section, option):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read('.config.ini')
        if cf.has_option(section, option):
            return cf.get(section, option)
        else:
            return ''
    except Exception as e:
        print(e)

def get_configs(configs):
    if len(configs) > 0:
        for section in configs:
            for option in configs[section]:
                configs[section][option] = get_config(section, option)
    return configs

def set_config(section, option, value):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read('.config.ini')
        if cf.has_section(section):
            cf.set(section, option, value)
        file = open('.config.ini', 'w')
        cf.write(file)
        file.close()
    except Exception as e:
        print(e)

def set_configs(configs):
    if len(configs) > 0:
        for section in configs:
            for option in configs[section]:
                value = configs[section][option]
                set_config(section, option, value)
