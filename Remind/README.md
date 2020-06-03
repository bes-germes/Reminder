	[


	{
	
	
		"team": <team_id>
		
		
		"rules": [
			{
				"id": 0,
				"whom": #принцип рассылки
						# all - всем в группе team_id
						# only - только людям из users
						# except - всем, кроме людей из users
						# по умолчанию only
				"users": [
					#список никнеймов юзеров, str
				],
				"message": "Do smth",
				"when": {
					"principe": 	# сколько и когда отправляем
									# period - периодичная рассылка начиная с time и периодом repeat
									# single - разовая в time. repeat необязателен. 
									# once - разовая в момент запуска скрипта. time и repeat необязательны
									# по умолчанию - single
					"time": "13-05-2020_13:39:30", # время первой отправки (покурите datetime)
					"repeat": {
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
 
