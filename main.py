from zhihu_crawler import login, get_hot_list, get_hot_answer
from llm import ai_choose_question
from utils import filter_content

import json
import time

if __name__ == "__main__":
    client = login()
    if not client:
        print("Login failed")
        exit(1)
    hot_list = get_hot_list()
    chosen_questions = ai_choose_question(hot_list)
    results = []
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
    with open("./results.json", mode="w") as f:
        f.write(json.dumps(results))
