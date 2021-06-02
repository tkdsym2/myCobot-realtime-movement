# myCobot realtime movement

Purpose: Controlling the movement of myCobot with sliders (realtime)

# Environment

- Processing v3.5.4
- Python v3.8.2

# controller

Implemented in Processing. When the value of the slider is changed, it is sent to the myCobot Server via osc.

In order to use this, we need to include oscP5 and ControlP5.

# server

## server.py

In order to use this, we need to install pytyhon-osc and pymycobot.
Please run the following command to install libraries.

```
$pip install python-osc pymycobot
```

After installing, the server will be build when you just run.

[This](https://github.com/tkdsym2/myCobot-realtime-movement/blob/main/server/server.py#L79) is where the angle signal sent from the client is received.

## mycobot.py

This is the class that executes the commands implemented in pymycobot.