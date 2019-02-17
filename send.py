#!/usr/bin/python

from smbus2 import SMBus, i2c_msg, SMBusWrapper

i2c_addr = 0x33

raw_image_stream = []

num_of_pixels = 10

BIT_POS = 12

def calc(l):
    x = (((l[0] << 8) & 0xFF00) | ((l[1] & 0x00FF)))
    return x

# Single transaction writing two bytes then read two at address 80
# write = i2c_msg.write(i2c_addr, [0x80, 0x0D])
# read = i2c_msg.read(i2c_addr, 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)

# ### read - write - chess - TV interleaved
reg_list = []
write = i2c_msg.write(i2c_addr, [0x80, 0x0D])
read = i2c_msg.read(i2c_addr, 2)
with SMBusWrapper(1) as bus:
    bus.i2c_rdwr(write, read)
    reg_list = list(read)

print(hex(reg_list[0]), hex(reg_list[1]))

reg = ((reg_list[0] << 8) & 0xFF00) | (reg_list[1] & 0x00FF)
reg = reg ^ (0x0001 << BIT_POS)
reg_list[0] = (reg >> 8) & 0xFF
reg_list[1] = reg & 0xFF

print(hex(reg_list[0]), hex(reg_list[1]))

write = i2c_msg.write(i2c_addr, [0x80, 0x0D, reg_list[0], reg_list[1]])
# write = i2c_msg.write(i2c_addr, [0x80, 0x0D, 0x09, 0x01])
read = i2c_msg.read(i2c_addr, 2)
with SMBusWrapper(1) as bus:
    bus.i2c_rdwr(write)

write = i2c_msg.write(i2c_addr, [0x80, 0x0D])
read = i2c_msg.read(i2c_addr, 2)
with SMBusWrapper(1) as bus:
    bus.i2c_rdwr(write, read)
    reg_list = list(read)

print(hex(reg_list[0]), hex(reg_list[1]))


# write = i2c_msg.write(i2c_addr, [0x04, 00])
# read = i2c_msg.read(i2c_addr, num_of_pixels * 2)
# with SMBusWrapper(1) as bus:
#     bus.i2c_rdwr(write, read)
#     l = list(read)
#     print(l)

#     for i in range(num_of_pixels):
#         x = (((l[i * 2] << 8) & 0xFF00) | ((l[i * 2 + 1] & 0x00FF)))
#         raw_image_stream.append(x)

# print("max: {:d}   min: {:d}".format(max(raw_image_stream), min(raw_image_stream)))
# print(raw_image_stream)
