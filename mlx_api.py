import i2c

TV_CHESS_MODE_POS_BIT = 12

class Mlx(object):

    def __init__(self):
        self.i2c = i2c.MlxI2C(0x33)

    # int MLX90640_GetFrameData(uint8_t slaveAddr, uint16_t *frameData);
    # int MLX90640_ExtractParameters(uint16_t *eeData, paramsMLX90640 *mlx90640);
    # float MLX90640_GetVdd(uint16_t *frameData, const paramsMLX90640 *params);
    # float MLX90640_GetTa(uint16_t *frameData, const paramsMLX90640 *params);
    # void MLX90640_GetImage(uint16_t *frameData, const paramsMLX90640 *params, float *result);
    # void MLX90640_CalculateTo(uint16_t *frameData, const paramsMLX90640 *params, float emissivity, float tr, float *result);

    
    def reg2list(reg):
        upper_byte = reg & 0xFF00
        lower_byte = reg & 0x00FF
        return list(upper_byte, lower_byte)

    def MLX90640_GetCurMode(self):
        register = int()
        
        register = self.i2c.MLX90640_I2CReadReg(0x800D)
        
        return register

    def MLX90640_SetInterleavedMode(self):
        register = int()
        register = self.i2c.MLX90640_I2CReadReg(0x800D)
        register = register & ~(0x0001 << TV_CHESS_MODE_POS_BIT)

        self.i2c.MLX90640_I2CWriteReg(0x800D, register)

    def MLX90640_SetChessMode(self):
        register = int()
        register = self.i2c.MLX90640_I2CReadReg(0x800D)
        register = register | (0x0001 << TV_CHESS_MODE_POS_BIT)

        self.i2c.MLX90640_I2CWriteReg(0x800D, register)
