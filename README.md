# Yatube API v1
## Базовый функционал для работы с моделями сервиса

### Описание
CRUD функционал для моделей, реализована аутентификация  с помощью токена (JWT\Djoser), разграничены права доступа.
### Запуск проекта
- Клонируйте репозиторий командой:
```
git clone https://github.com/HellfastUSMC/api_final_yatube.git
```
- Перейдите в папку проекта:
```
cd api_final_yatube/
```
- Установите и активируйте виртуальное окружение и запустите его:
```
python -m venv venv
```
```
source venv/scripts/activate/
```
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
- Для доступа к справочной информации по API откройте ссылку
```
http://127.0.0.1:8000/redoc/
```
### Автор
Александр Набиев, студент 26 когорты Яндекс Практикума, факультет backend-разработки python.