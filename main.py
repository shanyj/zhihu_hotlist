# coding:utf-8

from zhihu_crawler import login, get_hot_list, get_hot_answer
from llm import ai_choose_question, ai_generate_review
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
    # 获取热榜数据
    hot_list = get_hot_list()
    # 大模型选择问题
    chosen_questions = ai_choose_question(hot_list)
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
    write_json_to_file(results, "./raw_results.json")
    finals = []
    for item in results:
        # 对于每个问题，llm 融合回答
        res = ai_generate_review(item["question"], item["answers"])
        finals.append({
            "question": item["question"],
            "answer": res,
            "question_id": item["question_id"]
        })
    write_json_to_file(finals, "./final_results.json")
    # 发送邮件
    send_email(subject="subject", message=json.dumps(finals, indent=4))


if __name__ == "__main__":
    main()
