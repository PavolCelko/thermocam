#!/usr/bin/python

import mlx_api
import time
import imager

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

    refreshRate = sensor.MLX90640_GetRefreshRate()
    print("refreshRate: " + str(refreshRate))

    for subpage in range(2):

        frame_list = sensor.MLX90640_GetFrameData()
        print("FRAME len: " + str(len(frame_list)))
        # print("frame : ")
        # print(frame_list)

        subpage = frame_list[833]
        print("subpage: " + str(subpage))
        Ta = sensor.MLX90640_GetTa(frame_list)
        print("Ta: " + str(Ta))
        vdd = sensor.MLX90640_GetVdd(frame_list)
        print("vdd: " + str(vdd))

        image = sensor.MLX90640_CalculateTo(frame_list, 0.95, Ta)
        image = sensor.temp_latest_page
        round_image = []
        for i in image:
            round_image.append(int(round(i)))
        
        # wait for RR - 20%    (which is 80% of RR)
        time.sleep(float(1 / refreshRate) * 0.8)

    # imager.print_temp_integer_map(round_image)

    imager.list_to_image(round_image)    
    
if __name__ == '__main__':
    main()
        
