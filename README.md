 Описание проекта

Проект представляет собой веб-приложение для управления предпрофильными полями пользователей. Ниже приведено подробное описание структуры данных и функциональных блоков программного продукта:

 Метод установки и/или запуска программного продукта
Для запуска программы необходимо установить Python, Flask, sqlite3 и json. После установки необходимо склонировать репозиторий с проектом и запустить файл приложения main_front.py. Приложение будет доступно по адресу http://127.0.0.1:1025/.

 Описание структуры данных
Проект использует базу данных SQLite для хранения информации о пользователях, полях и призах. Структура данных включает следующие таблицы:

1. users: Содержит информацию о пользователях, такую как их уникальный идентификатор, логин, пароль, электронная почта, имя, список призов, флаг администратора и доступные поля.

2. fields: Хранит информацию о полях, доступных пользователям. Включает уникальный идентификатор поля, информацию о поле, список пользователей, связанных с полем, уникальное имя поля и список призов, связанных с полем.

3. prizes: Содержит информацию о призах, предоставляемых пользователям. Включает уникальный идентификатор приза, название приза, символ приза и описание приза.

 Описание функциональных блоков программного продукта
Программный продукт имеет следующие функциональные блоки:

- Регистрация и вход в систему: Пользователи могут зарегистрироваться и войти в систему, указав свой логин, пароль, адрес электронной почты и имя.
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/b459d071-e5cb-4a12-b493-162194a549ef)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/8b2d733c-a235-45c0-9c0c-92ab7c111024)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/16d8335e-a247-4387-9f09-fa2047dda773)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/d087bd81-adb7-4ed1-b44b-8eab9471db64)

  
- Управление полями: Администраторы могут создавать и удалять игровые поля для пользователей. Пользователи могут просматривать и выбирать доступные поля для игры.
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/30487ff7-0927-466d-875a-5819d938abb0)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/acc920d6-dafe-457a-b2ca-1280395e9a66)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/e684ea38-2ebf-4d8b-a9ce-60bf5641352a)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/f0b9a896-0acd-4a56-806a-28e64a49ab34)


- Управление призами: Администраторы могут создавать и редактировать призы, которые могут быть выиграны пользователями.
![image](https://github.com/JLirik/sEA_battLe/assets/118741123/b9800b4a-01f7-4cf0-ad08-464551cd1995)
![image](https://github.com/JLirik/sEA_battLe/assets/118741123/32736318-2246-4993-a3dc-7ead24ce4d10)


- Игра на игровых полях: Пользователи могут играть на морских полях, делая ходы и пытаясь выиграть призы.
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/91e0b287-fa7b-4651-8211-532fbe8f4d0f)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/e2af8f40-21ff-4bb0-829a-7e94657e331e)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/1476bdc7-a156-4d51-b408-a737770a4bea)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/0a66707e-49a1-47c7-93b2-aabff22be43b)
- ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/741e0fda-4c06-4abf-9204-49d40f6a0a8a)


- Просмотр призов: Пользователи могут просматривать список доступных призов и их описания.
  ![image](https://github.com/JLirik/sEA_battLe/assets/118741123/ef7a020b-f67b-414b-96fa-8c56de8794c4)

Это веб-приложение предоставляет удобный интерфейс для управления игровыми полями и выигрышем призов для пользователей.
