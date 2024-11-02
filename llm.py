import json
import re
from raw_file import write_to_file


def get_llm_response(url, data, retry_times=3):
    import requests
    key = "Bearer ai-consultant"
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


def get_doubao_llm_response(url, data, retry_times=3):
    import requests
    key = "Bearer "
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
    # url = 'https://maigpt.in.taou.com/rpc/platforms/go_pbs/maigpt/proxy/v1/chat/completions'
    url = 'https://openkey.cloud/v1/chat/completions'
    data = {
        'messages': [{"role": "user", "content": content}],
        "model": "gpt-4o",
        'temperature': 0.05,
    }
    resp = get_llm_response(url, data)
    try:
        return resp['choices'][0]['message']['content'] if resp else ''
    except Exception as e:
        print(resp)
        return ""


def get_doubao_response(content):
    url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
    data = {
        'messages': [{"role": "user", "content": content}],
        "model": "",
        'temperature': 0.05,
    }
    resp = get_doubao_llm_response(url, data)
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

    prompt_template2 = '''
    # Role: 内容审核/分类运营专家
    
    # Goals:
    - 对提供的热榜问题进行审核&筛选，找出符合条件的问题

    # Constrains:
    - 不会偏离原始信息，对提供的问题进行审核筛选

    # Workflows:
    - 作为专业审核/分类运营专家，你将按照如下的步骤进行工作
    - 1. 剔除问题内容长度超过500字的问题
    - 2. 只选择和政治、国际形势、军事冲突相关的实时事件或历史事件的问题
    - 3. 不可以选择和娱乐、八卦、明星、影视剧、美食、体育相关的实时问题
    - 4. 国际形势、军事冲突相关的问题优先级最高
    - 5. 返回所选的问题id和问题内容
    - 6. 最多选择3个问题，优先级高的问题优先选择
    
    # Output:
    - 严格按照如下 json 列表格式输出：
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

    # Input:
    以下是输入的问题列表：
    '''
    prompt = prompt_template2 + json.dumps(hotlist, indent=4)
    write_to_file(data=prompt, filename='./output/prompt_1_choose_answer.txt')
    res = get_doubao_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res


def ai_role_choose_answer(question, answers):
    prompt_template = '''
    你是一位内容分发专员，你的职责是对问题的回答分发，将不同的回答发给对应的专家。
    
    你服务的专家有5位，分别是：
    1. 老白：需要根据历史逻辑推理的、偏搞笑的答案
    2. 牛总：需要风格幽默诙谐的答案
    3. 翔哥：需要幽默类比的答案
    4. 敏姐：需要充满想象、令疼发笑的答案
    5. 单老板：需要荒诞搞笑的答案
    
    请你从输入的问题和回答列表中，为每个回答选择一个专家，将回答id发给对应的专家。
    要求：
    1. 每个回答只能分发给一个专家
    2. 一个专家仅能收到最匹配的那个回答的id
    3. 如果没有适合某位专家风格的回答，可以不分发任何答案给这位专家
    
    严格按照如下 json 列表格式输出：
        [{
        "name": "老白",
        "answer_id": 1
        },
        {
        "name": "牛总",
        "answer_id": 2
        }
        ]
    
    输入如下：
    
    '''
    prompt = prompt_template
    prompt += f'- 问题：{question}\n\n'
    prompt += '- 回答列表：\n'
    for idx, a in enumerate(answers, start=1):
        idx = str(idx)
        a = a.replace('\n', '')
        prompt += f'- 回答id：{idx}, 回答内容：{a}\n'
    write_to_file(data=prompt, filename='./output/prompt_2_role_choose_answer.txt')
    res = get_doubao_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res


def ai_generate_chat(question, answers, role_answers):
    prompt_template2 = '''
    # Role: 一位擅长政治、国际形势、军事冲突、历史相关话题的圆桌会议主持人

    # Goals:
    - 将问题和回答列表转化为幽默圆桌会议的讨论内容

    # Workflows:
    - 1. 主持人对要讨论的问题进行详细、口语化的阐述，开始引导圆桌会议的讨论。
    - 2. 圆桌会成员包括老白、牛总、小马哥、敏姐、单老板，都是幽默风趣爱举例子的人。
    - 3. 五位专家根据需要对原始回答进行扩充，使回答更加通俗易懂、更幽默。但不可以编造原始答案以外的内容。同时尽量不删除原答案的内容。
    - 4. 五位专家对改写后的回答进行适当的讨论、对比和开玩笑，以引导更深入的讨论。
    - 5. 每个专家只进行一次回答。
    - 6. 最终主持人进行讨论的收尾和感谢观众的发言，这部分要由主持人即兴发挥

    # Output:
    - 输出格式为json格式，包含role（主持人、老白、牛总、小马哥、敏姐、单老板）和content（问题、回答、总结）：
    [
    {
        "role": "主持人",
        "content": "问题：xxx"
    }
    {
        "role": "圆桌会成员",
        "content": "回答：xxx"
    }
    {
        "role": "主持人",
        "content": "串场：xxx"
    }
    ]

    # Input:


    '''
    prompt = prompt_template2
    prompt += f'- 问题：{question}\n\n'
    prompt += '- 原始回答列表：\n'
    for idx, a in enumerate(role_answers, start=1):
        name = a.get("name", "成员")
        origin_answer = answers[a["answer_id"] - 1]
        prompt += f'- {name}的原始答案: {origin_answer}\n'
    write_to_file(data=prompt, filename='./output/prompt_3_generate_chat.txt')
    res = get_doubao_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res


def ai_generate_scripts(question, answers):
    prompt_template2 = '''
    你是一位短视频编剧，现在需要将输入的圆桌会讨论列表转化为一个有趣的短视频剧本。
    请根据以下要求进行创作：
    1. 严格按照原始信息进行剧本编写，不得偏离原始信息
    2. 保持原始信息的本质和准确性
    
    最终输出一个有趣的短视频剧本，包含以下内容：
    - 场景：圆桌会议现场
    - 角色：主持人、成员
    - 对话：主持人提问、圆桌会成员回答、主持人串场、圆桌会成员回答、主持人总结
    
    请根据以下信息进行创作：
    
    '''
    prompt = prompt_template2
    prompt += f'- 圆桌会主题：{question}\n\n'
    prompt += '- 原始回答列表：\n'
    for idx, a in enumerate(answers, start=1):
        name = a.get("role", "成员")
        answer = a.get("content", "")
        prompt += f'- {name}的{answer}\n'
    write_to_file(data=prompt, filename='./output/prompt_4_generate_scripts.txt')
    res = get_doubao_response(prompt)
    return res


def ai_generate_review(question, answers):
    prompt_template = '''
    你是一位擅长政治、国际形势、军事冲突、历史相关的评论员，你的职责是对问题的已有回答进行整合和优化，最终合成对问题高质量回答。
    
    工作流程如下：
    - 分析问题已有的回答列表，判断是否存在开玩笑的回答，如存在则设置其属性为 happy, 否则设置为 professional
    - 对第一步处理后的回答列表，对属性为 happy 的每条内容按照如下原则进行优化：
        1. 使其更加口语化、幽默和接地气
        2. 不要更改回答的核心语义
        3. 优化后的回答不要超过150字
        4. 如果判断无法优化，则不做处理
    - 将第一步处理后的回答列表，对属性为 professional 的每条内容按照如下规则进行优化：
        1. 使回答更加专业真实且符合逻辑，更加适配专业解说的场景
        2. 不要自己杜撰新的内容
        3. 不要删除回答的核心语义
        4. 优化后的回答要保持通顺，具有和原回答一致的逻辑性
        5. 优化后的回答不要再次重复问题
        6. 不要生成新的回答，只对已有的回答进行改写
        7. 改写后的回答要避免被质疑抄袭原回答
        8. 改写后的回答长度不要超过原回答长度
        9. 优化后的回答不要超过600字
    - 对属性为 happy 的内容进行优化进行打分，分数越高表示回答越搞笑
    - 对属性为 professional 的内容进行重写进行打分，分数越高表示回答越专业
    - 返回最终的问题回答列表，条数与原回答条数一致
    
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

    prompt_template2 = '''
    # Role: 一位擅长政治、国际形势、军事冲突、历史相关话题的圆桌会议主持人
    
    # Goals:
    - 将问题和回答列表转化为高质量的圆桌会议讨论内容
    - 对要讨论的问题进行口语化的阐述，以引导圆桌会议的讨论
    - 对问题的现有初版回答进行优化，更贴合圆桌会议的讨论氛围
    
    # Constrains:
    - 不会偏离原始信息，只会基于原有的问题和回答做合理的改编
    - 不应该影响原信息的本质和准确性
    
    # Skills:
    - 熟悉各种新闻，有整理文本信息能力
    - 专业主持人，有强大的圆桌会串场能力、总结能力和引导能力
    - 有非常高超的表达能力
    
    # Workflows:
    - 1. 主持人对要讨论的问题进行详细、口语化的阐述，开始引导圆桌会议的讨论
    - 2. 圆桌会成员均为政治、国际形势、军事冲突、历史相关领域的专家，包括老白（严肃深刻）、牛总（幽默诙谐）、小马哥（深度思想）、敏姐（逻辑性强）、单老板（角度刁钻）
    - 3. 五位专家对原始答案列表中的答案进行选取，每人选择合适一个原始回答，每个专家不能选择相同的回答。如找不到适合自己的原始回答，可以选择参与此次圆桌会议。
    - 4. 五位专家分别对所选取的原始答案进行优化，优化后的回答要调理清楚、逻辑性强，同时描述尽量详尽，不可过分压缩原始回答。每个回答不得少于150字
    - 5. 将优化后的回答作为自己的正式发言回答，每个专家只进行一次回答
    - 6. 在圆桌会议的讨论中，主持人针对不同专家答案要进行适当的串场，以引导继续讨论。串场时不要点评，引导发言时要明确点出专家的名字，这部分要由主持人即兴发挥
    - 7. 最终主持人进行讨论的收尾和感谢观众的发言，这部分要由主持人即兴发挥
    
    # Output:
    - 输出格式为json格式，包含role（主持人、老白、牛总、小马哥、敏姐、单老板）和content（问题、回答、串场、总结）：
    [
    {
        "role": "主持人",
        "content": "问题：xxx"
    }
    {
        "role": "圆桌会成员",
        "content": "回答：xxx"
    }
    {
        "role": "主持人",
        "content": "串场：xxx"
    }
    ]
    
    # Output:
    
    
    '''
    # prompt = prompt_template
    prompt = prompt_template2
    prompt += f'- 问题：{question}\n\n'
    prompt += '- 原始回答列表：\n'
    for a in answers:
        prompt += f'- {a}\n'
    # res = get_gpt_response(prompt)
    res = get_doubao_response(prompt)
    # 提取json
    res = re.findall(r'\[[\s\S]*?\]', res)
    if not res:
        return []
    res = json.loads(res[0])
    return res
