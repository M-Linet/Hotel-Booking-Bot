import json
import os
from datetime import datetime

def initialize_log_file(filename='interaction_log.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as log_file:
            json.dump([], log_file)  

#logging interactions into json file
def log_interaction(user_input, bot_response, filename='interaction_log.json'):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_input': user_input,
        'bot_response': bot_response
    }
    
    #read existing entries
    with open(filename, 'r+') as log_file:
        log_data = json.load(log_file)
        log_data.append(log_entry)
        log_file.seek(0)
        json.dump(log_data, log_file, indent=4)