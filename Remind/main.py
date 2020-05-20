import json
import datetime
import time
import requests
from pathlib import Path

headers = {"Authorization": "Bearer k63r9hirjjdf7xwgd7jyh94zzo"}


def send(rule, team_name):
    r = requests.get("http://localhost:8065/api/v4/teams/name/"+team_name, headers=headers)
    team_id = r.json()["id"]
    r = requests.get("http://localhost:8065/api/v4/teams/" + team_id + "/members", headers=headers)
    team_members = (r.json())
    r = requests.get("http://localhost:8065/api/v4/users", headers=headers)
    users_json = r.json()
    print(rule)
    r = requests.get('http://localhost:8065/api/v4/users/me', headers=headers)
    my_id = (r.json())['id']
    group_users = filter(lambda user: user['id'] in list((d['user_id'] for d in team_members)), users_json)

    data = {}
    with open("rules.json", 'r') as json_file:
        data = json.load(json_file)
    if rule['whom'] == "all":
        for user_name in group_users:
            try:
                id = user_name['id']
                r = requests.post('http://localhost:8065/api/v4/channels/direct',
                                  json=[
                                      id,
                                      my_id
                                  ], headers=headers)
                channel_id = (r.json())['id']
                r = requests.post('http://localhost:8065/api/v4/posts',
                                  json={
                                      "channel_id": channel_id,
                                      "message": "You've got this message as a member of group:" + user_name[
                                          'username'] + "\n" + rule[
                                                     'todo']
                                  }, headers=headers)
            except:
                print("Error")
    elif rule['whom'] == "except":
        for user_name in group_users:
            try:
                if user_name['username'] not in rule['users']:
                    id = user_name['id']
                    r = requests.post('http://localhost:8065/api/v4/channels/direct',
                                      json=[
                                          id,
                                          my_id
                                      ], headers=headers)
                    channel_id = (r.json())['id']
                    r = requests.post('http://localhost:8065/api/v4/posts',
                                      json={
                                          "channel_id": channel_id,
                                          "message": "You've got this message as a member of group:" + user_name[
                                              'username'] + "\n" +
                                                     rule['todo']
                                      }, headers=headers)
            except:
                print("Error")
    else:
        for name in rule['users']:
            try:
                id = next(filter(lambda user: user['username'] == name, group_users))['id']
                r = requests.post('http://localhost:8065/api/v4/channels/direct',
                                  json=[
                                      id,
                                      my_id
                                  ], headers=headers)
                channel_id = (r.json())['id']
                r = requests.post('http://localhost:8065/api/v4/posts',
                                  json={
                                      "channel_id": channel_id,
                                      "message": "You've got this message as a member of group:" + name + "\n" +
                                                 rule['todo']
                                  }, headers=headers)
            except:
                print("Error")


def repeat_to_micros(repeat):
    return int(repeat.get('days', 0) * 8.64e+10 + repeat.get('hours', 0) * 3.6e+9 + repeat.get('minutes',
                                                                                               0) * 6e+7 + repeat.get(
        'seconds', 0) * 1e6)


pr_start_time = datetime.datetime.now()
json_file = open("rules.json", 'r')
data = json.load(json_file)
json_file.close()
for team in data:
    for task in team['rules']:
        if task['when']['principe'] == "once":
            send(task, team['team'])
while True:
    json_file = open("rules.json", 'r')
    data = json.load(json_file)
    json_file.close()
    start_time = datetime.datetime.now()
    for team in data:
        for task in team['rules']:
            task_time = datetime.datetime.strptime(
                task['when']['time'], '%d-%m-%Y_%H:%M:%S')
            if task['when']['principe'] == "period":
                if task['when']['repeat'] != "none" and pr_start_time >= task_time + datetime.timedelta(
                        microseconds=repeat_to_micros(task['when']['repeat'])):
                    task_time = pr_start_time + datetime.timedelta(microseconds=(round(
                        (pr_start_time - task_time).total_seconds() * 1e6) % repeat_to_micros(task['when']['repeat'])))
                if pr_start_time <= task_time < start_time:
                    send(task, team['team'])
            else:
                task['when']['repeat'] = "none"
                if task['when']['repeat'] != "none" and pr_start_time >= task_time + datetime.timedelta(
                        microseconds=repeat_to_micros(task['when']['repeat'])):
                    task_time = pr_start_time + datetime.timedelta(microseconds=(round(
                        (pr_start_time - task_time).total_seconds() * 1e6) % repeat_to_micros(task['when']['repeat'])))
                if pr_start_time <= task_time < start_time:
                    send(task, team['team'])

    time.sleep(1)
    pr_start_time = start_time

