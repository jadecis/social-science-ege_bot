from loader import db
import random

def check_answer(answer, type_task, trust, max_ball):
    if type_task == 1:
        miss=len(trust)-len(answer) if len(trust) > len(answer) else 0
        for i in trust:
            answer=answer.replace(i, '', 1)
        miss+=len(answer)
        return 0 if len(answer) >= max_ball else max_ball-miss
    else:
        if max_ball == 1:
            return 1 if answer == trust else 0
        if answer == trust: return 2 
        if len(answer)-len(trust) > 1: return 0
        miss=len(trust)-len(answer) if len(trust) > len(answer) else 0
        for i in range(0, len(answer)):
            try:
                if answer[i] != trust[i]: miss+=1
            except Exception as ex:
                print(ex)
                miss+=1    
        return 0 if miss > 1 else 2- miss

import random 

def random_task(user_id, section= None):
    res=db.get_last_tasks(user_id, section)
    bad_tasks=[str(i['task_id']) for i in res]  
    exercises= db.getdata_tasks(section=section, bad_tasks=",".join(bad_tasks))
    if exercises:
        i= random.randint(0, len(exercises))
        return exercises[i]
    return None