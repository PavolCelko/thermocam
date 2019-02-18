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

    ee_data = sensor.MLX90640_DumpEE()
    print("dump EE DATA len: ")
    print(len(ee_data))

    print("data 51: ")
    print(ee_data[51])

    frame_list = sensor.MLX90640_GetFrameData()
    print("FRAME len: ")
    print(len(frame_list))

    print("frame 810: ")
    print(frame_list[810])

    res = sensor.MLX90640_GetVdd(frame_list)
    print("res: ")
    print(res)
    
    # print("unknown mode {:X}".format(mode))

    fun2()

if __name__ == '__main__':
    main()
        