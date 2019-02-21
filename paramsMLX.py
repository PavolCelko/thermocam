
class params:
    def __init__(self, eeData):
        if self.CheckEEPROMValid(eeData) != 0:
            return None

        # int16_t kVdd
        self.kVdd = int()
        # int16_t vdd25
        self.vdd25 = int()
        # float KvPTAT
        self.KvPTAT = float()
        # float KtPTAT
        self.KtPTAT = float()
        # uint16_t vPTAT25
        self.vPTAT25 = int()
        # float alphaPTAT
        self.alphaPTAT = float()
        # int16_t gainEE
        self.gainEE = int()
        # float tgc
        self.tgc = float()
        # float cpKv
        self.cpKv = float()
        # float cpKta
        self.cpKta = float()
        # uint8_t resolutionEE
        self.resolutionEE = int()
        # uint8_t calibrationModeEE
        self.calibrationModeEE = int()
        # float KsTa
        self.KsTa = float()
        # float ksTo[4]
        self.ksTo = 4*[float()]
        # int16_t ct[4]
        self.ct = 4*[int()]
        # float alpha[768]
        self.alpha = 768*[float()]
        # int16_t offset[768]    
        self.offset = 768*[int()]
        # float kta[768]    
        self.kta = 768*[float()]
        # float kv[768]
        self.kv = 768*[float()]
        # float cpAlpha[2]
        self.cpAlpha = 2*[float()]
        # int16_t cpOffset[2]
        self.cpOffset = 2*[int()]
        # float ilChessC[3] 
        self.ilChessC = 3*[float()]
        # uint16_t brokenPixels[5]
        self.brokenPixels = 5*[int()]
        # uint16_t outlierPixels[5]
        self.outlierPixels = 5*[int()]
        
        self.ExtractVDDParameters(eeData)
        self.ExtractPTATParameters(eeData)
        self.ExtractGainParameters(eeData)
        self.ExtractTgcParameters(eeData)
        self.ExtractResolutionParameters(eeData)
        self.ExtractKsTaParameters(eeData)
        self.ExtractKsToParameters(eeData)
        self.ExtractAlphaParameters(eeData)
        self.ExtractOffsetParameters(eeData)
        self.ExtractKtaPixelParameters(eeData)
        self.ExtractKvPixelParameters(eeData)
        self.ExtractCPParameters(eeData)
        self.ExtractCILCParameters(eeData)
        self.ExtractDeviatingPixels(eeData)

    
    def ExtractVDDParameters(self, eeData):
        kVdd = eeData[51]
        kVdd = (eeData[51] & 0xFF00) >> 8
        if(kVdd > 127):
            kVdd = kVdd - 256
        kVdd = 32 * kVdd
        vdd25 = eeData[51] & 0x00FF
        vdd25 = ((vdd25 - 256) << 5) - 8192
        
        self.kVdd = kVdd
        self.vdd25 = vdd25


    def ExtractPTATParameters(self, eeData):

        KvPTAT = (eeData[50] & 0xFC00) >> 10
        if(KvPTAT > 31):
            KvPTAT = KvPTAT - 64
        
        KvPTAT = KvPTAT/4096
        
        KtPTAT = eeData[50] & 0x03FF
        if(KtPTAT > 511):
            KtPTAT = KtPTAT - 1024
        KtPTAT = KtPTAT/8
        
        vPTAT25 = eeData[49]
        
        alphaPTAT = (eeData[16] & 0xF000) / (2 ** 14) + 8.0
        
        self.KvPTAT = KvPTAT
        self.KtPTAT = KtPTAT
        self.vPTAT25 = vPTAT25
        self.alphaPTAT = alphaPTAT


    def ExtractGainParameters(self, eeData):

        gainEE = eeData[48]
        if(gainEE > 32767):
            gainEE = gainEE -65536
        self.gainEE = gainEE


    def ExtractTgcParameters(self, eeData):
        tgc = eeData[60] & 0x00FF
        if(tgc > 127):
            tgc = tgc - 256
        tgc = tgc / 32.0
        
        self.tgc = tgc


    def ExtractResolutionParameters(self, eeData):

        self.resolutionEE = (eeData[56] & 0x3000) >> 12
            

    def ExtractKsTaParameters(self, eeData):

        KsTa = (eeData[60] & 0xFF00) >> 8
        if(KsTa > 127):
            KsTa = KsTa -256
        KsTa = KsTa / 8192.0
        
        self.KsTa = KsTa


    def ExtractKsToParameters(self, eeData):

        step = ((eeData[63] & 0x3000) >> 12) * 10
        
        self.ct[0] = -40
        self.ct[1] = 0
        self.ct[2] = (eeData[63] & 0x00F0) >> 4
        self.ct[3] = (eeData[63] & 0x0F00) >> 8
        
        self.ct[2] = self.ct[2]*step
        self.ct[3] = self.ct[2] + self.ct[3]*step
        
        KsToScale = (eeData[63] & 0x000F) + 8
        KsToScale = 1 << KsToScale
        
        self.ksTo[0] = float(eeData[61] & 0x00FF)
        self.ksTo[1] = float((eeData[61] & 0xFF00) >> 8)
        self.ksTo[2] = float(eeData[62] & 0x00FF)
        self.ksTo[3] = float((eeData[62] & 0xFF00) >> 8)
        
        
        for i in range(4):
            if(self.ksTo[i] > 127):
                self.ksTo[i] = self.ksTo[i] -256
            self.ksTo[i] = self.ksTo[i] / KsToScale
        

    def ExtractAlphaParameters(self, eeData):

        # int accRow[24]
        accRow = 24 * [int()]
        # int accColumn[32]
        accColumn = 32 * [int()]
        
        accRemScale = eeData[32] & 0x000F
        accColumnScale = (eeData[32] & 0x00F0) >> 4
        accRowScale = (eeData[32] & 0x0F00) >> 8
        alphaScale = ((eeData[32] & 0xF000) >> 12) + 30
        alphaRef = eeData[33]
        
        for i in range(6):
            p = i * 4
            accRow[p + 0] = (eeData[34 + i] & 0x000F)
            accRow[p + 1] = (eeData[34 + i] & 0x00F0) >> 4
            accRow[p + 2] = (eeData[34 + i] & 0x0F00) >> 8
            accRow[p + 3] = (eeData[34 + i] & 0xF000) >> 12
        
        for i in range(24):
            if (accRow[i] > 7):
                accRow[i] = accRow[i] - 16
            
        for i in range(8):
            p = i * 4
            accColumn[p + 0] = (eeData[40 + i] & 0x000F)
            accColumn[p + 1] = (eeData[40 + i] & 0x00F0) >> 4
            accColumn[p + 2] = (eeData[40 + i] & 0x0F00) >> 8
            accColumn[p + 3] = (eeData[40 + i] & 0xF000) >> 12
        
        for i in range(32):
            if (accColumn[i] > 7):
                accColumn[i] = accColumn[i] - 16
            
        for i in range(24):
            for j in range(32):
                p = 32 * i +j
                self.alpha[p] = float((eeData[64 + p] & 0x03F0) >> 4)
                if (self.alpha[p] > 31):
                    self.alpha[p] = self.alpha[p] - 64
                self.alpha[p] = self.alpha[p]*(1 << accRemScale)
                self.alpha[p] = (alphaRef + (accRow[i] << accRowScale) + (accColumn[j] << accColumnScale) + self.alpha[p])
                self.alpha[p] = self.alpha[p] / (2 ** alphaScale)
            

    def ExtractOffsetParameters(self, eeData):

        # int occRow[24]
        occRow = 24*[int()]
        # int occColumn[32]
        occColumn = 32*[int()]
        # int p = 0
        # int16_t offsetRef
        # uint8_t occRowScale
        # uint8_t occColumnScale
        # uint8_t occRemScale
        

        occRemScale = (eeData[16] & 0x000F)
        occColumnScale = (eeData[16] & 0x00F0) >> 4
        occRowScale = (eeData[16] & 0x0F00) >> 8
        offsetRef = eeData[17]
        if (offsetRef > 32767):
            offsetRef = offsetRef - 65536
        
        for i in range(6):
            p = i * 4
            occRow[p + 0] = (eeData[18 + i] & 0x000F)
            occRow[p + 1] = (eeData[18 + i] & 0x00F0) >> 4
            occRow[p + 2] = (eeData[18 + i] & 0x0F00) >> 8
            occRow[p + 3] = (eeData[18 + i] & 0xF000) >> 12
        
        for i in range(24):
            if (occRow[i] > 7):
                occRow[i] = occRow[i] - 16
            
        for i in range(8):
            p = i * 4
            occColumn[p + 0] = (eeData[24 + i] & 0x000F)
            occColumn[p + 1] = (eeData[24 + i] & 0x00F0) >> 4
            occColumn[p + 2] = (eeData[24 + i] & 0x0F00) >> 8
            occColumn[p + 3] = (eeData[24 + i] & 0xF000) >> 12
        
        for i in range(32):
            if (occColumn[i] > 7):
                occColumn[i] = occColumn[i] - 16
            
        for i in range(24):
            for j in range(32):
                p = 32 * i +j
                self.offset[p] = (eeData[64 + p] & 0xFC00) >> 10
                if(self.offset[p] > 31):
                    self.offset[p] = self.offset[p] - 64
                self.offset[p] = self.offset[p]*(1 << occRemScale)
                self.offset[p] = (offsetRef + (occRow[i] << occRowScale) + (occColumn[j] << occColumnScale) + self.offset[p])
            

    def ExtractKtaPixelParameters(self, eeData):

        # int p = 0
        p = 0
        # int8_t KtaRC[4]
        KtaRC = 4*[int()]
        # int8_t KtaRoCo
        # int8_t KtaRoCe
        # int8_t KtaReCo
        # int8_t KtaReCe
        # uint8_t ktaScale1
        # uint8_t ktaScale2
        # uint8_t split

        KtaRoCo = (eeData[54] & 0xFF00) >> 8
        if (KtaRoCo > 127):
            KtaRoCo = KtaRoCo - 256
        KtaRC[0] = KtaRoCo
        
        KtaReCo = (eeData[54] & 0x00FF)
        if (KtaReCo > 127):
            KtaReCo = KtaReCo - 256
        KtaRC[2] = KtaReCo
        
        KtaRoCe = (eeData[55] & 0xFF00) >> 8
        if (KtaRoCe > 127):
            KtaRoCe = KtaRoCe - 256
        KtaRC[1] = KtaRoCe
        
        KtaReCe = (eeData[55] & 0x00FF)
        if (KtaReCe > 127):
            KtaReCe = KtaReCe - 256
        KtaRC[3] = KtaReCe
    
        ktaScale1 = ((eeData[56] & 0x00F0) >> 4) + 8
        ktaScale2 = (eeData[56] & 0x000F)

        for i in range(24):
            for j in range(32):
                p = 32 * i +j
                split = 2*(p/32 - (p/64)*2) + p%2
                self.kta[p] = (eeData[64 + p] & 0x000E) >> 1
                if (self.kta[p] > 3):
                    self.kta[p] = self.kta[p] - 8
                self.kta[p] = self.kta[p] * (1 << ktaScale2)
                self.kta[p] = KtaRC[split] + self.kta[p]
                self.kta[p] = self.kta[p] / (2 ** ktaScale1)
            

    def ExtractKvPixelParameters(self, eeData):

        # int p = 0
        p = 0
        # int8_t KvT[4]
        KvT = 4 * [int()]
        
        KvRoCo = (eeData[52] & 0xF000) >> 12
        if (KvRoCo > 7):
            KvRoCo = KvRoCo - 16
        KvT[0] = KvRoCo
        
        KvReCo = (eeData[52] & 0x0F00) >> 8
        if (KvReCo > 7):
            KvReCo = KvReCo - 16
        KvT[2] = KvReCo
        
        KvRoCe = (eeData[52] & 0x00F0) >> 4
        if (KvRoCe > 7):
            KvRoCe = KvRoCe - 16
        KvT[1] = KvRoCe
        
        KvReCe = (eeData[52] & 0x000F)
        if (KvReCe > 7):
            KvReCe = KvReCe - 16
        KvT[3] = KvReCe
    
        kvScale = (eeData[56] & 0x0F00) >> 8


        for i in range(24):
            for j in range(32):
                p = 32 * i +j
                split = 2*(p/32 - (p/64)*2) + p%2
                self.kv[p] = KvT[split]
                self.kv[p] = self.kv[p] / (2 ** kvScale)
        

    def ExtractCPParameters(self, eeData):

        # float alphaSP[2]
        alphaSP = 2 * [float()]
        # int16_t offsetSP[2]
        offsetSP = 2 * [int()]
        # float cpKv
        # float cpKta
        cpKv = float()
        cpKta = float()
        # uint8_t alphaScale
        # uint8_t ktaScale1
        # uint8_t kvScale

        alphaScale = ((eeData[32] & 0xF000) >> 12) + 27
        
        offsetSP[0] = (eeData[58] & 0x03FF)
        if (offsetSP[0] > 511):
            offsetSP[0] = offsetSP[0] - 1024
        
        offsetSP[1] = (eeData[58] & 0xFC00) >> 10
        if (offsetSP[1] > 31):
            offsetSP[1] = offsetSP[1] - 64
        offsetSP[1] = offsetSP[1] + offsetSP[0] 
        
        alphaSP[0] = float((eeData[57] & 0x03FF))
        if (alphaSP[0] > 511):
            alphaSP[0] = alphaSP[0] - 1024
        alphaSP[0] = alphaSP[0] /  (2 ** alphaScale)
        
        alphaSP[1] = float((eeData[57] & 0xFC00) >> 10)
        if (alphaSP[1] > 31):
            alphaSP[1] = alphaSP[1] - 64
        alphaSP[1] = (1 + alphaSP[1]/128) * alphaSP[0]
        
        cpKta = float((eeData[59] & 0x00FF))
        if (cpKta > 127):
            cpKta = cpKta - 256
        ktaScale1 = ((eeData[56] & 0x00F0) >> 4) + 8
        self.cpKta = cpKta / (2 ** ktaScale1)
        
        cpKv = float((eeData[59] & 0xFF00) >> 8)
        if (cpKv > 127):
            cpKv = cpKv - 256
        kvScale = (eeData[56] & 0x0F00) >> 8
        self.cpKv = cpKv / (2 ** kvScale)
        
        self.cpAlpha[0] = alphaSP[0]
        self.cpAlpha[1] = alphaSP[1]
        self.cpOffset[0] = offsetSP[0]
        self.cpOffset[1] = offsetSP[1]  


    def ExtractCILCParameters(self, eeData):

        # float ilChessC[3]
        ilChessC = 3 * [float()]
        
        calibrationModeEE = (eeData[10] & 0x0800) >> 4
        calibrationModeEE = calibrationModeEE ^ 0x80

        ilChessC[0] = (eeData[53] & 0x003F)
        if (ilChessC[0] > 31):
            ilChessC[0] = ilChessC[0] - 64
        ilChessC[0] = ilChessC[0] / 16.0
        
        ilChessC[1] = (eeData[53] & 0x07C0) >> 6
        if (ilChessC[1] > 15):
            ilChessC[1] = ilChessC[1] - 32
        ilChessC[1] = ilChessC[1] / 2.0
        
        ilChessC[2] = (eeData[53] & 0xF800) >> 11
        if (ilChessC[2] > 15):
            ilChessC[2] = ilChessC[2] - 32
        ilChessC[2] = ilChessC[2] / 8.0
        
        self.calibrationModeEE = calibrationModeEE
        self.ilChessC[0] = ilChessC[0]
        self.ilChessC[1] = ilChessC[1]
        self.ilChessC[2] = ilChessC[2]

    # int CheckAdjacentPixels(uint16_t pix1, uint16_t pix2)
    def CheckAdjacentPixels(pix1, pix2):

        pixPosDif = pix1 - pix2
        if(pixPosDif > -34 and pixPosDif < -30):
            return -6
        if(pixPosDif > -2 and pixPosDif < 2):
            return -6
        if(pixPosDif > 30 and pixPosDif < 34):
            return -6
        
        return 0

    # int ExtractDeviatingPixels(eeData)
    def ExtractDeviatingPixels(self, eeData):

        pixCnt = int(0)
        brokenPixCnt = int(0)
        outlierPixCnt = int(0)
        warn = 0
        
        for pixCnt in range(5):
            self.brokenPixels[pixCnt] = 0xFFFF
            self.outlierPixels[pixCnt] = 0xFFFF
            
        pixCnt = 0    
        while (pixCnt < 768 and brokenPixCnt < 5 and outlierPixCnt < 5):
            if(eeData[pixCnt+64] == 0):
                self.brokenPixels[brokenPixCnt] = pixCnt
                brokenPixCnt = brokenPixCnt + 1
            else:
                if((eeData[pixCnt+64] & 0x0001) != 0):
                    self.outlierPixels[outlierPixCnt] = pixCnt
                    outlierPixCnt = outlierPixCnt + 1
            
            pixCnt = pixCnt + 1
        
        if(brokenPixCnt > 4):
            warn = -3
        else: 
            if(outlierPixCnt > 4):
                warn = -4
            else:
                if((brokenPixCnt + outlierPixCnt) > 4): 
                    warn = -5
                else:
                    for pixCnt in range(brokenPixCnt):
                        for i in range(pixCnt+1, brokenPixCnt):
                            warn = self.CheckAdjacentPixels(self.brokenPixels[pixCnt], self.brokenPixels[i])
                            if(warn != 0):
                                return warn
                        
                    for pixCnt in range(outlierPixCnt):
                        for i in range(pixCnt+1, outlierPixCnt):
                            warn = self.CheckAdjacentPixels(self.outlierPixels[pixCnt],self.outlierPixels[i])
                            if(warn != 0):
                                return warn
                            
                    for pixCnt in range(brokenPixCnt):
                        for i in range(outlierPixCnt):
                            warn = self.CheckAdjacentPixels(self.brokenPixels[pixCnt],self.outlierPixels[i])
                            if(warn != 0):
                                return warn
                            
        
        return warn

    
    def CheckEEPROMValid(self, eeData):

        deviceSelect = eeData[10] & 0x0040
        if(deviceSelect == 0):
            return 0
        
        return -7