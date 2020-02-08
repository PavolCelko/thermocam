#!/usr/bin/python

from smbus2 import SMBus, i2c_msg, SMBusWrapper

TWO_BYTES_LEN = 2

class EEWriteError(Exception):
    """!!!attepmt to write to EEPROM memory which is 10 times only writable."""
    pass

class ReservedRegWrite(Exception):
    """!!!attepmt to write to Reserved Reg memory."""
    pass


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
        
        if 0x2400 <= writeAddress and writeAddress <= 0x273F:
            raise EEWriteError(Exception)

        if 0x8000 <= writeAddress and writeAddress <= 0x800C:
            # this is the only valid option for writing to the 0x8000 status register defined by MLX driver
            if 0x8000 == writeAddress and data == 0x0030:
                pass            
            else:
                raise ReservedRegWrite(Exception)
        
        if 0x8011 <= writeAddress and writeAddress <= 0x8016:
            raise ReservedRegWrite(Exception)

        reg_address = []
        reg_address.append((writeAddress & 0xFF00) >> 8)
        reg_address.append(writeAddress & 0x00FF)

        if writeAddress == 0x800D:
            data = data & ~0x0002
        
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
    def MLX90640_I2CReadMultiReg(self, startReadAddress, data_len):
        reg_address =  [0x00, 0x00]
        reg_address[0] = (startReadAddress & 0xFF00) >> 8
        reg_address[1] = startReadAddress & 0x00FF

        write = i2c_msg.write(self.slave_addr, reg_address)
        
        read = i2c_msg.read(self.slave_addr, data_len * TWO_BYTES_LEN)

        with SMBusWrapper(1) as bus:
            bus.i2c_rdwr(write, read)

        byte_list = list(read)
        word_list = []

        for i in range(0, data_len * TWO_BYTES_LEN, 2):
            word_list.append(((byte_list[i] << 8) & 0xFF00) | (byte_list[i + 1] & 0x00FF))

        return word_list
