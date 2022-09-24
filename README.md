# DJI Mini Controller - Linux Driver

This is a small python script to use the DJI Mini Controller as a joystick on Linux thanks to the serial interface that have the controller.

Based on [hjstn/miniDjiController][https://github.com/hjstn/miniDjiController] for Windows (vJoy).

## Why?
Because I wanted to play [Liftoff](https://store.steampowered.com/app/410340/Liftoff_FPV_Drone_Racing/) on Linux.

## Supported Device

- Bus 001 Device 017: ID 2ca3:0008 DJI Technology Co., Ltd. Mavic Mini MR1SD25 Remote controller

## Installation

```bash
git clone https://github.com/catrielmuller/dji-mini-controller-linux-driver.git
cd dji-mini-controller-linux-driver
pip install -r requirements.txt
```

## Usage

```bash
python main.py -p /dev/ttyACM0
```
