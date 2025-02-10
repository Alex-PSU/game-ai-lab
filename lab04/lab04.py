import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import TemplateChat

def run_console_chat(**kwargs):
    end_regex = kwargs.get('end_regex', r"SHOP\((.*?)\)END")
    chat = TemplateChat.from_file(**kwargs)
    chat_generator = chat.start_chat()
    print(next(chat_generator))  

    while True:
        try:
            user_input = input('You: ')
            message = chat_generator.send(user_input).strip()
            print(f'Agent: {message}')

            if re.search(end_regex, message):
                print("Ending condition met: Chat is over.")
                break

        except StopIteration as e:
            if isinstance(e.value, tuple):
                print('Agent:', e.value[0])
                ending_match = e.value[1]
                print('Ending match:', ending_match)
            break

lab04_params = {
    "template_file": 'lab04/lab04_trader_chat.json',
    "inventory": 'My Brain',  # Default inventory, will be replaced in the test
    "sign": 'Alexander H',
    "end_regex": r"SHOP\((.*?)\)END"  
}

if __name__ ==  '__main__':
    run_console_chat(**lab04_params)