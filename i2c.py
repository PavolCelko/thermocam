#!/usr/bin/python

from smbus2 import SMBus, i2c_msg, SMBusWrapper

TWO_BYTES_LEN = 2

class MlxI2C:
    def __init__(self, slave_addr):
        self.slave_addr = slave_addr

    # TODO: no need to be an instance method
    def list2reg(self, reg_list):
        register = reg_list[1] & 0x00FF
        register = register | ((reg_list[0] << 8)& 0xFF00)
        
        return register

    #int MLX90640_I2CWrite(uint8_t slaveAddr,uint16_t writeAddress, uint16_t data)
    def MLX90640_I2CWriteReg(self, writeAddress, data):
        reg_address = []
        reg_address.append((writeAddress & 0xFF00) >> 8)
        reg_address.append(writeAddress & 0x00FF)
        reg_address.append((data & 0xFF00) >> 8)
        reg_address.append(data & 0x00FF)

        write = i2c_msg.write(self.slave_addr, reg_address)
        
        with SMBusWrapper(1) as bus:
            bus.i2c_rdwr(write)


    def MLX90640_I2CReadReg(self, readAddress):
        reg_address = [0x00, 0x00]
        reg_address[0] = (readAddress & 0xFF00) >> 8
        reg_address[1] = readAddress & 0x00FF

        write = i2c_msg.write(self.slave_addr, reg_address)
        read = i2c_msg.read(self.slave_addr, TWO_BYTES_LEN)

        with SMBusWrapper(1) as bus:
            bus.i2c_rdwr(write, read)

        return self.list2reg(list(read))
    
    #int MLX90640_I2CRead(uint8_t slaveAddr,uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data);
    def MLX90640_I2CReadMultiReg(self, startReadAddress, data_len, data):
        reg_address =  [0x00, 0x00]
        reg_address[0] = (startReadAddress & 0xFF00) >> 8
        reg_address[1] = startReadAddress & 0x00FF

        write = i2c_msg.write(self.slave_addr, reg_address)
        
        read = i2c_msg.read(self.slave_addr, data_len * TWO_BYTES_LEN)

        with SMBusWrapper(1) as bus:
            bus.i2c_rdwr(write, read)

        return list(read)
