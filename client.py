import asyncio
import threading
import websockets
import pydirectinput
import time

key_thread = None
key_thread_stop_flag = False

def hold_key(keys):
    global key_thread_stop_flag
    while not key_thread_stop_flag:
        # Create a copy of the keys set before iterating
        keys_copy = keys.copy()
        for key in keys_copy:
            pydirectinput.keyDown(key)

def release_keys(keys):
    for key in keys:
        pydirectinput.keyUp(key)

async def server(websocket, path):
    global key_thread, key_thread_stop_flag
    print("Connection from the Web")
    await websocket.send("connected")
    keys_pressed = set()

    async for data in websocket:
        print(f"Received from Web: {data}")
        if '[arrow]' in data:
            keys = data.replace('[arrow]', '')
            keys_pressed.update(keys)
            if key_thread is None:
                key_thread_stop_flag = False
                key_thread = threading.Thread(target=hold_key, args=(keys_pressed,))
                key_thread.start()
        elif '[arrow-stop]' in data:
            if key_thread is not None:
                key_thread_stop_flag = True
                key_thread.join()
                key_thread = None
                print(set(keys_pressed))
                release_keys(set(keys_pressed))
                keys_pressed.clear()
        else:
            pydirectinput.keyDown(data)
            pydirectinput.keyUp(data)

        if '[arrow]' not in data:
            release_keys(set(keys_pressed))

start_server = websockets.serve(server, "0.0.0.0", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()