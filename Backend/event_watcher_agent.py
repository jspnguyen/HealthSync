from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  # Includes both uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))

alice = Agent(name="alice", seed=generate_random_string())

@alice.on_interval(period=4.0)
async def say_hello(ctx: Context):
    messages = [
        {"role": "system", "content": "You are a professional hospital staff allocation manager who judges the level of alert a hospital should be on when a described event occurs. You should only respond with a number from 0-10 based with up to two decimals and nothing else."},
        {"role": "user", "content": f"Medium forest fire"},
    ]

    payload = {
        "messages": messages,
        "stream": False,
        "max_new_tokens": 2048,
        "temperature": 0.9
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    # Print the generated tokens as they get streamed
    alert_level = float(res.text.strip('"'))
    ctx.logger.info(f"The alert level is {alert_level}!")

if __name__ == "__main__":
    alice.run()