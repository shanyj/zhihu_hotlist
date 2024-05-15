import json
import re


def get_llm_response(url, data, retry_times=3):
    import requests
    key = "Bearer ai-consultant"
    # key = "Bearer sk-kp2w55hcJWuR12w6KmaBsI9xVZLwv7q3ptP78slj37DlymM3"
    headers = {"Authorization": key, "Content-Type": "application/json"}
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
    # url = 'https://openkey.cloud/v1/chat/completions'
    data = {
        'messages': [{"role": "user", "content": content}],
        "model": "gpt-4",
        'temperature': 0.05,
    }
    resp = get_llm_response(url, data)
    try:
        return resp['choices'][0]['message']['content'] if resp else ''
    except Exception as e:
        print(resp)
        return ""


def ai_choose_question(hotlist):
    prompt_template = """
    你是一位内容审核专员，你的职责是对热榜问题进行筛选审核，最终找出最符合条件的问题。

    审核和筛选方法:
    - 剔除问题内容长度超过50字的问题
    - 选择和政治、国际形势、军事冲突、历史事件相关的问题
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


def ai_generate_review(question, answers):
    prompt_template = '''
    你是一位擅长政治、国际形势、军事冲突、历史相关的评论员，你的职责是对问题的已有回答进行整合和优化，最终合成对问题高质量回答。
    
    工作流程如下：
    - 分析问题已有的回答列表，判断是否存在开玩笑的回答，如存在则设置其属性为 happy, 否则设置为 professional
    - 对上一步处理后的回答列表，对属性为 happy 的内容进行优化
        - 使其更加口语化、幽默和接地气
        - 不要更改回答的核心语义
        - 如果判断无法优化，则不做处理
    - 将上一步处理后的回答列表，对属性为 professional 的内容进行优化
        - 尝试重写回答，使回答更加专业真实且符合逻辑，更加适配评论员解说的身份
        - 不要自己杜撰新的内容
        - 可删除部分重复的内容，但不要删除回答的核心语义
        - 优化后的回答依旧要保持通顺和原回答一致的逻辑性
        - 优化后的回答不要再次重复问题
        - 不要生成新的回答，只对已有的回答进行改写
        - 改写后的回答长度不要超过原回答长度
        - 如果判断无法优化，则不做处理
    - 对属性为 happy 的内容进行优化进行打分，分数越高表示回答越搞笑
    - 对属性为 professional 的内容进行重写进行打分，分数越高表示回答越专业
    - 返回最终的问题回答列表
    
    严格按照如下 json 列表格式输出：
        [
            {
                "answer": xxx,
                "property": xxx,
                "score": xxx
            },
            {
                "answer": xxx,
                "property": xxx,
                "score": xxx
            }
        ]
        
    以下是输入的问题和已有的回答列表：
    
    '''
    prompt = prompt_template
    prompt += f'问题：{question}\n\n'
    prompt += '回答列表：\n'
    for a in answers:
        prompt += f'- {a}\n'
    res = get_gpt_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res
