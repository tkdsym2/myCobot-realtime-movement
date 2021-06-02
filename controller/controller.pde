import controlP5.*;

import netP5.*;
import oscP5.*;

OscP5 oscP5;
NetAddress remoteLocation;

ControlP5 cp5;

void setup() {
  size(600, 600);
  frameRate(60);
  oscP5 = new OscP5(this, 10000);
  remoteLocation = new NetAddress("127.0.0.1", 12000);

  // gui
  noStroke();
  cp5 = new ControlP5(this);
  cp5.addSlider("slider")
    .setPosition(100, 305)
    .setRange(0,200)
    .setValue(0)
    .setSize(400,30);
}

void draw() {
  background(255);
}

void slider(float value) {
  println("value: " + value);
  OscMessage msg = new OscMessage("/sync/angles");
  msg.add(value);
  oscP5.send(msg, remoteLocation);
}

void keyPressed() {
  if (key == 'c') {
    println("start connection");
    OscMessage msg = new OscMessage("/connection");
    msg.add(0);
    oscP5.send(msg, remoteLocation);
  }

  if (key == 'd') {
    println("disconnect arm");
    OscMessage msg = new OscMessage("/disconnection");
    msg.add(0);
    oscP5.send(msg, remoteLocation);
  }

  if (key == 'u') {
    println("initialize");
    OscMessage msg = new OscMessage("/initialize");
    msg.add(0);
    oscP5.send(msg, remoteLocation);
  }

  if (key == 'r') {
    println("reset");
    OscMessage msg = new OscMessage("/reset");
    msg.add(0);
    oscP5.send(msg, remoteLocation);
  }
}
