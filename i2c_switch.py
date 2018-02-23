from python_i2c import *


class i2c_switch():
	def __init__(self, I2CPort):
		# self.reg_setter = Si5324_controller_reg_setter(self.regs)
		self.port = I2CPort
		self.switch1 = I2CDevice(self.port, 0x70)
		self.switch2 = I2CDevice(self.port, 0x71)
		self.reset()

	def reset(self):
		self.switch1.i2c_write_byte_to(0x00)
		self.switch2.i2c_write_byte_to(0x00)

	def enable_eem(self, num):
		switcher1 = {
			0: 0x80,
			1: 0x20,
			2: 0x10,
			3: 0x08,
			4: 0x04,
			5: 0x02,
			6: 0x01,
			7: 0x40,
		}
		switcher2 = {
			8: 0x10,
			9: 0x20,
			10: 0x80,
			11: 0x40,
		}
		if num >= 8:
			self.switch2.i2c_write_byte_to(switcher2.get(num, 0x00))
			self.switch1.i2c_write_byte_to(0x00)
		else:
			self.switch1.i2c_write_byte_to(switcher1.get(num, 0x00))
			self.switch2.i2c_write_byte_to(0x00)

	def enable_si5324(self):
		self.switch1.i2c_write_byte_to(0x00)
		self.switch2.i2c_write_byte_to(0x08)