
#include <stdio.h>
#include <stdlib.h>

#include "MLX90640_I2C_Driver.h"
#include "MLX90640_API.h"

int main(void)
{
    printf("hello\n");

    int i;
    int status = 37;
    uint16_t aEEData[200] = {0};
    uint16_t aFrame_0[200] = {0};
    uint16_t aFrame_1[200] = {0};
    uint16_t statusReg = 0xFFFF;

    MLX90640_I2CInit();
    printf("%04X\n", statusReg);

    status = MLX90640_DumpEE(0x33, aEEData);    
    if(status == 0)
    {
        printf("Dumpped EE:\n");
        for(i = 0; i < sizeof(aEEData) / sizeof(uint16_t); i++)
            printf("%04X\n", aEEData[i]);        
    }

    // status = MLX90640_GetFrameData(0x33, aFrame_0);    
    // if(status == 0)
    // {
    //     printf("Frame_0:\n");
    //     for(i = 0; i < sizeof(aFrame_0) / sizeof(uint16_t); i++)
    //         printf("%04X\n", aFrame_0[i]);        
    // }

    // status = MLX90640_GetFrameData(0x33, aFrame_1);    
    // if(status == 0)
    // {
    //     printf("Frame_0:\n");
    //     for(i = 0; i < sizeof(aFrame_1) / sizeof(uint16_t); i++)
    //         printf("%04X\n", aFrame_1[i]);        
    // }

    printf("status = %d\n", status);

    free(aEEData);
    free(aFrame_0);
    free(aFrame_1);
    return status;
}