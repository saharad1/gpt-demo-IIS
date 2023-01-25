import openai
import re
import pandas as pd
import json
from collections import OrderedDict

def gpt(query):
    key = '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'
    openai.api_key = key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        temperature=0.1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = response.choices[0]
    return content.text


def construct_query(details_dict):
    age = details_dict['age']
    weight = details_dict['weight']
    height = details_dict['height']
    goal = details_dict['main_goal']
    fit_level = details_dict['fitness_level']
    perimeters = [details_dict['chest'], details_dict['arm'], details_dict['belly'], details_dict['legs']]

    days_workout = details_dict['num_work_days']
    if perimeters[0] == 0:
        query = f"i want a weekly workout gym program, my age is {age} and my weight is {weight} kg and my height is {height}.\n" \
                f"my goal is to {goal}, my fitness level is {fit_level} and im planning to workout ONLY {days_workout} days a week.\n" \
                f"please include the exercise names and amount of sets, reps and rest time."

    else:
        query = f"i want a weekly workout gym program, my age is {age} and my weight is {weight} kg and my height is {height}.\n" \
                f"my goal is to {goal}, my fitness level is {fit_level} and im planning to workout ONLY {days_workout} days a week.\n" \
                f"my perimeters are: chest={perimeters[0]}, arm={perimeters[1]}, belly={perimeters[2]}, leg={perimeters[3]}" \
                f"please include the exercise names and amount of sets, reps and rest time."
    return query


def construct_plan(username, text):
    delimiters = ['Sunday:', 'Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:', 'Saturday:']
    pattern = '|'.join(map(re.escape, delimiters))
    plan_list = re.split(pattern, text)
    for day in plan_list:
        if day == '':
            plan_list.remove(day)
    plan_list = plan_list[1:]
    plan_dict = OrderedDict()
    i = 0
    for day in plan_list:
        tmp_dict = OrderedDict()
        if 'Rest' not in day:
            i += 1
            day = day.split('\n')
            day = [val for val in day if val != '']
            day = [val for val in day if len(val) > 15]
            for ex in day:
                name, sets_reps = ex.split(':')
                tmp_dict[name] = sets_reps
            plan_dict[f'day{i}'] = tmp_dict.copy()
    set_plan(username, json.dumps(plan_dict))
    return plan_dict


def get_user_details(username: str):
    users_df = pd.read_csv('users.csv')
    return users_df.loc[(users_df['username'] == username)]


def sign_up(details_dict: dict):


    users_df = pd.read_csv('users.csv')
    users_df = users_df.append(details_dict, ignore_index=True)
    users_df.to_csv('users.csv', index=False)


def get_plan(username):
    row = get_user_details(username)
    return json.loads(row['plan'].item())


def set_plan(username, plan_json):
    users_df = pd.read_csv('users.csv')
    users_df.loc[users_df['username'] == username, 'plan'] = plan_json
    users_df.to_csv('users.csv', index=False)

def set_details(username, details_dict):
    users_df = pd.read_csv('users.csv')
    for key in details_dict.keys():
        users_df.loc[(users_df['username'] == username), key] = details_dict[key]
    users_df.to_csv('users.csv', index=False)


def get_ex_replace(ex):
    query = f'give me a list of 3 possible replacements for {ex}'
    res = gpt(query)
    delimiters = ['1.', '2.', '3.']
    pattern = '|'.join(map(re.escape, delimiters))
    ex_list = re.split(pattern, res)[1:]
    ex_list.insert(0, "Choose replacement")
    return ex_list

def set_replacement(username, day_plan_dict, day):
    set_plan(username, json.dumps(day_plan_dict))

def get_how_to(ex):
    return gpt(f'how to do {ex}')


if __name__ == '__main__':
    # print()
    # q = construct_query({'age': 0, 'weight': 0, 'height': 0, 'fitness_level': 'Beginner', 'main_goal': 'Lose fat', 'num_work_days': 3, 'chest': 0.0, 'arm': 0.0, 'belly': 0.0, 'legs': 0.0, 'weight_goal': 0.0})
    # response = gpt(q)
    # plan_list = construct_plan('dor', response)
    # print()
    # print(get_how_to('Bench Press'))
    # q = "what is an exercise replacement for Bench Press"
    # res = gpt(q)

    # get_ex_replace('Bench Press')


    d = {'username': 'dor1', 'password': 'dor2','Email':'dor3',
                           'FullName':'dor4', 'weight':None, 'age':None, 'height':None, 'maon_goal':None,
                           'fitness_level': None, 'chest': None, 'arm':None, 'belly': None, 'legs':None}
    get_plan('admin')
    print()

