Cloning Airbnb with python, Django, Tailwind and more ... :)))

## Applications in AirBnb Clone

Users, Lists, Conversations, Reservations, Rooms, Reviews

### Users

### Lists

### Conversations

### Reservations

### Rooms

### Reviews

# 프로젝트 실행하기 위해서 해줘야할 것들

## 1. pipenv 환경 생성

```
python -m pipenv --three
python -m pipenv shell
```

## 2. DB 생성 migrate

```
python manange.py migrate
```

## 3. seed data 생성

순서 지켜서 실행.

```
python manage.py seed_amenities
python manage.py seed_facilities
python manage.py seed_room_types
python manage.py seed_house_rules
python manage.py seed_users
python manage.py seed_rooms
python manage.py seed_reviews
```

## 4. postCSS -> CSS 번들링

```
npm run css
```

## 5. 서버 실행

```
python manage.py runserver
```
