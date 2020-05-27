# Reminder
+ `userGroups` - группы с пользователями. Даём название группе, и добавляем в них пользователей. Формат: "название группы": [имя участников]
+ `allMembers` - хранит весь список участников команды, **заполняется автоматически**   
+ `rules` - методы для отправки сообщений пользователям   
+ `id` - номер задачи   
+ `users` - кому отправляем сообщения. Перечисляем группы(allMembers если хотим всем)   
+ `todo` - Сообщение, которое мы хотим отправить пользователям   
+ `time` - В какое время будет отправлено первое сообщение. Формат: '%d-%m-%Y_%H:%M:%S'   
+ `repeat` - С какой частотой мы хотим отправлять сообщения.(Days - отправлять раз в n дней, hours - отправлять раз в n часов, minutes - раз в n минут, none - если хотим, чтобы сообщение отправилось одинь раз)
