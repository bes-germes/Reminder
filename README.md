**Пример шаблона для rules.json:**  

	[
	{
	
	
		"team": <team_id> # в кавычки нужно вписать название команды 
		
		
		"rules": [
			{
				"id": 0, #номер задачи
				"whom": #принцип рассылки
						# all - всем в группе team_id
						# only - только людям из users
						# except - всем, кроме людей из users
						# по умолчанию only
				"users": [
					#список никнеймов пользователей, str  
				],
				"message": "Do smth", #сообщение, которое будет отправлено 
				"when": { #когда отправляем сообщения  
					"principe": 	# сколько раз отправляем  
									# period - периодичная рассылка начиная с time и периодом repeat
									# single - разовая в time. repeat необязателен. 
									# once - разовая в момент запуска скрипта. time и repeat необязательны
									# по умолчанию - single
					"time": "13-05-2020_13:39:30", # время первой отправки
					"repeat": {#отправка раз в столько-то...  
						"days": 0,
						"hours": 0,
						"minutes": 1
					}
				}
			},
			{
				# ...
			}
		]
	}
	] 
 
---
