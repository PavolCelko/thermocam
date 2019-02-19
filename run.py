#!/usr/bin/python

import mlx_api

def fun1():
    print("FAIL!!!")

def fun2():
    print("PASS...")

def print_reg(reg):
    print("PASS...")

def main():
    
    sensor = mlx_api.Mlx()

    # mode = sensor.MLX90640_GetCurMode()
    # print(hex(mode))
    # sensor.MLX90640_SetChessMode()
    # mode = sensor.MLX90640_GetCurMode()
    # print(hex(mode))
    # sensor.MLX90640_SetInterleavedMode()
    # mode = sensor.MLX90640_GetCurMode()
    # print(hex(mode))

    ee_data = sensor.MLX90640_DumpEE()
    print("dump EE DATA len: ")
    print(len(ee_data))
    print("EE data: ")
    print(ee_data)

    frame_list = sensor.MLX90640_GetFrameData()
    print("FRAME len: ")
    print(len(frame_list))
    print("frame : ")
    print(frame_list)

    Ta = sensor.MLX90640_GetTa(frame_list)
    print("Ta: ")
    print(Ta)

    # frame_list = sensor.MLX90640_CalculateTo()
    # print("FRAME len: ")
    # print(len(frame_list))
    # print("frame 810: ")
    # print(frame_list[810])

    vdd = sensor.MLX90640_GetVdd(frame_list)
    print("vdd: ")
    print(vdd)

    image = sensor.MLX90640_CalculateTo(frame_list, 1, Ta)
    print("calc To len: ")
    print(len(image))
    print("calc To IMAGE: ")
    print(image)

    image = sensor.MLX90640_GetImage(frame_list)
    print("IMAGE len: ")
    print(len(image))
    print("IMAGE: ")
    print(image)

    # print(frame_list)

    
if __name__ == '__main__':
    main()
        