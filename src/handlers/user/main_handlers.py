from aiogram.types import Message, CallbackQuery
from loader import db, dp
from src.keyboards.user.inline_markup import decide_tusk_but, type_decide, section_menu, task_menu
from src.handlers.user.stats import get_stats
from aiogram.dispatcher import FSMContext
from src.handlers.other import random_task
from src.states.user.state import Task


@dp.callback_query_handler(text='instruction', state="*")
async def instruction_hand(call: CallbackQuery):
    await call.message.answer(
"""Как оценивается?

За успешно выполненное задание первой части ЕГЭ по обществознанию ты можешь получить 1-2 балла, в зависимости от задания.

Если задание оценивается в 2 балла, ты можешь допустить 1 любую ошибку - получишь 1 балл из 2. Если же ошибок 2 и более - досвидули, за задание ты получишь 0 баллов.

Если задание оценивается в 1 балл, то любая ошибка сразу стоит тебе этого балла.

Сколько правильных вариантов ответа?

В заданиях, где нужно выбрать варианты ответа, правильных вариантов может быть от 2 до 4. То есть в заданиях, где есть 5 вариантов ответа, 4 могут быть правильными. Или 3. Или 2. Ты понимаешь.

Как лучше решать задачки?

1. Внимательно читай задание и варианты ответа. Около 20% ошибок егэшники совершают потому, что что-то неправильно прочитали.
2. Сначала выбери то, что точно подходит или не подходит. А потом разбирайся с остальным.
3. Не торопись.
4. Обращай внимание на такие слова как "никогда", "всегда", "только", "в основном" и самое главное на частицу "не". Иногда их наличие в ответе кардинальным образом влияет на его правильность.""",
reply_markup=decide_tusk_but('deleteinst'))
    
@dp.callback_query_handler(text='stat', state="*")
async def stat_hand(call: CallbackQuery):
    message=get_stats(call.message.chat.id)
    await call.message.answer(message)


@dp.callback_query_handler(text='decide', state="*")
async def decide_hand(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Можем решать задачки рандомно по всем темам, а можем по отдельным разделам.   "
                              +"Что выбираешь?   P.S. Если не знаешь, как проверяются задания, или хочешь получить"
                              +"советы по решению, то жми инструкцию.", reply_markup=type_decide())

@dp.callback_query_handler(text='deleteinst', state="*")
async def decide_hand(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Можем решать задачки рандомно по всем темам, а можем по отдельным разделам.   "
                              +"Что выбираешь?   P.S. Если не знаешь, как проверяются задания, или хочешь получить"
                              +"советы по решению, то жми инструкцию.", reply_markup=type_decide())

@dp.callback_query_handler(text='random', state="*")
async def random_hand(call: CallbackQuery, state: FSMContext):
    last_task=db.last_user_answer(call.message.chat.id)
    if last_task and last_task['user_answer'] is None:
        exercise= db.get_task_from_id(last_task['id'])
    else:
        exercise= random_task(user_id=call.message.chat.id)
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
    
    
@dp.callback_query_handler(text='section', state="*")
async def section_hand(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Как скажешь.\nКакой раздел будем отрабатывать?", reply_markup=section_menu())

@dp.callback_query_handler(text_contains='section_', state="*")
async def section_filter_hand(call: CallbackQuery, state: FSMContext):
    sec_filter= int(call.data.replace('section_', ''))
    exercise= random_task(user_id=call.message.chat.id, section=sec_filter)
    if exercise:
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
        await state.update_data(section_id=exercise['section_id'])
        await Task.answer.set()
    else:
        await call.message.edit_text("На данный блок пока нет заданий(\nВыбери другой блок!", reply_markup=section_menu())