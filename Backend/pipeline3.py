import requests
import json
from uagents import Agent, Context
import random
import string
import os
import requests
from dotenv import load_dotenv
import main
import faker

fake = faker.Faker()

load_dotenv()


def generate_random_string(length=128):
    letters = string.ascii_letters  # Includes both uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))


random_event = Agent(name="random_event", seed=generate_random_string())



@random_event.on_interval(period=45.0)
async def random_event_gen(ctx: Context):
    victims = random.randint(20, 70)
    prompt = f"""
        Create a random tragic event. It can be natural, accidental, or human caused. It resulted in {victims} injuries.
        The goal is to create a coherent, realistic narrative that would be plausible in today's world."""

    stream = False
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": os.getenv("TUNE_AUTH"),
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.9,
        "messages":  [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": "What was the tragic event and give a headline?"
            }
        ],
        "model": "rohan/tune-gpt-4o-mini",
        "stream": stream,
        "frequency_penalty":  0.2,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)

    print(response.text)

    main.admit_n_patients(victims)

if __name__ == "__main__":
    random_event.run()