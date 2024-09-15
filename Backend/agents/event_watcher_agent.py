from uagents import Agent, Context
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

def generate_random_string(length=128):
    letters = string.ascii_letters  
    return ''.join(random.choice(letters) for _ in range(length))

event_agent = Agent(name="event_watcher", seed=generate_random_string())

@event_agent.on_interval(period=4.0)
async def event_watcher(ctx: Context):
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

    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    alert_level = float(res.text.strip('"'))
    ctx.logger.info(f"The alert level is {alert_level}!")

if __name__ == "__main__":
    event_agent.run()