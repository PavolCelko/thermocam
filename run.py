#!/usr/bin/python

import mlx_api

def main():
    
    sensor = mlx_api.Mlx()

    # print("alpha[333] = " + str(sensor.params.alpha[333]))
    # print("cpKta = " + str(sensor.params.cpKta))
    # print("KsTa = " + str(sensor.params.KsTa))
    
    sensor.MLX90640_SetInterleavedMode()
    if (sensor.MLX90640_GetCurMode() & 0x1000) == 0:
        mode = "TV intlv"
    else:
        mode = "CHESS"
    print("Current mode: " + mode)
    
    frame_list = sensor.MLX90640_GetFrameData()
    print("FRAME len: " + str(len(frame_list)))
    # print(len(frame_list))
    # print("frame : ")
    # print(frame_list)

    Ta = sensor.MLX90640_GetTa(frame_list)
    print("Ta: " + str(Ta))
    
    vdd = sensor.MLX90640_GetVdd(frame_list)
    print("vdd: " + str(vdd))
    
    image = sensor.MLX90640_CalculateTo(frame_list, 0.95, Ta)
    round_image = []
    for i in image:
        round_image.append(int(round(i)))
    print("calc To IMAGE: ")
    for i in range(0, len(round_image), 32):
        print(round_image[i:(i + 31)])

    # image = sensor.MLX90640_GetImage(frame_list)
    # print("IMAGE len: ")
    # print(len(image))
    # print("IMAGE: ")
    # print(image)

    
if __name__ == '__main__':
    main()
        
