from si5324_controller_v1_0 import *
from i2c_switch import *

mask = 0x13  # in, in,in  Out, In, In, out, out
gpio = GpioController()
gpio.open_from_url('ftdi://ftdi:4232h/1', mask)
port = I2CPort(gpio)
switch = i2c_switch(port)
switch.enable_si5324()
si5324 = I2CDevice(port, 0x68)
si = Si5324(port, si5324)
# si5324_init(si)

if True:
	rj45 = I2CDevice(port, 0x3E)
	switch.enable_eem(0)
	rj45.i2c_write_byte_to(0xFF)  # high - output

	switch.enable_eem(1)
	rj45.i2c_write_byte_to(0x00)

	switch.enable_eem(2)
	rj45.i2c_write_byte_to(0xFF)

	switch.enable_eem(3)
	rj45.i2c_write_byte_to(0x00)