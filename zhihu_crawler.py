# coding: utf-8
import datetime
import requests

from utils import filter_content

from zhihu_oauth.oauth.token import ZhihuToken
from zhihu_oauth.zhcls.question import Question
from zhihu_oauth import ZhihuClient

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": '''_9755xjdesxxd_=32; YD00517437729195%3AWM_TID=nOf24KiqJExAFUQRQBcq58zsLFTr0%2Byc; YD00517437729195%3AWM_NI=zMDsgQfXTPzvz82WvDud6%2BcX3srRg6ZKr96APjXtiUz4jPgdiOpkV%2BwF%2FcQLVrWTH99klxwLtIZV36OWz%2B9tfGKm9IUY6wQD62C62vAxum2TEYHBgFxWXJh64vwjvTlhbHc%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2c548829d9cabb36996b48fa2c84b879f8bafb621edb1aed2ed6e918fa7b9fc2af0fea7c3b92aba938c94e65ba6889cb1f97ebae8feb8f550b7bcfacce254f1adbeb3e63e9a95bedab54b94b69895ec5fbaeca6b1e670ab91c08cd521b59ae184d44896ae99b5cb33fbb5a499f648b89796b7b23e8d89b6ccbc80a699858ebc439787fa98d450f6ee8dd7b17e83a8bb8eb160878788a3e64ebc8998abeb3ef8aab98bf560b0b8aea9e237e2a3; _xsrf=lrZRPWEgLz9iX1paRKP9XqDSRXkvpKrM; d_c0=AfBRksMDBhmPTr-edxIXD6XD_rjQLwb_7tA=|1722680369; _zap=78b810d9-a0f7-458d-9f8b-3b0f7317fe46; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1726883740; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1726883740; HMACCOUNT=A6543819E59952B3; __snaker__id=XcQ8KHUZ7P5qoa0W; gdxidpyhxdE=xxxSZd2sRQ%5CRobbVMmk7W8i3Nxj4ssNfznZ9YVthpd5rNSefYAaeTvbzcnjr47XvlhlSY8o%2BnEDmYjbljB1hbA%2FEDSVleNf%2F%2BlDiKWJyqRCVvd5iod8gSmu2fBjQpMjcksu6TyxZ68PCcAgyCJPyZGgiBo9bgxs%2ByofIcDe8Wd2sybLB%3A1726982434293; __zse_ck=003_bTX/bhJ9jDyc2vE7sJTkH1ivFjmXkQXbwRBmrEg5OipOx1kl39K/B6HiJAJJWZ+Oh2EWBYeBLR0O=iTuevvU1=k+dMAoxiiQgop9H+8va+D/; captcha_session_v2=2|1:0|10:1729393809|18:captcha_session_v2|88:N1U3REo0SFVTcUkzMXNaNytIOCs0SUhENno4RFgwWE0ydDZqc0R6cC8wdmJZd3VQVTNHTVArdW81dmhYS2JYMQ==|68f2a0da01b803ba21e6382cd447ae84494bb6b3a446a9a1f4180db27feeb46e; captcha_ticket_v2=2|1:0|10:1729393834|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfS0JzVHlaUXdvdjhoczZ4b3ROMXB5dnVsR1dhV2l0STk4RFpSTWpBZEpORVJmZ3VoeTNuYjFGODg2bnguTGI1SnFuSWkuU3VuNHNrZGFPSGpIVDE0NjNNUWhRS1lwa2pwRzRGYUFPZVlVaTZfeFJIenl6c0ttcG9ZandsdFlxSFZTdjk4R1NRVjR3R0tkNVNUaVREWmpYQmVkQUxHMWNmQlpmcTU1X1VfRFY1bFduakFQbHNpVWVMUTBvWWxJWTBqcWxDb2FoTFFZMnA0TzlKd1RvSzhWQ29GSVN2WmN0NFVUZ2kqeG5SQmw5cGp0UnZVSEx4UkZXaUFDMEJESnpPUypBcXJuRHZLYjBlX2hUcDYybGRXcjJlaEJndGNaVHZNcWZOUFpMeWVxbGhmY01SM0hTOTRmbXE1RTQ5T3YqM1FtUVVtOEJtWGFaWE1ubUN3TlRrMU1PKkRDa29hUjl2VFNldkVtaGRmeHJsRHhveEVmUTNOZmt4LjJQMHNUQmp0ckNDWFVVTUVLeHVYVTlyYThlRlVDNm1aSkJvZGcxc3BTYkc2aTEuZkJXLkhYYmhoSi40OHJtdVNCSlRrdVZBYWswSm5Pb28yb1JvWipGeWtWVVNDR05XbDYzWEYzRmtPYUJkUEZQbW0xanNXdFdrZm9ibnJZZGtaWlNRQjE0WlNZOXRqLlk3N192X2lfMSJ9|bbeff1ce44d74a1faca7614b817000547ba2980da725d068e641d83e35be1cec; q_c1=2bb99efb9f794fc787d77e1b1b5a0524|1729394215000|1729394215000; BEC=d6322fc1daba6406210e61eaa4ec5a7a; z_c0=2|1:0|10:1729394217|4:z_c0|92:Mi4xZHo1eEFnQUFBQUFCOEZHU3d3TUdHU1lBQUFCZ0FsVk52TUlCYUFETUt0dlFRR0VsN2tUVFNfXy16MUlOSVNPLVhR|869a35ebd9d6611d5cca3f514a698460979580a4b0116db680f72b352fba89be; SESSIONID=j3ioIIDVRzGht7J2vuMHSZhxBVUJHY8B8yOU48cRA49; JOID=VlARBkytzuPC0QtVAqyRfULi8TYRy_GLr5tOHVX8uKirpz8TPIS19KTeC1gBEtGJgX2orqzoXDEfMJtpbRgTdec=; osd=W10UCkqgw-bO1wZYB6CXcE_n_TAcxvSHqZZDGFn6taWuqzkeMYG58qnTDlQHH9yMjXulo6nkWjwSNZdvYBUWeeE=; tst=h'''
}

zhihu_token_config = {
    "uid": "f5494f977cf33ec5fe29764f4f8b993f",
    "user_id": 667301141109542912,
    "access_token": "2.1dz5xAgAAAAAB8FGSwwMGGSYAAABgAlVNvMIBaADMKtvQQGEl7kTTS__-z1INISO-XQ",
    "token_type": "bearer",
    "refresh_token": "2.1901c0ae3c68a92af44b50e74",
    "expires_in": 15552000,
    "cookie": {
        "q_c0": "2|1:0|10:1729393852|4:q_c0|92:Mi4xZHo1eEFnQUFBQUFCOEZHU3d3TUdHU1lBQUFCZ0FsVk52TUlCYUFETUt0dlFRR0VsN2tUVFNfXy16MUlOSVNPLVhR|86cd1bfcc4eeab82f110e85950e9307e3906b2cfff3cb08492e09e5e90192a84",
        "z_c0": "2|1:0|10:1729393852|4:z_c0|92:Mi4xZHo1eEFnQUFBQUFCOEZHU3d3TUdHU1lBQUFCZ0FsVk52TUlCYUFETUt0dlFRR0VsN2tUVFNfXy16MUlOSVNPLVhR|a197952e07e465ce813aff7718aa0f9c2260014067f5b37796e53ecf0bbc8a58"
    },
    "unlock_ticket": "ABAMMtq6QgkmAAAAYAJVTcR7FGdY5RMs8Scj0zDHZa7Pk9isqj1P2Q==",
    "lock_in": 1800
}


def login():
    client = ZhihuClient()
    ZhihuToken.from_dict(zhihu_token_config).save('token.pkl')
    client.load_token('./token.pkl')
    client.save_token('token.pkl')
    if client.is_login:
        return client
    return None


def get_hot_list():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    hour = now_time.hour

    sess = requests.Session()
    res = sess.get(url, headers=headers)
    data = res.json()["data"]
    hot_list = []
    res = []
    for item in data:
        item_id = item["target"]["id"]
        item_title = item["target"]["title"]
        hot_list.append("{}: {}".format(item_id, item_title))
        res.append({
            "question_id": item_id,
            "question_content": item_title
        })

    output = "\n".join(hot_list)
    with open("./hotlist/{}_{}_{}_{}.txt".format(year, month, day, hour), mode="w") as f:
        f.write(output)
    return res


def get_similiar_question(client, question_id):
    url = "https://www.zhihu.com/api/v4/questions/{}/similar-questions?limit=2".format(question_id)
    sess = requests.Session()
    res = sess.get(url, headers=headers)
    data = res.json()["data"]
    results = []
    for item in data:
        item_id = item["id"]
        results.append(item_id)
    return results


def get_hot_answer(client, question_id):
    question = client.question(question_id)
    answers = []
    for _, answer in zip(range(100), question.answers):
        answers.append(answer)
    answers = sorted(answers, key=lambda x: x.voteup_count, reverse=True)
    answers = list(filter(lambda x: 90 < len(filter_content(x.content)) < 5000, answers))
    return answers[:8]
