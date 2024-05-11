import json
import re


def get_llm_response(url, data, retry_times=3):
    import requests
    key = "Bearer ai-consultant"
    headers = {"Authorization": key}
    while retry_times > 0:
        try:
            response = requests.post(url, json=data, headers=headers, timeout=240)
            if response.status_code != 200:
                print('error resp status_code', response.status_code)
                return {}
            response = response.json()
            if response.get('error', None):
                print(response.get('error', ''))
                return {}

            return response
        except Exception as e:
            if retry_times == 0:
                raise e
        retry_times -= 1


def get_gpt_response(content):
    url = 'https://maigpt.in.taou.com/rpc/platforms/go_pbs/maigpt/proxy/v1/chat/completions'
    data = {
        'messages': [{"role": "user", "content": content}],
        "model": "gpt-4",
        'temperature': 0.05,
    }
    resp = get_llm_response(url, data)
    return resp['choices'][0]['message']['content'] if resp else ''


def ai_choose_question(hotlist):
    prompt_template = """
    你是一位内容审核专员，你的职责是对热榜问题进行筛选审核，最终找出最符合条件的问题。

    审核和筛选方法:
    - 剔除问题内容长度超过50字的问题
    - 选择和政治、国际形势、军事冲突、历史相关的问题
    - 不选择和娱乐、八卦、明星、影视剧、美食相关的问题
    - 国际形势、军事冲突相关的问题优先级最高
    - 返回所选的问题id和问题内容
    - 最多选择3个问题，优先级高的问题优先选择

    严格按照如下 json 列表格式输出：
        [
            {
                "question_id": xxx,
                "question_content": xxx
            },
            {
                "question_id": xxx,
                "question_content": xxx
            }
        ]

    以下是输入的问题列表：

    """
    prompt = prompt_template + json.dumps(hotlist, indent=4)
    res = get_gpt_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res
