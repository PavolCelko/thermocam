#!/usr/bin/python

import mlx_api

def fun1():
    print("FAIL!!!")

def fun2():
    print("PASS...")

def print_reg(reg):
    print("PASS...")

def main():
    print("Firstly, NOTHING.")
    
    sensor = mlx_api.Mlx()

    mode = sensor.MLX90640_GetCurMode()
    print(hex(mode))
    sensor.MLX90640_SetChessMode()
    mode = sensor.MLX90640_GetCurMode()
    print(hex(mode))
    sensor.MLX90640_SetInterleavedMode()
    mode = sensor.MLX90640_GetCurMode()
    print(hex(mode))

    frame_data = sensor.MLX90640_GetFrameData()

    print("FRAME DATA len: ")
    print(len(frame_data))

    res = sensor.MLX90640_GetVdd(frame_data)
    
    # print("unknown mode {:X}".format(mode))

    fun2()

if __name__ == '__main__':
    main()
        