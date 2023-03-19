import requests

token = {'X-Auth-Token': 'jh2gskwd'}
bad_flighting_plan = requests.get("https://dt.miet.ru/ppo_it_final", headers=token).json()["message"]

fly_plan = []
global_flighting = []
print(bad_flighting_plan)
for elem in bad_flighting_plan:
    global_flighting.append([])
    for element in elem['points']:
        print(elem)
        global_flighting[-1].append([element['distance'], element['SH']])
print(global_flighting)
