import os
from fastapi import FastAPI, WebSocket
from concurrent.futures import ThreadPoolExecutor
import json
import asyncio
from colorama import init
import ptyprocess

init()

app = FastAPI()

import asyncio

async def readline(process, timeout=.01):
    line = ''
    while process.isalive():
        char = process.read(1)
        if char == '':
            await asyncio.sleep(timeout)
        elif char == '\n':
            break
        else:
            line += char

    return line


# WebSocket route
@app.websocket("/espflash")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Receive JSON message containing the file path
    data = await websocket.receive_text()
    message = json.loads(data)
    args = message.get('args')
    print(args)

    try:
        print("Calling espflash...")
        # Execute "espflash" command for the given file path
        process = ptyprocess.PtyProcessUnicode.spawn(["espflash", *args])

        while process.isalive():
            await websocket.send_text(str(await readline(process)))

    except Exception as e:
        print("espflash failed.")
        # Send any exception message back to the client
        await websocket.send_text(str(e))

    print("espflash succeeded!")
    # Close the websocket connection
    await websocket.close()

# WebSocket route for /espflash/ls
@app.websocket("/espflash/ls")
async def espflash_ls_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        print("Executing espflash ls command...")
        # Execute "espflash" command for the given file path
        process = ptyprocess.PtyProcessUnicode.spawn(["espflash", "board-info"])

        saw = False
        while process.isalive():
            
            line = str(await readline(process))
            if line.strip().startswith(">"): 
                if saw: break
                else: saw = True
            
            await websocket.send_text(line)
 
    except Exception as e:
        print("espflash ls command execution failed.")
        # Send any exception message back to the client
        await websocket.send_text(str(e))

    print("espflash ls command execution succeeded!")
    # Close the websocket connection
    await websocket.close()

if __name__ == "__main__":
    flash_bridge_port = int(os.getenv("FLASH_BRIDGE_PORT", 8000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=flash_bridge_port)
