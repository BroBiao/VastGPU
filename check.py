#!/usr/bin/python3

import subprocess
import json
import datetime
from telegram import Bot
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot = Bot(bot_token)
loop = asyncio.get_event_loop()

search_command = [
    'vastai', 'search', 'offers',
    "rentable=true", "verified=false", "external=true",
     "dph<0.5", "gpu_ram>25",
    '--storage', '40',
    '-o', 'dph+',
    '--raw'
]
search_result = subprocess.run(search_command, capture_output=True, text=True)
try:
    search_result = json.loads(search_result.stdout)
except:
    print(search_result.stderr)

def form_create_command(contract_id, image):
    create_command = [
        'vastai', 'create', 'instance', str(contract_id),
        '--image', image,
        '--disk', '40'
        ]
    return create_command

show_instances_command = ['vastai', 'show', 'instances', '--raw']
my_instances = subprocess.run(show_instances_command, capture_output=True, text=True)
try:
    my_instances = json.loads(my_instances.stdout)
except:
    print(my_instances.stderr)

for machine in search_result:
    try:
        cond1 = (my_instances == [])    # 当前无使用中实例
        cond2 = (machine['discounted_dph_total'] < 0.3)
        cond3 = (machine['dlperf_per_dphtotal'] > 500)
        if cond1 and cond2 and cond3:
            contract_id = machine['ask_contract_id']
            if machine['cuda_max_good'] < 12.2:
                print("CUDA version too low...\n")
                print(machine)
                continue
            elif machine['cuda_max_good'] < 12.4:
                image = 'nvidia/cuda:12.2.2-devel-ubuntu22.04'
            elif machine['cuda_max_good'] >= 12.4:
                image = 'nvidia/cuda:12.4.1-devel-ubuntu22.04'
            else:
                pass
            create_command = form_create_command(contract_id, image)
            subprocess.run(create_command, capture_output=True, text=True)
            message = 'New instance created! GPU name: ' + machine['gpu_name']
            loop.run_until_complete(bot.send_message(chat_id=chat_id, text=message))
            break
        else:
            pass
    except:
        print(machine)

print(str(datetime.datetime.now()) + ' ' + 'Nothing happened.')