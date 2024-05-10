import datetime
import requests
from zhihu_oauth import ZhihuClient
from zhihu_oauth.oauth.token import ZhihuToken
from zhihu_oauth.zhcls.question import Question

url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
}

zhihu_token_config = {
    "uid": "f5494f977cf33ec5fe29764f4f8b993f",
    "user_id": 667301141109542912,
    "access_token": "2.1dz5xAgAAAAAA4F75HulNEyYAAABgAlVNaSQrZwBZFMROLPAdX5LzGkb2C2XtzsGGJw",
    "token_type": "bearer",
    "refresh_token": "2.1283516d52441841c37acf2d3",
    "expires_in": 15552000,
    "cookie": {
        "q_c0": "2|1:0|10:1715328617|4:q_c0|92:Mi4xZHo1eEFnQUFBQUFBNEY3NUh1bE5FeVlBQUFCZ0FsVk5hU1FyWndCWkZNUk9MUEFkWDVMekdrYjJDMlh0enNHR0p3|e0cde53ba114a2ccb227e621c630f3ec20e6dfeb395242bf99eb8c97ee5ffb55",
        "z_c0": "2|1:0|10:1715328617|4:z_c0|92:Mi4xZHo1eEFnQUFBQUFBNEY3NUh1bE5FeVlBQUFCZ0FsVk5hU1FyWndCWkZNUk9MUEFkWDVMekdrYjJDMlh0enNHR0p3|971ff8ad2de1423c7c6ad1da1efabca616f4436d7ca101f8a1732dc8f35372d6"
    },
    "unlock_ticket": "ABAMMtq6QgkmAAAAYAJVTXHdPWZIG-n6YABnf4oqmNlX3R-YnUElGg==",
    "lock_in": 1800
}


def login():
    client = ZhihuClient()
    ZhihuToken.from_dict(zhihu_token_config).save('token.pkl')
    client.load_token('token.pkl')
    if client.is_login:
        return client
    return None


def get_hot_list():
    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    hour = now_time.hour

    sess = requests.Session()
    res = sess.get(url, headers=headers)
    data = res.json()["data"]
    hot_list = []
    for item in data:
        item_id = item["target"]["id"]
        item_title = item["target"]["title"]
        hot_list.append("{}: {}".format(item_id, item_title))

    output = "\n".join(hot_list)
    with open("./hotlist/{}_{}_{}_{}.txt".format(year, month, day, hour), mode="w") as f:
        f.write(output)


def get_similiar_question(question_id):
    url = "https://www.zhihu.com/api/v4/questions/{}/similar-questions?limit=2".format(question_id)
    sess = requests.Session()
    res = sess.get(url, headers=headers)
    data = res.json()["data"]
    similiar_questions = []
    for item in data:
        item_id = item["id"]
        item_title = item["title"]
        similiar_questions.append("{}: {}".format(item_id, item_title))

    output = "\n".join(similiar_questions)
    with open("./similiar_questions/{}.txt".format(question_id), mode="w") as f:
        f.write(output)


def get_hot_answer(client, question_id):
    question = client.question(question_id)
    # for _, answer in zip(range(5), question.answers.order_by('default')):
    answers = []
    for _, answer in zip(range(50), question.answers):
        answers.append(answer)
    answers = sorted(answers, key=lambda x: x.voteup_count, reverse=True)
    return answers[:5]


if __name__ == "__main__":
    client = login()
    if not client:
        print("Login failed")
        exit(1)
    answers = get_hot_answer(client, 655536394)
    for a in answers:
        print(a.voteup_count, a.author.name, a.content)
