import json
import datetime
import time
import requests

headers = {"Authorization": "Bearer k63r9hirjjdf7xwgd7jyh94zzo"}

def send(rule):
    r = requests.get("http://localhost:8065/api/v4/users", headers=headers)
    users_json = r.json()
    print(rule)
    r = requests.get('http://localhost:8065/api/v4/users/me', headers=headers)
    my_id = (r.json())['id']

    data = {}
    with open("rules.json", 'r') as json_file:
        data = json.load(json_file)
    for group in rule['users']:
        for email in data['userGroups'][str(group)]:
            try:
                id = next(filter(lambda user: user['email'] == email, users_json))['id']
                r = requests.post('http://localhost:8065/api/v4/channels/direct',
                              json=[
                                  id,
                                  my_id
                              ], headers=headers)
                channel_id = (r.json())['id']
                r = requests.post('http://localhost:8065/api/v4/posts',
                              json={
                                  "channel_id": channel_id,
                                  "message": "You've got this message as a member of group:" + group + "\n" + rule['todo']
                              }, headers=headers)
            except:
                print("Error")


def repeat_to_micros(repeat):
    return int(repeat.get('days', 0) * 8.64e+10 + repeat.get('hours', 0) * 3.6e+9 + repeat.get('minutes', 0) * 6e+7 + repeat.get('seconds', 0) * 1e6)

pr_start_time = datetime.datetime.now()
while True:
    json_file = open("rules.json", 'r')
    data = json.load(json_file)
    json_file.close()
    start_time = datetime.datetime.now()
    for task in data['rules']:
        task_time = datetime.datetime.strptime(
            task['time'], '%d-%m-%Y_%H:%M:%S')
        if task['repeat'] != "none" and pr_start_time >= task_time + datetime.timedelta(microseconds=repeat_to_micros(task['repeat'])):
            task_time = pr_start_time + datetime.timedelta(microseconds=(round(
                (pr_start_time - task_time).total_seconds() * 1e6) % repeat_to_micros(task['repeat'])))
        if pr_start_time <= task_time < start_time:
            send(task)

    time.sleep(1)
    pr_start_time = start_time
