import urllib, urllib2, zipfile, os, sys, xlsxwriter
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
reload(sys)
sys.setdefaultencoding('utf-8')


def upload_file(url, file_full_name):
    register_openers()
    datagen, headers = multipart_encode({'file': open(file_full_name, 'rb')})
    request = urllib2.Request(url, datagen, headers)
    ret = urllib2.urlopen(request).read()
    return ret


def download_file(url, file_full_name):
    urllib.urlretrieve(url, file_full_name)


def zip_directory(directory_path, file_full_name):
    zip = zipfile.ZipFile(file_full_name, 'w', zipfile.ZIP_DEFLATED)
    for directory, directory_name, file_names in os.walk(directory_path):
        file_path = directory.replace(directory_path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        file_path = file_path and file_path + os.sep or '' # 实现文件夹以及包含的所有文件的压缩
        for file_name in file_names:
            zip.write(os.path.join(directory, file_name).decode(encoding = 'GBK'), file_path + file_name)
    zip.close()


# data [{'':'', '':''}, {'':'', '':''}]
def write_to_excel(data, file_full_name):
    workbook = xlsxwriter.Workbook(file_full_name)
    worksheet = workbook.add_worksheet()
    style_title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10})
    style_content = workbook.add_format({'font_size': 9})
    row = col = 0
    for line in data:
        if row == 0:
            for key in line.keys():
                worksheet.write(row, col, key, style_title)
                col += 1
        row += 1
        col = 0
        for key in line.keys():
            worksheet.write(row, col, str(line[key]) if line[key] is not None else '', style_content)
            col += 1
    workbook.close()

    
# 上传函数参考: https://my.oschina.net/whp/blog/127909
