import configparser

def get_config(section, option):
    try:
        cf = configparser.RawConfigParser()
        cf.read('.config.ini')
        if cf.has_option(section, option):
            return cf.get(section, option)
        else:
            return ''
    except Exception as e:
        print(e)

'''
configs = {
    'section1': {
        'option11': 'value11',
        'option12': 'value12'
    }
}
'''
def get_configs(configs):
    if len(configs) > 0:
        for section in configs:
            for option in configs[section]:
                configs[section][option] = get_config(section, option)
    return configs

def set_config(section, option, value):
    try:
        cf = configparser.RawConfigParser()
        cf.read('.config.ini')
        if not cf.has_section(section):
            add_section(section)
            cf.read('.config.ini')
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
                set_config(section, option)

def remove_config(section, option):
    try:
        cf = configparser.RawConfigParser()
        cf.read('.config.ini')
        if cf.has_option(section, option):
            cf.remove_option(section, option)
        file = open('.config.ini', 'w')
        cf.write(file)
        file.close()
    except Exception as e:
        print(e)

def remove_configs(configs):
    if len(configs) > 0:
        for section in configs:
            for option in configs[section]:
                remove_config(section, option)

def add_section(section):
    try:
        cf = configparser.RawConfigParser()
        cf.read('.config.ini')
        if not cf.has_section(section):
            cf.add_section(section)
        file = open('.config.ini', 'w')
        cf.write(file)
        file.close()
    except Exception as e:
        print(e)

def add_sections(sections):
    if len(sections) > 0:
        for section in sections:
            add_section(section)

def remove_section(section):
    try:
        cf = configparser.RawConfigParser()
        cf.read('.config.ini')
        if cf.has_section(section):
            cf.remove_section(section)
        file = open('.config.ini', 'w')
        cf.write(file)
        file.close()
    except Exception as e:
        print(e)

def remove_sections(sections):
    if len(sections) > 0:
        for section in sections:
            remove_section(section)
