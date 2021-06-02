# mycobot url port
import argparse
import asyncio
import time

from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

import mycobot

arm_port = 'COM3'
arm = None
connection = False
angle_queue = []

def arm_connection(addr, *args):
    global arm
    arm = mycobot.MyCobotCon(arm_port, client, simpleClient)
    res = arm.connect()
    global connection
    connection = True
    print('connected')
    arm.initialize_position()
    arm.set_led_color(255,255,255)
    msg = OscMessageBuilder(address='/util/connection')
    msg.add_arg(res)
    m = msg.build()
    client.send(m)

def arm_disconnection(addr, *args):
    global arm
    res = arm.disconnect()
    global connection
    connection = False
    msg = OscMessageBuilder(address='/util/connection')
    msg.add_arg(res)
    m = msg.build()
    client.send(m)

def arm_initialization(addr, *args):
    global arm
    arm.initialize_position()
    msg = OscMessageBuilder(address='/util/initialize')
    msg.add_arg('initialized')
    m = msg.build()
    client.send(m)

def arm_status(addr, *args):
    global arm
    _status = arm.get_arm_status()
    msg = OscMessageBuilder(address='/util/status')
    msg.add_arg(_status)
    m = msg.build()
    client.send(m)

def arm_release_all_servo(addr, *args):
    global arm
    arm.release_all_servo()
    msg = OscMessageBuilder(address='/util/servo')
    msg.add_arg('released')
    m = msg.build()
    client.send(m)

def arm_set_free_mode(addr, *args):
    global arm
    arm.set_free_mode()
    msg = OscMessageBuilder(address='/util/servo')
    msg.add_arg('free')
    m = msg.build()
    client.send(m)

def arm_command_angles(addr, *args):
    # print('args: {}'.format(args))
    global arm
    arm.command_angle(args[0], args[1])

def arm_sync_angles(addr, *args):
    # print('args: {}'.format(args))
    global arm, angle_queue
    angle_queue.append(args[0])
    # angles = angle_queue[-1]
    angles = [0,0, angle_queue[-1], 0,0,0]
    arm.command_angle(angles, 40)
    time.sleep(.01)

def arm_set_led_color(addr, *args):
    global arm
    arm.set_led_color(args[0], args[1], args[2])

async def loop():
    global arm
    while True:
        if connection:
            simpleClient.send_message('/util/status/angles', arm.get_arm_status()['angles'])
            simpleClient.send_message('/util/status/coords', arm.get_arm_status()['coords'])
            simpleClient.send_message('/util/status/radians', arm.get_arm_status()['radians'])
            # print('{}'.format(arm.get_arm_status()))
        await asyncio.sleep(0.01)

async def init_main(_ip, _port, _dispatcher):
    server = AsyncIOOSCUDPServer((_ip, _port), _dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()

if __name__ == "__main__":
    # tthis server settings
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=12000, help="The port to listen on")
    args = parser.parse_args()

    # another client port settings
    server_ip = '127.0.0.1'
    server_port = 10000
    client = udp_client.UDPClient(server_ip, server_port)

    # first response
    msg = OscMessageBuilder(address='/subprocess/connection')
    msg.add_arg(0)
    m = msg.build()
    client.send(m)

    print('building server')

    dispatcher = Dispatcher()
    dispatcher.map('/connection', arm_connection)
    dispatcher.map('/disconnection', arm_disconnection)
    dispatcher.map('/initialize',arm_initialization)
    dispatcher.map('/getStatus', arm_status)
    dispatcher.map('/releaseAll', arm_release_all_servo)
    dispatcher.map('/free', arm_set_free_mode)
    dispatcher.map('/command/angles', arm_command_angles)
    dispatcher.map('/sync/angles', arm_sync_angles)
    dispatcher.map('/color', arm_set_led_color)

    simpleClient = udp_client.SimpleUDPClient(server_ip, server_port)

    evloop = asyncio.get_event_loop()
    evloop.run_until_complete(init_main(args.ip, args.port, dispatcher))
