from uagents import Agent, Bureau, Context, Model
import random, string, os, requests
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")

# Define the message structure
class Message(Model):
    message: str

# Create agents
nurses_allocator = Agent(name="Nurse Allocator", seed="nurse_seed")
doctors_allocator = Agent(name="Doctor Allocator", seed="doctor_seed")

# Define behaviour for Emma
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

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    # Print the generated tokens as they get streamed
    num_nurses = int(res.text.strip('"'))
    ctx.logger.info(f"You should send {num_nurses} nurse(s) to a room with {patients} patients.")
    await ctx.send(doctors_allocator.address, Message(message=f"{num_nurses}|{patients}"))

# # Define behavior for handling messages received by Emma
# @emma.on_message(model=Message)
# async def emma_message_handler(ctx: Context, sender: str, msg: Message):
#     ctx.logger.info(f"Received message from {sender}: {msg.message}")

# Define behavior for handling messages received by Liam
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

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )

    # Print the generated tokens as they get streamed
    num_doctors = int(res.text.strip('"'))
    ctx.logger.info(f"You should send {num_doctors} doctor(s) to a room with {value_list[0]} nurses and {value_list[1]} patients.")

# Create a bureau and add agents
bureau = Bureau()
bureau.add(nurses_allocator)
bureau.add(doctors_allocator)

# Run the bureau
if __name__ == "__main__":
    bureau.run()