#!/usr/bin/python

from smbus2 import SMBus, i2c_msg, SMBusWrapper

i2c_addr = 0x33

# Single transaction writing two bytes then read two at address 80
# write = i2c_msg.write(i2c_addr, [0x80, 0x0D])
# read = i2c_msg.read(i2c_addr, 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)

# write = i2c_msg.write(i2c_addr, [0x80, 0x0F])
# read = i2c_msg.read(i2c_addr, 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)

for i in range(0, 32*2, 2):
    write = i2c_msg.write(i2c_addr, [0x04, i])
    read = i2c_msg.read(i2c_addr, 2)
    with SMBusWrapper(1) as bus:
        bus.i2c_rdwr(write, read)

    l = list(read)
    # print(l)

    x = (((l[0] << 8) & 0xFF00) | ((l[1] & 0x00FF)))
    print(x)
