from aiogram.types import Message, CallbackQuery
from loader import db, dp
from aiogram.dispatcher import FSMContext
from src.keyboards.user.inline_markup import *
from src.states.user.state import Task
from src.handlers.other import check_answer  
from src.handlers.other import random_task

  
@dp.message_handler(content_types=['text'], state= Task.answer)
async def answer_hand(msg: Message, state: FSMContext):
    task_id= db.last_user_answer(msg.chat.id)['task_id']
    exercise= db.get_task_from_id(task_id)
    type_task= exercise['typecheck']
    max_ball=exercise['maxBalls']
    result= check_answer(
        answer=msg.text,
        type_task=type_task,
        trust=str(exercise['answer']),
        max_ball=max_ball
    )
    db.add_user_an(
        user_id=msg.chat.id,
        task_id=task_id,
        user_an=result,
    )
    if result == 2: message="Все правильно! 2 балла из 2."
    if result == 1 and max_ball==2: message=f"Почти удалось! Правильный ответ -  <b>{exercise['answer']}</b>. 1 балл из 2"
    if result == 1 and max_ball==1: message="Все правильно! 1 балл из 1."
    if result == 0: message=f"Косяк! Ответ неправильный. Правильный ответ - <b>{exercise['answer']}</b>."
    but= True if exercise['decide'] else False
    decide= '\n<i>У этой задачи пока нет решения</i>' if not but else ''
    await msg.answer(text=message+decide, reply_markup=answer_menu(but))
    await Task.decide.set()

@dp.callback_query_handler(text='taskDecide', state=Task.answer)
async def showDecide_hand(call: CallbackQuery, state: FSMContext):
    task_id= db.last_user_answer(call.message.chat.id)['task_id']
    exercise= db.get_task_from_id(task_id)
    await call.message.edit_text(text=exercise['decide'], reply_markup=back_task())
    await Task.decide.set()

@dp.callback_query_handler(text='returnTask', state=Task.decide)
async def decidedel_hand(call: CallbackQuery, state: FSMContext):
    task_id= db.last_user_answer(call.message.chat.id)['task_id']
    exercise= db.get_task_from_id(task_id)
    but= True if exercise['decide'] else False
    decide= '\n<i>У этой задачи пока нет решения</i>' if not but else ''
    await call.message.edit_text(f"[{exercise['section']}] {exercise['exercise']}{decide}", reply_markup=task_menu(but))
    await Task.answer.set()

@dp.callback_query_handler(text='nextTask', state= Task.answer)
async def nextTask_hand(call: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    section= data.get('section_id')
    exercise= random_task(user_id=call.message.chat.id, section=section)
    last_task=db.last_user_answer(call.message.chat.id)
    if last_task and last_task['user_answer'] is None:
        db.delete_last_task(last_task['id'])
    db.add_last_task(
        user_id=call.message.chat.id,
        task_id=exercise['id'],
        section=exercise['section_id'],
        max_an= exercise['maxBalls'],
    )
    but= True if exercise['decide'] else False
    decide= '\n<i>У этой задачи пока нет решения</i>' if not but else ''
    await call.message.answer(f"[{exercise['section']}] {exercise['exercise']}{decide}", reply_markup=task_menu(but))
    await Task.answer.set()
    
@dp.callback_query_handler(text='showDecide', state=Task.decide)
async def showDecide_hand(call: CallbackQuery, state: FSMContext):
    task_id= db.last_user_answer(call.message.chat.id)['task_id']
    exercise= db.get_task_from_id(task_id)
    await call.message.edit_text(text=exercise['decide'], reply_markup=answer_menu(False))
    await Task.decide.set()
    
@dp.callback_query_handler(text='nextTaskdelete', state=Task.decide)
async def nextTask_hand(call: CallbackQuery, state: FSMContext):
    data= await state.get_data()
    section= data.get('section_id')
    exercise= random_task(user_id=call.message.chat.id, section=section)
    db.add_last_task(
        user_id=call.message.chat.id,
        task_id=exercise['id'],
        section=exercise['section_id'],
        max_an= exercise['maxBalls'],
    )
    but= True if exercise['decide'] else False
    decide= '\n<i>У этой задачи пока нет решения</i>' if not but else ''
    await call.message.answer(f"[{exercise['section']}] {exercise['exercise']}{decide}", reply_markup=task_menu(but))
    await Task.answer.set()