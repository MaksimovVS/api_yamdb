# API_YaMDb
## Проект YaMDb для Яндекс.Практикум

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Ресурсы API **YaMDb**
-   Ресурс **auth:** аутентификация.
-   Ресурс **users:** пользователи.
-   Ресурс **titles:** произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
-   Ресурс **categories:** категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
-   Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
-   Ресурс **reviews:** отзывы на произведения. Отзыв привязан к определённому произведению.
-   Ресурс **comments:** комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Пользовательские роли и права доступа
-   **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
-   **Аутентифицированный пользователь (**`user`**)** — может читать всё, как и **Аноним**, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
-   **Модератор (**`moderator`**)** — те же права, что и у **Аутентифицированного пользователя**, плюс право удалять и редактировать **любые** отзывы и комментарии.
-   **Администратор (**`admin`**)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
-   **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Установка
Склонируйте и перейдите в папку с репозиторием:
```bash
git clone https://github.com/MaksimovVS/api_yamdb.git
cd api_yamdb
```
Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
```
Установите зависимости:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполните миграции и запустите сервер:
```bash
python manage.py migrate
python manage.py runserver
```
### Документация
После запуска сервера станет доступна полная документация API и примеры запросов по адресу:
```http
http://127.0.0.1:8000/redoc/
```

### Технологии
django 2.2.16
djangorestframework 3.12.4
PyJWT 2.1.0
djangorestframework-simplejwt 5.2.2
django-filter
django-import-export

### Как добавить информацию в БД
Создайте суперюзера и запустите сервер:
```bash
python manage.py createsuperuser
python manage.py runserver
```
Войдите в админку используя логин и пароль суперюзера
```http
http://127.0.0.1:8000/admin/
```
Перейдите в интересующую Вас категорию
Нажмите на кнопку IMPORT
Выберете файл и укажите его формат
Нажмите на кнопку CONFIRM IMPORT.