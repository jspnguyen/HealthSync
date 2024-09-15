from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  # Includes both uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))

priority_level = Agent(name="priority_level", seed=generate_random_string())

@priority_level.on_interval(period=10.0)
async def say_hello(ctx: Context):
    messages = [
        {"role": "system", "content": "You are a patient priority decision system. Based on the following patient's priority, return a number from 0-10 with up to 3 decimals on how prioritized the patient should be."},
        {"role": "user", "content": f"Patient has a paper cut"},
    ]

    payload = {
        "messages": messages,
        "stream": False,
        "max_new_tokens": 2048,
        "temperature": 0.2
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    # Print the generated tokens as they get streamed
    response = float(res.text.strip('"'))
    ctx.logger.info(response)

if __name__ == "__main__":
    priority_level.run()