import i2c
import paramsMLX
import copy
import math

TV_CHESS_MODE_POS_BIT = 12

class Mlx(object):

    def __init__(self):
        self.i2c = i2c.MlxI2C(0x33)
        eeData = self.MLX90640_DumpEE()

        self.const_params = paramsMLX.params(eeData)
        self.params = copy.copy(self.const_params)
        
    
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

    # int MLX90640_DumpEE(uint8_t slaveAddr, uint16_t *eeData)
    def MLX90640_DumpEE(self):
    
        eeData = self.i2c.MLX90640_I2CReadMultiReg(0x2400, 832)

        return eeData

    
    # int MLX90640_GetFrameData(uint8_t slaveAddr, uint16_t *frameData)
    def MLX90640_GetFrameData(self):
    
        # uint16_t dataReady = 1;
        # uint16_t controlRegister1;
        # uint16_t statusRegister;
        # int error = 1;
        cnt = 0
        frame_data = []

        
        dataReady = 0;
        while dataReady == 0:
            # error = MLX90640_I2CRead(slaveAddr, 0x8000, 1, &statusRegister);
            statusRegister = self.i2c.MLX90640_I2CReadReg(0x8000)
            
            # if error != 0:
            #     return error;
            
            dataReady = statusRegister & 0x0008;
            
        while(dataReady != 0 and cnt < 5):
            # MLX90640_I2CWrite(slaveAddr, 0x8000, 0x0030)
            self.i2c.MLX90640_I2CWriteReg(0x8000, 0x0030)
            # if(error == -1):
            #     return error;
                
            # error = MLX90640_I2CRead(slaveAddr, 0x0400, 832, frameData)
            frame_data = self.i2c.MLX90640_I2CReadMultiReg(0x0400, 832)
            # if(error != 0):
            #     return error;
                    
            statusRegister = self.i2c.MLX90640_I2CReadReg(0x8000)
            # if(error != 0):
            #     return error;
            
            dataReady = statusRegister & 0x0008
            cnt = cnt + 1
        
        if(cnt > 4):
            return -8
        
        # error = MLX90640_I2CRead(slaveAddr, 0x800D, 1, &controlRegister1);
        controlRegister1 = self.i2c.MLX90640_I2CReadReg(0x8000)
        # frame_data[832] = controlRegister1
        # frame_data[833] = statusRegister & 0x0001
        frame_data.append(controlRegister1)
        frame_data.append(statusRegister & 0x0001)
        
        # if(error != 0):
        #     return error;
        
        return frame_data;    


    # int MLX90640_GetSubPageNumber(uint16_t *frameData)
    def MLX90640_GetSubPageNumber(frameData):
    
        return frameData[833];
      

#void MLX90640_GetImage(uint16_t *frameData, const paramsMLX90640 *params, float *result)
    def MLX90640_GetImage(self, frameData):
    
        # float vdd;
        # float ta;
        # float gain;
        irDataCP = 2*[float()]
        # float irData;
        # float alphaCompensated;
        # uint8_t mode;
        # int8_t ilPattern;
        # int8_t chessPattern;
        # int8_t pattern;
        # int8_t conversionPattern;
        # float image;
        # uint16_t subPage;

        self.params = copy.copy(self.const_params)
        result = 768 * [float()]
        
        subPage = frameData[833]
        vdd = self.MLX90640_GetVdd(frameData)
        ta = self.MLX90640_GetTa(frameData)
        
    # ------------------------- Gain calculation -----------------------------------    
        gain = frameData[778]
        if(gain > 32767):
            gain = gain - 65536
                
        gain = self.params.gainEE / gain; 
    
    # ------------------------- Image calculation -------------------------------------    
        mode = (frameData[832] & 0x1000) >> 5;
        
        irDataCP[0] = frameData[776]
        irDataCP[1] = frameData[808]
        for i in range(2):
        
            if irDataCP[i] > 32767:
                irDataCP[i] = irDataCP[i] - 65536;
            irDataCP[i] = irDataCP[i] * gain;
        
        irDataCP[0] = irDataCP[0] - self.params.cpOffset[0] * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        if( mode ==  self.params.calibrationModeEE):
            irDataCP[1] = irDataCP[1] - self.params.cpOffset[1] * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        else:
            irDataCP[1] = irDataCP[1] - (self.params.cpOffset[1] + self.params.ilChessC[0]) * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        
        for pixelNumber in range(768):
            ilPattern = pixelNumber / 32 - (pixelNumber / 64) * 2
            chessPattern = ilPattern ^ (pixelNumber - (pixelNumber/2)*2)
            conversionPattern = ((pixelNumber + 2) / 4 - (pixelNumber + 3) / 4 + (pixelNumber + 1) / 4 - pixelNumber / 4) * (1 - 2 * ilPattern)
            
            if(mode == 0):
                pattern = ilPattern; 
            else:
                pattern = chessPattern; 
            
            if(pattern == frameData[833]):
                irData = frameData[pixelNumber]
                if(irData > 32767):
                    irData = irData - 65536
                irData = irData * gain
                
                irData = irData - self.params.offset[pixelNumber]*(1 + self.params.kta[pixelNumber]*(ta - 25))*(1 + self.params.kv[pixelNumber]*(vdd - 3.3))
                if(mode !=  self.params.calibrationModeEE):
                    irData = irData + self.params.ilChessC[2] * (2 * ilPattern - 1) - self.params.ilChessC[1] * conversionPattern
                
                irData = irData - self.params.tgc * irDataCP[subPage]
                
                alphaCompensated = (self.params.alpha[pixelNumber] - self.params.tgc * self.params.cpAlpha[subPage])*(1 + self.params.KsTa * (ta - 25))
                
                image = irData/alphaCompensated
                
                result[pixelNumber] = image

        return result


# void MLX90640_CalculateTo(uint16_t *frameData, const paramsMLX90640 *params, float emissivity, float tr, float *result)
    def MLX90640_CalculateTo(self, frameData, emissivity, tr):
    
        # float vdd;
        # float ta;
        # float ta4;
        # float tr4;
        # float taTr;
        # float gain;
        irDataCP = 2 * [float()]
        # float irData;
        # float alphaCompensated;
        # uint8_t mode;
        # int8_t ilPattern;
        # int8_t chessPattern;
        # int8_t pattern;
        # int8_t conversionPattern;
        # float Sx;
        # float To;
        alphaCorrR = 4 * [float()]
        # int8_t range;
        # uint16_t subPage;
        
        self.params = copy.copy(self.const_params)
        result = 768 * [float()]

        subPage = frameData[833]
        vdd = self.MLX90640_GetVdd(frameData)
        ta = self.MLX90640_GetTa(frameData)
        ta4 = (ta + 273.15)**float(4)
        tr4 = (tr + 273.15)**float(4)
        taTr = tr4 - (tr4-ta4)/emissivity
        
        alphaCorrR[0] = 1 / (1 + self.params.ksTo[0] * 40)
        alphaCorrR[1] = 1
        alphaCorrR[2] = (1 + self.params.ksTo[2] * self.params.ct[2])
        alphaCorrR[3] = alphaCorrR[2] * (1 + self.params.ksTo[3] * (self.params.ct[3] - self.params.ct[2]))
        
    # ------------------------- Gain calculation -----------------------------------    
        gain = frameData[778];
        if(gain > 32767):
            gain = gain - 65536;
        

        gain = self.params.gainEE / gain; 
    
    # ------------------------- To calculation -------------------------------------    
        mode = (frameData[832] & 0x1000) >> 5
        
        irDataCP[0] = frameData[776]
        irDataCP[1] = frameData[808]
        for i in range(2):
            if(irDataCP[i] > 32767):
                irDataCP[i] = irDataCP[i] - 65536
            irDataCP[i] = irDataCP[i] * gain
        irDataCP[0] = irDataCP[0] - self.params.cpOffset[0] * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        if( mode ==  self.params.calibrationModeEE):
            irDataCP[1] = irDataCP[1] - self.params.cpOffset[1] * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        else:
            irDataCP[1] = irDataCP[1] - (self.params.cpOffset[1] + self.params.ilChessC[0]) * (1 + self.params.cpKta * (ta - 25)) * (1 + self.params.cpKv * (vdd - 3.3))
        
        for pixelNumber in range(768):
            ilPattern = pixelNumber / 32 - (pixelNumber / 64) * 2
            chessPattern = ilPattern ^ (pixelNumber - (pixelNumber/2)*2)
            conversionPattern = ((pixelNumber + 2) / 4 - (pixelNumber + 3) / 4 + (pixelNumber + 1) / 4 - pixelNumber / 4) * (1 - 2 * ilPattern)
            
            if(mode == 0):
                pattern = ilPattern
            else:
                pattern = chessPattern
            
            if(pattern == frameData[833]):
                irData = frameData[pixelNumber]
                if(irData > 32767):
                    irData = irData - 65536
                irData = irData * gain
                
                irData = irData - self.params.offset[pixelNumber]*(1 + self.params.kta[pixelNumber]*(ta - 25))*(1 + self.params.kv[pixelNumber]*(vdd - 3.3))
                if(mode !=  self.params.calibrationModeEE):
                    irData = irData + self.params.ilChessC[2] * (2 * ilPattern - 1) - self.params.ilChessC[1] * conversionPattern
                
                irData = irData / emissivity
        
                irData = irData - self.params.tgc * irDataCP[subPage]
                
                alphaCompensated = (self.params.alpha[pixelNumber] - self.params.tgc * self.params.cpAlpha[subPage])*(1 + self.params.KsTa * (ta - 25))
                
                Sx = (alphaCompensated  ** float(3)) * (irData + alphaCompensated * taTr)
                Sx = math.sqrt(math.sqrt(Sx)) * self.params.ksTo[1]
                
                To = math.sqrt(math.sqrt(irData/(alphaCompensated * (1 - self.params.ksTo[1] * 273.15) + Sx) + taTr)) - 273.15
                        
                if(To < self.params.ct[1]):
                    range = 0;
                else:
                    if(To < self.params.ct[2]):
                        range = 1
                    else:
                        if(To < self.params.ct[3]):
                            range = 2
                        else:
                            range = 3
                
                To = math.sqrt(math.sqrt(irData / (alphaCompensated * alphaCorrR[range] * (1 + self.params.ksTo[range] * (To - self.params.ct[range]))) + taTr)) - 273.15
                
                result[pixelNumber] = To

        return result


    # float MLX90640_GetVdd(uint16_t *frameData, const paramsMLX90640 *params)
    def MLX90640_GetVdd(self, frameData):

        vdd = float()
        resolutionCorrection = float()
        resolutionRAM = int()

        self.params = copy.copy(self.const_params)
        
        vdd = frameData[810]
        if(vdd > 32767):
            vdd = vdd - 65536
        resolutionRAM = (frameData[832] & 0x0C00) >> 10
        resolutionCorrection = (2 ** self.params.resolutionEE) / (2 ** resolutionRAM)
        vdd = (resolutionCorrection * vdd - self.params.vdd25) / self.params.kVdd + 3.3
        
        return vdd


    # float MLX90640_GetTa(uint16_t *frameData, const paramsMLX90640 *params)
    def MLX90640_GetTa(self, frameData):
    
        ptat = float()
        ptatArt = float()
        vdd = float()
        ta = float()

        self.params = copy.copy(self.const_params)
        
        vdd = self.MLX90640_GetVdd(frameData);
        
        ptat = frameData[800]
        if(ptat > 32767):
            ptat = ptat - 65536
        
        ptatArt = frameData[768]
        if(ptatArt > 32767):
            ptatArt = ptatArt - 65536
        
        ptatArt = (ptat / (ptat * self.params.alphaPTAT + ptatArt)) * (2 ** float(18))
        
        ta = (ptatArt / (1 + self.params.KvPTAT * (vdd - 3.3)) - self.params.vPTAT25)
        ta = ta / self.params.KtPTAT + 25
        
        return ta
