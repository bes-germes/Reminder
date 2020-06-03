import json
import datetime
import requests
import configparser
import logging

logging.basicConfig(filename='log.log', level=logging.DEBUG)

settings = configparser.ConfigParser()
settings.sections()
settings.read('settings.ini')
headers = json.loads((settings['DEFAULT']['headers']))
url = settings['DEFAULT']['url']


def mk_dir(m_id, id_of_users, mk_dir_task):
    r = requests.post(f"http://{url}/api/v4/channels/direct",
                      json=[
                          id_of_users,
                          m_id
                      ], headers=headers)
    channel_id = (r.json())['id']
    r = requests.post(f"http://{url}/api/v4/posts",
                      json={
                          "channel_id": channel_id,
                          "message": "You've got this message as a member" + mk_dir_task[
                              'todo']
                      }, headers=headers)


def send(rule, team_name):
    r = requests.get(f"http://{url}/api/v4/teams/name/" + team_name,
                     headers=headers)
    team_id = r.json()["id"]
    r = requests.get(f"http://{url}/api/v4/teams/{team_id}/members", headers=headers)
    team_members = (r.json())
    r = requests.get(f"http://{url}/api/v4/users", headers=headers)
    users_json = r.json()
    r = requests.get(f"http://{url}/api/v4/users/me", headers=headers)
    my_id = (r.json())['id']
    group_users = list(filter(lambda user: user['id'] in list((d['user_id'] for d in team_members)), users_json))

    if rule['whom'] == "all":
        for user_name in group_users:
            try:
                id = user_name['id']
                mk_dir(my_id, id, rule)
            except:
                logging.warning('No users with such name')
    elif rule['whom'] == "except":
        for user_name in group_users:
            try:
                if user_name['username'] not in rule['users']:
                    id = user_name['id']
                    mk_dir(my_id, id, rule)
            except:
                logging.warning('No users with such name')
    else:
        print(group_users)
        for name in rule['users']:
            try:
                it = next(filter(lambda user: user['username'] == name, group_users), None)
                if not it:
                    continue
                id = it['id']
                mk_dir(my_id, id, rule)
            except:
                logging.warning('No users with such name' + name)


remember_minute = -1
remember_hour = -1
remember_day = -1
with open("rules.json", 'r') as json_file:
    data = json.load(json_file)
json_file.close()
for team in data:
    for task in team['rules']:
        if task['when']['principe'] == "once":
            send(task, team['team'])
while True:
    now = datetime.datetime.now()
    for team in data:
        for task in team['rules']:
            task_time = datetime.datetime.strptime( 
                task['when']['time'], '%d-%m-%Y_%H:%M:%S')
            days_data = task['when']['repeat']['days']
            hours_data = task['when']['repeat']['hours']
            minutes_data = task['when']['repeat']['minutes']
            if task['when']['principe'] == "period":
                period = now - task_time
                if remember_minute != now.minute and remember_day != now.day and remember_hour != now.hour:
                    if period.total_seconds() // 60 % (
                            task['when']['repeat']['days'] * 60 * 24 + task['when']['repeat']['hours'] * 60 +
                            task['when']['repeat']['minutes']) == 0 and now >= task_time:
                        remember_minute = now.minute
                        remember_hour = now.hour
                        remember_day = now.day
                        send(task, team['team'])

            else:
                if (now.day == task_time.day
                        and now.hour == task_time.hour
                        and now.minute == task_time.minute
                        and remember_minute != now.minute):
                    task_time = datetime.timedelta(days=days_data, hours=hours_data,
                                                   minutes=minutes_data)
                    remember_minute = now.minute
                    send(task, team['team'])

