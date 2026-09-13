# Подготовка к ЕГЭ по обществознанию

Telegram-бот с заданиями, учётом ответов и статистикой прогресса. Команды /exercise, /stats и /about дополняются административными обработчиками.

**Стек:** aiogram 2, MySQL/PyMySQL, python-dotenv.

## Устройство проекта

- `bot_polling.py` — точка входа.
- `loader.py` — создание клиентов и общих зависимостей.
- `src/handlers/` — Сценарии диалогов.
- `src/keyboards/` — Клавиатуры.
- `src/database/` — Доступ к данным.
- `src/commands/` — Команды.

## Локальная настройка

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Настройте `.env`: `TOKEN_BOT`, `HOST_DB`, `USER_DB`, `PASSWORD_DB`, `NAME_DB`. Загрузчик вызывает `load_dotenv()`. Базу MySQL с таблицами заданий, разделов, пользователей и статистики нужно подготовить отдельно; миграции в репозитории отсутствуют.

После настройки зависимостей и конфигурации запускайте из корня репозитория:

```bash
python bot_polling.py
```

## Статус

Исходный проект для изучения асинхронных ботов и разделения обработчиков. Запуск внешних сервисов и production-готовность этой версии не подтверждены. Код рассчитан на API aiogram 2; обновление до aiogram 3 требует адаптации. 
