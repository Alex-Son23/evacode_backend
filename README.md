Команда для установки poetry
curl -sSL https://install.python-poetry.org | python3 -

Далее создаем виртуальное окружение:
poetry install

Активируем окружение:
poetry shell

Запускаем django проект:
python manage.py migrate
python manage.py runserver

Пока что для получения данных нужно делать get-запрос на endpoint:
127.0.0.1:8000/market/update_data