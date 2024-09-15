from uagents import Agent, Bureau, Context, Model
import random, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

class Message(Model):
    message: str

nurses_allocator = Agent(name="Nurse Allocator", seed="nurse_seed")
doctors_allocator = Agent(name="Doctor Allocator", seed="doctor_seed")

@nurses_allocator.on_interval(period=60.0)
async def send_message(ctx: Context):
    patients = random.randint(0, 30)
    
    messages = [
        {"role": "system", "content": "You are a professional hospital staff allocation manager. You should only respond with a number and nothing else."},
        {"role": "user", "content": f"Tell me how many nurses should be deployed to a room with {patients} patients"},
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

    num_nurses = int(res.text.strip('"'))
    ctx.logger.info(f"You should send {num_nurses} nurse(s) to a room with {patients} patients.")
    await ctx.send(doctors_allocator.address, Message(message=f"{num_nurses}|{patients}"))

@doctors_allocator.on_message(model=Message)
async def doctor_allocator_message_handler(ctx: Context, sender: str, msg: Message):
    value_list = [int(i) for i in msg.message.split("|")]
    
    messages = [
        {"role": "system", "content": "You are a professional hospital staff allocation manager. You should only respond with a number and nothing else."},
        {"role": "user", "content": f"Tell me how many doctors should be deployed to a room with {value_list[0]} nurses and {value_list[1]} patients."},
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

    num_doctors = int(res.text.strip('"'))
    ctx.logger.info(f"You should send {num_doctors} doctor(s) to a room with {value_list[0]} nurses and {value_list[1]} patients.")

bureau = Bureau()
bureau.add(nurses_allocator)
bureau.add(doctors_allocator)

if __name__ == "__main__":
    bureau.run()