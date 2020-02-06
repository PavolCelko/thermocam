#include "MLX90640_I2C_Driver.h"
#include "i2c.h"

static I2CDevice device;

void MLX90640_I2CInit(getTime_t getTime)
{   
    const char *dev = "/dev/i2c-1";
    int fd;

    /* First open i2c bus */
    if ((fd = i2c_open(dev)) == -1) {

        return;
    }

    /* Fill i2c device struct */
    device.bus = fd;
    device.addr = 0x33;
    device.tenbit = 0;
    device.delay = 10;
    device.flags = 0;
    device.page_bytes = 8;
    device.iaddr_bytes = 2; /* Set this to zero, and using i2c_ioctl_xxxx API will ignore chip internal address */
}

int MLX90640_I2CRead(uint8_t slaveAddr, uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data)
{
    int cnt = 0;
    int i = 0;
    char i2cData[1664] = {0};
    uint16_t *p;
    
    p = data;
    //sa = (slaveAddr << 1);
    
    i2c_ioctl_read(&device, startAddress, (void *)i2cData, nMemAddressRead);

    for(cnt=0; cnt < nMemAddressRead; cnt++)
    {
        i = cnt << 1;
        *p++ = (uint16_t)i2cData[i]*256 + (uint16_t)i2cData[i+1];
    }
    
    return 0;   
} 

int MLX90640_I2CWrite(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
    uint8_t sa;
    static uint16_t dataCheck;

    // sa = (slaveAddr << 1);
    // cmd[0] = writeAddress >> 8;
    // cmd[1] = writeAddress & 0x00FF;
    // cmd[2] = data >> 8;
    // cmd[3] = data & 0x00FF;

    //i2c_ioctl_write(const I2CDevice *device, unsigned int writeAddress, const void *buf, size_t len);
    i2c_ioctl_write(&device, writeAddress, (void *)&data, 2);
    
    MLX90640_I2CRead(slaveAddr,writeAddress,1, &dataCheck);
    
    if ( dataCheck != data)
    {
        return -2;
    }    
    
    return 0;
}