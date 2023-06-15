import sys
import asyncio
import websockets
import os
import json
from colorama import init, Fore

# Initialize colorama
init()

async def connect_and_forward(args):
    flash_bridge_port = int(os.getenv("FLASH_BRIDGE_PORT", 8000))
    
    path = "espflash/ls" if len(args) and args[0] else "espflash"
    
    async with websockets.connect(f'ws://localhost:{flash_bridge_port}/{path}') as websocket:
        if len(args) and args[0] == "ls":
            pass
        else:
            # Call /espflash with the provided arguments
            await websocket.send(json.dumps({"args": args}))

        # Receive and forward messages to the console
        try:
            while True:
                message = await websocket.recv()
                print(format_message(message))
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

def format_message(message):
    if message.startswith(">"):
        return f"{Fore.GREEN}{message}{Fore.RESET}"
    else:
        return message

if __name__ == "__main__":

    args = sys.argv[1:]
    asyncio.get_event_loop().run_until_complete(connect_and_forward(args))
