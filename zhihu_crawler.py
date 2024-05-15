# coding: utf-8
import datetime
import requests

from utils import filter_content

from zhihu_oauth import ZhihuClient

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": '''d_c0="AOBe-R7pTROPTjYJzih5TVRFsZUbg8T3fg8=|1624426008"; q_c1=e176cf33f45c4a99b9aba84fefddb6ff|1659669169000|1627291964000; _zap=b8138f7e-017f-4389-b074-740f24fa54f1; dream_token=Yzg4YzY4NDQ1MzEwNDllZWM5ZDBhY2IyMTI5ZDJiNzI1YmYwMDAxMTg0YzAwNDM2ODk2YTYxN2U3MzBjMTM5Mw==; _xsrf=d4bba265-9840-4515-81ea-a6d70b513108; SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1715322393; __snaker__id=LBaQvPhxhdSPRk5m; captcha_session_v2=2|1:0|10:1715328571|18:captcha_session_v2|88:QlJkeUxxcXN1UXZTSEFia2kxeVBlS2lmMk9FZFBwYm45TFYyc1dXbm13Q2x3SW5NZ0FudkdoZHY3dUVqWUxSWA==|7e004ddeecad0f2434a7e0e894658a2762011894b07b7f9a0fc2937499a771e0; captcha_ticket_v2=2|1:0|10:1715328602|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZGxuSWduTkdnV0dFX2FMZTNIM21PcXhZV0pGejFXUHJBUipLUDZHZzFqdzBYcld0TSpibkRBMG1OdzkuekRvblkuYnJLQUhlM3BpTWFFQXNzeHU4MXNuY3ZHUURzcXkzS3p1cnU4LnY0QnZuU0RQVlJuZDFCQV9LZENWeTBpRHdjX3kyTEhiQipfNXhEOWZKQ0hQQUNsLmMzekZYZkJZdjFvZllPUGM5X3F5ZmZWZ0d6cEpzOVlodmprUVk2VjFaeXM4ZDZfbmZDM2tzYTVQMzg2c2gyX0NXUkF0c2FnQ18yNUNRenRHSEphVWRDWUJNKmFRdEc4TU1YR3RZSWx3SnI1V1hTc1l2Undnb1dOMWNKYmN0MVNEaWpKKmQqQkZVRXExTmFoR1pEX2xqeldEc05VaW9IZ0h1MTI5TFRGZGk4SXdaY0wxNnhXOW1NTk41WERnOWlNMnRWY1JhelFnNEJTQy5ETE8uMTVrSDNsczFQcTl3bVFZKmkzUUROVmRxU0twYU5ORjF2THhzSWsyOWdRVUJWTmpjTWhNclpfNEUxbmZaVDZSR3l5VGFaNVhOQ3pSX0FYQ2NsaUYqcXBiNTgwX052Q05VQlZFZWREVXY5MGlXbzIzZ0JhZnBQczlTU1UuakhjMTNkOW5YTTZJMDZkcm9ZOHR4YTA1MGV2Wm1CKnNmTGc3N192X2lfMSJ9|4a075b8342a974bdda6fa3bc8ea5dc9a4b4c8086510a5b4f6d9043805df01e79; gdxidpyhxdE=Lb3e6%2FDoTy2fTN02rI74YfnCRIpX%2F9x4pzlzpCrX%5CGH1MZzNtNElvaEUWbdUyiTHqs8pM%2Bt%2BU9kPVdyIkN%2FKVNV1M6qkOlgt3lmJvdEhwsNRZUid5WLDul%2BKw7JazkXstZiHt4thJ4oKign4EuQTsP2BJSMeRv%5CDEk9R1vkuR89ECZQg%3A1715331514184; ff_supports_webp=1; z_c0=2|1:0|10:1715414442|4:z_c0|92:Mi4xZHo1eEFnQUFBQUFBNEY3NUh1bE5FeVlBQUFCZ0FsVk5hU1FyWndCWkZNUk9MUEFkWDVMekdrYjJDMlh0enNHR0p3|38101ee38a33830a3e2ddd578d4d51dab64e4b99dec0a8aac177923fe4a77f3e; BEC=f3a75d7265fd269b7c515e5c94175904; tst=h; SESSIONID=KWuvlhdx2tcQnC1KfJrK5CT51OXwEqYWIB4Nf2YkrQU; JOID=UloXA0wUzw5m-RG4FBSq0yHd-PAFXZh5F5J73G4huW01kFWLX_D_NAD8E7oRtjAIPANdbF29Ofut9GBqEpDWAl8=; osd=VVoWBEsTzw9h_ha4FROt1CHc__cCXZl-EJV73Wkmvm00l1KMX_H4Mwf8Er0WsTAJOwRabFy6Pvyt9WdtFZDXBVg=; KLBRSID=ed2ad9934af8a1f80db52dcb08d13344|1715417835|1715410350; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1715417836'''
}


# zhihu_token_config = {
#     "uid": "f5494f977cf33ec5fe29764f4f8b993f",
#     "user_id": 667301141109542912,
#     "access_token": "2.1dz5xAgAAAAAA4F75HulNEyYAAABgAlVNaSQrZwBZFMROLPAdX5LzGkb2C2XtzsGGJw",
#     "token_type": "bearer",
#     "refresh_token": "2.1283516d52441841c37acf2d3",
#     "expires_in": 15552000,
#     "cookie": {
#         "q_c0": "2|1:0|10:1715328617|4:q_c0|92:Mi4xZHo1eEFnQUFBQUFBNEY3NUh1bE5FeVlBQUFCZ0FsVk5hU1FyWndCWkZNUk9MUEFkWDVMekdrYjJDMlh0enNHR0p3|e0cde53ba114a2ccb227e621c630f3ec20e6dfeb395242bf99eb8c97ee5ffb55",
#         "z_c0": "2|1:0|10:1715328617|4:z_c0|92:Mi4xZHo1eEFnQUFBQUFBNEY3NUh1bE5FeVlBQUFCZ0FsVk5hU1FyWndCWkZNUk9MUEFkWDVMekdrYjJDMlh0enNHR0p3|971ff8ad2de1423c7c6ad1da1efabca616f4436d7ca101f8a1732dc8f35372d6"
#     },
#     "unlock_ticket": "ABAMMtq6QgkmAAAAYAJVTXHdPWZIG-n6YABnf4oqmNlX3R-YnUElGg==",
#     "lock_in": 1800
# }


def login():
    client = ZhihuClient()
    # ZhihuToken.from_dict(zhihu_token_config).save('token.pkl')
    client.load_token('./token.pkl')
    # client.save_token('token.pkl')
    if client.is_login:
        return client
    return None


def get_hot_list():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=30"
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
    for _, answer in zip(range(50), question.answers):
        answers.append(answer)
    answers = sorted(answers, key=lambda x: x.voteup_count, reverse=True)
    answers = list(filter(lambda x: len(10 < filter_content(x.content)) < 1500, answers))
    return answers[:8]
