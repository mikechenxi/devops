from lxml import etree

# 解析html
text = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Study/title>
</head>
<body>
    <h1>webpage</h1>
    <p>source link</p>
    <a href="http://www.runoob.com/html/html-tutorial.html" target="_blank">HTML</a> 
    <a href="http://www.runoob.com/python/python-tutorial.html" target="_blank">Python</a>
    <a href="http://www.runoob.com/cplusplus/cpp-tutorial.html" target="_blank">C++</a> 
    <a href="http://www.runoob.com/java/java-tutorial.html" target="_blank">Java</a>
</body>
</html>
'''

# 读取内容
html = etree.HTML(text)
# 读取文件
html = etree.parse(text.html)

print(str(etree.tostring(html), 'utf-8'))

# 获取html下的所有 a 标签
html.xpath('//a')
# 沿着节点顺序找 a 标签
html.xpath('/html/body/a')
# 当前节点后代里面找 a 标签
html.xpath('/descendant::a')
# > [<Element a at 0x22573a07408>, <Element a at 0x22573abdd48>, <Element a at 0x22573abdc48>, <Element a at 0x22573abde08>]

# 按照标签属性筛选
html.xpath('/html/body/a[@href="http://www.runoob.com/python/python-tutorial.html"]')
# 按照文本筛选
html.xpath('/html/body/a[text()="Python"]')
# 按照位置筛选
html.xpath('/html/body/a[position()=2]')

# 获取标签文本
html.xpath('/html/body/a/text()')
# > ['HTML', 'Python', 'C++', 'Java']
html.xpath('/html/body/a')[0].text
# > 'HTML'

# 获取标签属性
html.xpath('/html/body/a/@href')
# > ['http://www.runoob.com/html/html-tutorial.html', 'http://www.runoob.com/python/python-tutorial.html', 'http://www.runoob.com/cplusplus/cpp-tutorial.html', 'http://www.runoob.com/java/java-tutorial.html']
html.xpath('/html/body/a')[0].attrib
# > {'href': 'http://www.runoob.com/html/html-tutorial.html', 'target': '_blank'}
