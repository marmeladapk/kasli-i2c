# import pyftdi
from pyftdi.gpio import GpioController, GpioException


class I2CPort:
	"""Class that opens an I2C port in a bit-bang way and inits the bus."""
	mask = 0x13  # in, in,in  Out, In, In, out, out

	def __init__(self, gpio, inmask=mask):
		self.gpio = gpio
		self.gpio.set_direction(0xFF, inmask)
		self.mask = inmask
		self.i2c_init()

	def i2c_init(self):
		"""Initialises the bus."""
		self.gpio.write_port(0xff & self.mask)


class I2CDevice:
	"""A class for handling a single device on a I2C bus.

	Uses bitbang GPIO, which results in unreliable timings (also is horribly slow), but was tested without any problems on the Kasli board.
	"""
	def __init__(self, port, address):
		"""Initialises a member of the class.

		:param port: I2C port from I2CPort class.
		:param address: Address of the device on the I2C bus (without R/W bit).
		"""
		self.address = address
		self.port = port
		self.gpio = self.port.gpio
		self.mask = self.port.mask

	def i2c_start(self):
		"""Sets condition of I2C transaction."""
		self.gpio.write_port(0x11 & self.mask)
		self.gpio.write_port(0x10 & self.mask)

	def i2c_ack(self):
		"""Acknowledges transaction."""
		self.gpio.write_port(0x10 & self.mask)
		self.gpio.write_port(0x11 & self.mask)

	def i2c_read_ack(self):
		"""Checks if transaction is acknowledged.

		:return: True if ACK, False if NACK
		"""
		self.gpio.set_direction(0xFF, 0x11)
		self.gpio.write_port(0x10 & self.mask)
		self.gpio.write_port(0x11 & self.mask)
		pins = self.gpio.read_port()
		# print(pins)
		self.gpio.set_direction(0xFF, self.mask)
		if not (pins & 0x02):
			return True
		else:
			return False

	def i2c_write_bit(self, bit):
		"""Writes a single bit on the bus."""
		self.gpio.write_port((0x10 + (bit << 1) & self.mask))
		self.gpio.write_port((0x11 + (bit << 1) & self.mask))
		self.gpio.write_port((0x10 + (bit << 1) & self.mask))

	def i2c_read_bit(self):
		"""Reads a single bit from the bus.

		:return: Bit that was read from the bus.
		"""
		self.gpio.write_port(0x10)
		self.gpio.write_port(0x11)
		pins = self.gpio.read_port()
		self.gpio.write_port(0x10)
		return (pins & 0x02) >> 1

	def i2c_end(self):
		"""Sets an end condition on bus."""
		self.gpio.write_port(0x10 & self.mask)
		self.gpio.write_port(0x11 & self.mask)
		self.gpio.write_port(0x13 & self.mask)

	def i2c_write_address(self, write, address):
		"""Writes address with R/W bit at the end.

		:param write: R/W bit
		:param address: Address to write to bus.
		:return: True if ACK, False if NACK.
		"""
		self.i2c_start()
		for i in range(0, 7):
			self.i2c_write_bit((address >> (6-i)) & 1)
			# print((address >> (6-i)) & 1)
		self.i2c_write_bit(write)
		v = self.i2c_read_ack()
		return v

	def i2c_write_byte(self, byte):
		"""Writes a single byte to the bus.

		:return: True if ACK, False if NACK.
		"""
		# i2c_start(self.gpio)
		for i in range(0, 8):
			self.i2c_write_bit((byte >> (7-i)) & 1)
			# print((byte >> (7-i)) & 1)
		v = self.i2c_read_ack()
		return v

	def i2c_read_byte(self):
		"""Reads a single byte from the bus.

		:return: Byte that was read.
		"""

		self.gpio.set_direction(0xFF, 0x11)
		byte = 0x00
		for i in range(0, 8):
			bit = self.i2c_read_bit()
			# print(bit)
			byte += bit << (7-i)
		self.gpio.set_direction(0xFF, self.mask)
		self.i2c_ack()
		self.i2c_end()
		# print(byte)
		return byte

	def i2c_read_byte_from(self):
		"""Read a single byte from this device (includes writing an address with R bit).

		:return: Byte that was read.
		"""
		v = self.i2c_write_address(1, self.address)
		byte = self.i2c_read_byte()
		if not v:
			print("Error")
		return byte

	def i2c_write_byte_to(self, byte):
		"""Writes a single byte to this device (includes writing an address with W bit).

		:return: True if ACK, False if NACK.
		"""
		v = self.i2c_write_address(0, self.address)
		v &= self.i2c_write_byte(byte)
		self.i2c_end()
		return v

	def i2c_write_to_reg(self, reg, byte):
		"""Writes a single byte to specified register.

		:param reg: Register number to which the byte will be written.
		:param byte: Byte to be written.
		:return: True if ACK, False if NACK on any of transactions.
		"""
		v = self.i2c_write_address(0, self.address)
		v &= self.i2c_write_byte(reg)
		v &= self.i2c_write_byte(byte)
		if not v:
			print("Error writing to %d register" % reg)
		self.i2c_end()
		return v

	def i2c_read_from_reg(self, reg):
		"""Reads a single byte from specified register.

		:param reg: Register to be read.
		:return: Byte that was read.
		"""
		v = self.i2c_write_address(0, self.address)
		v &= self.i2c_write_byte(reg)
		self.i2c_end()
		v &= self.i2c_write_address(1, self.address)
		byte = self.i2c_read_byte()
		if not v:
			print("Error")
		self.i2c_end()
		return byte


if __name__ == '__main__':
	mask = 0x13  # in, in,in  Out, In, In, out, out
	gpio = GpioController()
	gpio.open_from_url('ftdi://ftdi:4232h/1', mask)
	port = I2CPort(gpio)
	switch2 = I2CDevice(port, 0x71)
	switch2.i2c_write_byte_to(0x04)
	i = switch2.i2c_read_byte_from()
	print("%x" % i)
	gpio.close()
