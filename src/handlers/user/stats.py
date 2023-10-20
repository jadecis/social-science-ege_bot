from loader import db, dp
from src.keyboards.user.inline_markup import *

def get_stats(user_id):
    decide_tasks= len(db.get_user_tasks(user_id))
    right_tasks= len(db.get_user_tasks_answer(user_id))
    partly_tasks= len(db.get_user_tasks_answer(user_id, param='partly'))
    wrong_tasks= len(db.get_user_tasks_answer(user_id, param='wrong'))
    user_poins= db.get_answer_points(user_id)
    max_points= db.get_max_points(user_id)
    pr_right_tasks= f"{int((right_tasks / decide_tasks) * 100)}%" if decide_tasks != 0 else ''
    pr_partly_tasks= f"{int((partly_tasks / decide_tasks) * 100)}%" if decide_tasks != 0 else ''
    pr_wrong_tasks= f"{int((wrong_tasks / decide_tasks) * 100)}%" if decide_tasks != 0 else ''
    pr_points_tasks= f"{int((user_poins / max_points) * 100)}%" if max_points else ''
    sec_peop_user= db.get_answer_points(user_id, section='Человек и общество')
    sec_peop_max= db.get_max_points(user_id, section='Человек и общество')
    sec_eco_user= db.get_answer_points(user_id, section='Экономика')
    sec_eco_max= db.get_max_points(user_id, section='Экономика')
    sec_policy_user= db.get_answer_points(user_id, section='Политика')
    sec_policy_max= db.get_max_points(user_id, section='Политика')
    sec_social_user= db.get_answer_points(user_id, section='Социология')
    sec_social_max= db.get_max_points(user_id, section='Социология')
    sec_law_user= db.get_answer_points(user_id, section='Право')
    sec_law_max= db.get_max_points(user_id, section='Право')
    pr_peop=f"{int((sec_peop_user / sec_peop_max) * 100)}%" if sec_peop_max else ''
    pr_eco= f"{int((sec_eco_user / sec_eco_max) * 100)}%" if sec_eco_max else ''
    pr_policy= f"{int((sec_policy_user / sec_policy_max) * 100)}%" if sec_policy_max else ''
    pr_social= f"{int((sec_social_user / sec_social_max) * 100)}%" if sec_social_max else ''
    pr_law= f"{int((sec_law_user / sec_law_max) * 100)}%" if sec_law_max else ''
    message=f"""
<b>Всего решено заданий</b> - {decide_tasks}
<b>Решено полностью правильно</b> - {right_tasks}  {pr_right_tasks}
<b>Решено частично правильно</b> - {partly_tasks}  {pr_partly_tasks}
<b>Решено задач неправильно</b> - {wrong_tasks}  {pr_wrong_tasks}
<b>Процент успешности решения задач</b> - {pr_points_tasks}

<b>Успешность выполнения заданий по блокам (количество набранных баллов от их общего числа:)</b>

<b>«Человек и общество»</b> - {pr_peop}
<b>«Экономика»</b> - {pr_eco}
<b>«Политика»</b> - {pr_policy}
<b>«Социология»</b> - {pr_social}
<b>«Право»</b> - {pr_law}"""

    return message
