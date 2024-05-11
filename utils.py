import re, html


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def filter_content(content):
    html_content = html.unescape(content)
    regex = r'\>.*?\<'
    listAll = re.findall(regex, html_content)
    listToSave = [i[1:-1] for i in listAll if i != '><' and len(i) > 2]
    strContent = ' '.join(listToSave)
    strContent = filter_emoji(strContent)
    return strContent
