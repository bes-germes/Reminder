# Reminder
`userGroups` - группы с пользователями. Даём название группе, и добавляем в них пользователей. Формат: "название группы": [имя участников добавляем по почте]  
`rules` - методы, для отправки сообщений пользователям.   
`id` - номер задачи   
`users` - кому отправляем сообщения. Перечисляем группы(allGroups если хотим всем)   
`todo` - Сообщение, которое мы хотим отправить пользователям   
`time` - В какое время будет отправлено первое сообщение. Формат: '%d-%m-%Y_%H:%M:%S'   
`repeat` - С какой частотой мы хотим отправлять сообщения.(Days - отправлять раз в n дней, hours - отправлять раз в n часов, minutes - раз в n минут, none - если хотим, чтобы сообщение отправилось одинь раз).
Пример формата:  
<{
    "userGroups": {
        "group1": [
            "olezhka.kruzhkov@mail.ru",
            "harold@example.com",
            "tod@example.com",
            "dustin@example.com"
        ],
        "group2": [
            "bill@example.com",
            "jerry@example.com",
            "chris@example.com",
            "mike@example.com"
        ],
        "allGroups": [
            "olezhka.kruzhkov@mail.ru",
            "harold@example.com",
            "tod@example.com",
            "dustin@example.com",
            "bill@example.com",
            "jerry@example.com",
            "chris@example.com",
            "mike@example.com"
        ]
    },

    "rules": [
        {
            "id": 0,
            "users": [
                "group2"
            ],
            "todo": "Do smth",
            "time": "06-05-2020_01:41:30",
            "repeat": {
                "days": 0,
                "hours": 0,
                "minutes": 1
            }
        },
        {
            "id": 2,
            "users": [
                "allGroups"
            ],
            "todo": "Do smth",
            "time": "06-05-2020_01:41:30",
            "repeat": {
                "days": 0,
                "hours": 0,
                "minutes": 1
            }
        },
        {
            "id": 3,
            "users": [
                "group1"
            ],
            "todo": "Do smth else",
            "time": "06-05-2020_01:41:30",
            "repeat": "none"
        }
    ]
}>
