import urllib, urllib2, zipfile, os, sys, xlsxwriter, openpyxl
from openpyxl.styles import Font, Alignment
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

def read_from_excel(file_full_name):
    workbook = openpyxl.load_workbook(file_full_name)
    sheetnames = workbook.sheetnames
    sheetname = workbook[sheetnames[0]]
    titles = ret = []
    row_number = col_number = 0
    for row in sheetname.rows:
        js = {}
        for cell in row:
            if row_number == 0:
                titles.append(cell.value)
            else:
                js[titles[col_number]] = cell.value
                col_number += 1
        if row_number != 0:
            ret.append(js)
        row_number += 1
        col_number = 0
    return ret

def write_to_excel(data, file_full_name):
    workbook = openpyxl.Workbook()
    workbook.create_sheet()
    worksheet = workbook.active
    alignment_title = Alignment(horizontal = 'center')
    font_title = Font(bold = True, size = 10)
    font_content = Font(size = 9)
    row_number = col_number = 1
    for row in data:
        if row_number == 1:
            for key in row.keys():
                worksheet.cell(row_number, col_number, str(key) if key is not None else '')
                worksheet.cell(row_number, col_number).font = font_title
                worksheet.cell(row_number, col_number).alignment = alignment_title
                col_number += 1
        row_number += 1
        col_number = 1
        for key in row.keys():
            worksheet.cell(row_number, col_number, str(row[key]) if row[key] is not None else '')
            worksheet.cell(row_number, col_number).font = font_content
            col_number += 1
    workbook.save(file_full_name)
    log_util.log('file_util.write_to_excel', 'filename:%s' % (file_full_name))

def write_to_excel2(data, file_full_name):
    workbook = xlsxwriter.Workbook(file_full_name)
    worksheet = workbook.add_worksheet()
    style_title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 10})
    style_content = workbook.add_format({'font_size': 9})
    row_number = col_number = 0
    for row in data:
        if row_number == 0:
            for key in row.keys():
                worksheet.write(row_number, col_number, str(key) if key is not None else '', style_title)
                col_number += 1
        row_number += 1
        col_number = 0
        for key in row.keys():
            worksheet.write(row_number, col_number, str(row[key]) if row[key] is not None else '', style_content)
            col_number += 1
    workbook.close()
    log_util.log('file_util.write_to_excel', 'filename:%s' % (file_full_name))
    
# 上传函数参考: https://my.oschina.net/whp/blog/127909
