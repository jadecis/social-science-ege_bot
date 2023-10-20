# import random

# # def check_answer(answer, type_task, trust, max_ball):
# #     if type_task == 1:
# #         miss=len(trust)-len(answer) if len(trust) > len(answer) else 0
# #         for i in trust:
# #             answer=answer.replace(i, '', 1)
# #         miss+=len(answer)
# #         return 0 if len(answer) >= max_ball else max_ball-miss
# #     else:
# #         if max_ball == 1:
# #             return 1 if answer == trust else 0
# #         if answer == trust: return 2 
# #         if len(answer)-len(trust) > 1: return 0
# #         miss=len(trust)-len(answer) if len(trust) > len(answer) else 0
# #         for i in range(0, len(answer)):
# #             try:
# #                 if answer[i] != trust[i]: miss+=1
# #             except Exception as ex:
# #                 print(ex)
# #                 miss+=1    
# #         return 0 if miss > 1 else 2- miss
    
# # print(check_answer(
# #     answer='63',
# #     type_task=1,
# #     trust='123',
# #     max_ball=2
# # ))

# from loader import db

# def get_stats(user_id):
#     decide_tasks= len(db.get_user_tasks(user_id))
#     right_tasks= len(db.get_user_tasks_answer(user_id))
#     partly_tasks= len(db.get_user_tasks_answer(user_id, param='partly'))
#     wrong_tasks= len(db.get_user_tasks_answer(user_id, param='wrong'))
#     user_poins= db.get_answer_points(user_id)
#     max_points= db.get_max_points(user_id)
#     pr_right_tasks=int((right_tasks / decide_tasks) * 100) if decide_tasks != 0 else 100
#     pr_partly_tasks=int((partly_tasks / decide_tasks) * 100) if decide_tasks != 0 else 100
#     pr_wrong_tasks=int((wrong_tasks / decide_tasks) * 100) if decide_tasks != 0 else 100
#     pr_points_tasks=int((user_poins / max_points) * 100) if max_points else 100
#     sec_peop_user= db.get_answer_points(user_id, section='Человек и общество')
#     sec_peop_max= db.get_max_points(user_id, section='Человек и общество')
#     sec_eco_user= db.get_answer_points(user_id, section='Экономика')
#     sec_eco_max= db.get_max_points(user_id, section='Экономика')
#     sec_policy_user= db.get_answer_points(user_id, section='Политика')
#     sec_policy_max= db.get_max_points(user_id, section='Политика')
#     sec_social_user= db.get_answer_points(user_id, section='Социология')
#     sec_social_max= db.get_max_points(user_id, section='Социология')
#     sec_law_user= db.get_answer_points(user_id, section='Право')
#     sec_law_max= db.get_max_points(user_id, section='Право')
#     pr_peop=int((sec_peop_user / sec_peop_max) * 100) if sec_peop_max else 100
#     pr_eco=int((sec_eco_user / sec_eco_max) * 100) if sec_eco_max else 100
#     pr_policy=int((sec_policy_user / sec_policy_max) * 100) if sec_policy_max else 100
#     pr_social=int((sec_social_user / sec_social_max) * 100) if sec_social_max else 100
#     pr_law=int((sec_law_user / sec_law_max) * 100) if sec_law_max else 100
#     message=f"""
# <b>Всего решено заданий</b> - {decide_tasks}
# <b>Решено полностью правильно</b> - {right_tasks}  {pr_right_tasks}%
# <b>Решено частично правильно</b> - {partly_tasks}  {pr_partly_tasks}%
# <b>Решено задач неправильно</b> - {wrong_tasks}  {pr_wrong_tasks}%
# <b>Процент успешности решения задач</b> - {pr_points_tasks}%

# <b>Успешность выполнения заданий по блокам (количество набранных баллов от их общего числа:)</b>

# <b>«Человек и общество»</b> - {pr_peop}%
# <b>«Экономика»</b> - {pr_eco}%
# <b>«Политика»</b> - {pr_policy}%
# <b>«Социология»</b> - {pr_social}%
# <b>«Право»</b> - {pr_law}%"""

#     return message

# def random_task(user_id, section= None):
#     res=db.get_last_tasks(user_id, section)
#     bad_tasks=[str(i['task_id']) for i in res]  
#     exercises= db.getdata_tasks(section=section, bad_tasks=",".join(bad_tasks))
#     i= random.randint(0, len(exercises))
#     return exercises[i]

# # print(db.get_answer_points(849253641, section='Экономика'))
# print(random_task(849253641))