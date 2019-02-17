#!/usr/bin/python

from smbus2 import SMBus, i2c_msg, SMBusWrapper

i2c_addr = 0x33

raw_image_stream = []

# Single transaction writing two bytes then read two at address 80
# write = i2c_msg.write(i2c_addr, [0x80, 0x0D])
# read = i2c_msg.read(i2c_addr, 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)

# write = i2c_msg.write(i2c_addr, [0x80, 0x0F])
# read = i2c_msg.read(i2c_addr, 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)

for i in range(0, 0xFF):
    write = i2c_msg.write(i2c_addr, [0x04, i])
    read = i2c_msg.read(i2c_addr, 2)
    with SMBusWrapper(1) as bus:
        bus.i2c_rdwr(write, read)

    l = list(read)
    # print(l)

    x = (((l[0] << 8) & 0xFF00) | ((l[1] & 0x00FF)))
    raw_image_stream.append(x)

#print(x)
print("max: {:d}   min: {:d}".format(max(raw_image_stream), min(raw_image_stream)))
