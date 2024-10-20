# coding:utf-8

from zhihu_crawler import login, get_hot_list, get_hot_answer
from llm import ai_choose_question, ai_generate_review, ai_role_choose_answer, ai_generate_chat, ai_generate_scripts
from utils import filter_content
from mail import send_email
from raw_file import write_json_to_file

import json
import time


def main():
    client = login()
    if not client:
        print("Login failed")
        exit(1)
    print("Login success")
    # 获取热榜数据
    hot_list = get_hot_list()
    print("get hot list success")
    # 大模型选择问题
    chosen_questions = ai_choose_question(hot_list)
    print("choose questions success")
    results = []
    # 获取问题答案
    for i in chosen_questions:
        all_answers = []
        time.sleep(3)
        answers = get_hot_answer(client, i["question_id"])
        for a in answers:
            content = filter_content(a.content)
            all_answers.append(content)
        results.append({
            "question": i["question_content"],
            "answers": all_answers,
            "question_id": i["question_id"],
        })
    write_json_to_file(results, "./output/1_raw_results.json")
    # 发送邮件
    send_email(subject="原回答", message=json.dumps(results, indent=4))
    finals = []
    # 获取剧本
    for item in results:
        # 对于每个问题，llm 融合回答
        # res = ai_generate_review(item["question"], item["answers"])
        res = ai_role_choose_answer(item["question"], item["answers"])
        write_json_to_file(res, "./output/2_role_choose_answer.json")
        res2 = ai_generate_chat(item["question"], item["answers"], res)
        write_json_to_file(res, "./output/3_generate_chat.json")
        res3 = ai_generate_scripts(item["question"], res2)
        finals.append({
            "question": item["question"],
            "answer": res3,
            "question_id": item["question_id"]
        })
    write_json_to_file(finals, "./output/4_final_results.json")
    print("get final answers success")
    # 发送邮件
    send_email(subject="gpt 修改版", message=json.dumps(finals, indent=4))


if __name__ == "__main__":
    main()
