from python_i2c import *
from bitstring import BitArray
from si5324_controller_reg_setter import *
from si5324_controller_reg_reader import *
import pickle
import math


class Si5324(Si5324_controller_reg_setter, Si5324_controller_reg_reader):
	"""This is the main class of Si5324 controller.

	It handles reading and writing to the device, saving and loading current values to file for later use and settings output frequency.

	It further abstracts some common operations, like setting input clock priority.

	It requires an open I2C port and device (via I2CPort and I2CDevice classes).

	During initialisation default values are written to local register. They can be modified using set_* methods.

	Register numbers are consistent with Si5324 documentation.
	"""

	reg_numbers = list(range(0, 11+1)) + list(range(19, 25+1)) + list(range(31, 36+1)) + list(range(40, 48+1)) + [55] + list(range(128, 132+1)) + list(range(134, 139+1)) + [142, 143]
	reg_defaults = [0b00010100, 0b11100100, 0b01000010, 0b00000101, 0b00010010, 0b11101101, 0b00101101, 0b00101010, 0b00000000, 0b11000000,
					0b00000000, 0b01000000, 0b00101100,
					0b00111110, 0b11111111, 0b11011111, 0b00011111, 0b00111111, 0b00100000,
					0b00000000, 0b00000000, 0b00110001, 0b00000000, 0b00000000, 0b00110001,
					0b11000000, 0b00000000, 0b11111001, 0b00000000, 0b00000000, 0b00001001, 0b00000000, 0b00000000, 0b00001001,
					0b00000000,
					0b00100000, 0b00000110,
					0b00000001, 0b00011111, 0b00000010, 0b00000001, 0b10000010, 0b00000000, 0b00000000, 0b00001111, 0b11111111,
					0b00000000, 0b00000000]
	regs = {}
	input_freq = [None, None]

	def __init__(self, I2CPort, I2CDevice):
		# self.reg_setter = Si5324_controller_reg_setter(self.regs)
		self.port = I2CPort
		self.device = I2CDevice
		self.reset()

	def write_to_reg(self, reg, value):
		"""This method abstracts writing to I2C device."""
		self.device.i2c_write_to_reg(reg, value)

	def read_from_reg(self, reg):
		"""This method abstracts reading from I2C device."""
		r = self.device.i2c_read_from_reg(reg)
		return r

	def reset(self):
		"""Resets local register values to defaults."""
		for i in range(0, len(self.reg_numbers)):
			self.regs[self.reg_numbers[i]] = BitArray(uint=self.reg_defaults[i], length=8)

	def read_current_state_from_device(self):
		"""Reads current register values from the device."""
		for i in range(0, len(self.reg_numbers)):
			self.regs[self.reg_numbers[i]] = self.read_from_reg(self.reg_numbers[i])

	def write_current_state_to_device(self):
		"""Writes locally modified register values to the device."""
		for i in range(0, len(self.reg_numbers)):
			self.write_to_reg(self.reg_numbers[i], self.regs[self.reg_numbers[i]].int)

	def write_current_state_to_file(self, file_path):
		"""Writes locally modified register values to binary file."""
		f = open(file_path, 'wb+')
		# f.write(json.dumps(self.regs, cls=BitArrayEncoder, sort_keys=True, indent=4, ensure_ascii=True))
		f.write(pickle.dumps(self.regs))
		f.close()

	def read_state_from_file(self, file_path):
		"""Reads register map from file and modifies local register values."""
		f = open(file_path, 'rb')
		file_contents = f.read()
		# print(self.regs)
		# self.regs = json.loads(file_contents, cls = BitArrayDecoder)
		self.regs = pickle.loads(file_contents)
		f.close()

	def set_clock_input_priority(self, selected_clock):
		"""Will set manual selection of clock in register. Internal calibration register will also be set.

		:param selected_clock: 0 - clkin1, 1 - clkin2
		"""
		if selected_clock != 0 and selected_clock != 1:
			raise NameError("selected_clock must be 0 or 1")

		self.set_ck_prior1(selected_clock)
		self.set_ck_prior2(not selected_clock)
		self.set_cksel_reg(selected_clock)
		self.set_autosel_reg(0)
		self.set_cksel_pin(0)
		self.set_ical(1)

	def set_clock_input_frequency(self, frequency, clock):
		"""Sets input frequency on selected clock"""
		if 10 <= frequency <= 26:
			rate = 0
		elif 26 < frequency <= 52:
			rate = 1
		elif 52 < frequency <= 100:
			rate = 2
		elif 100 < frequency <= 200:
			rate = 3
		elif 200 < frequency <= 400:
			rate = 4
		elif 400 < frequency <= 710:
			rate = 5
		else:
			raise NameError("f=%d MHz is too high input frequency!" % frequency)
		if clock:
			self.set_clkin2rate(rate)
		else:
			self.set_clkin1rate(rate)
		self.input_freq[clock] = frequency
		self.set_ical(1)

	def set_clock_multiplication(self, output_clock_freq, input_clock, output_clock):
		"""Gets divider values from optimisation function and sets appropriate registers.

		:param output_clock_freq: Desired output frequency.
		:param input_clock: Which clock is the input (0 - CLKIN1, 1 - CLKIN2).
		:param output_clock: Which output clock is set (0 - CLKIN1, 1 - CLKIN2).
		"""
		x = self.clock_dividers_optimisation_brute(self.input_freq[input_clock], output_clock_freq)
		n3 = x[0]
		n2_hs = x[1]
		n2_ls = x[2]
		n1_hs = x[3]
		n1_ls = x[4]

		# f3 = input_clock_freq / n3
		# n2 = n2_hs * n2_ls
		# f_osc = f3 * n2_hs * n2_ls
		# n1 = n1_ls * n1_hs
		# f_out = f_osc / n1_hs / n1_ls

		# print("Target:", output_clock_freq, "MHz")
		# print("n3:", n3, "\nf3:", f3, "MHz\nn2:", n2, "n2_hs:", n2_hs, "n2_ls:", n2_ls, "ls*hs:", n2_ls*n2_hs)
		# print("f_osc:", f_osc, "Mhz")
		# print("n1:", n1, "n1_hs:", n1_hs, "n1_ls:", n1_ls, "ls*hs:", n1_ls*n1_hs)
		# print("f_out:", f_out, "MHz")

		if input_clock:
			self.set_n32(n3-1)
		else:
			self.set_n31(n3-1)
		if output_clock:
			self.set_nc2_ls(n1_ls-1)
		else:
			self.set_nc1_ls(n1_ls-1)
		self.set_n1_hs(n1_hs-4)
		self.set_n2_ls(n2_ls-1)
		self.set_n2_hs(n2_hs-4)
		self.set_ical(1)

	def clock_dividers_optimisation_brute(self, input_clock_freq, output_clock_freq):
		"""
		Finds right divider parameters to achieve output clock frequency while respecting allowed values for registers and intermediate frequencies.

		Exits immediately if an exact match is found.

		:param input_clock_freq: Input clock frequency.
		:param output_clock_freq: Desired output clock frequency.
		:return: Divider values which allow exact or (if the former is \ not found) approximate output frequency generation.
		"""
		exact = []
		inexact = [0, 0, 0, 0, 0, 1e6]

		n3_start = max(math.ceil(input_clock_freq / 2), 1)
		n3_stop = min(math.floor(input_clock_freq / 0.02), 2 ** 19)
		for n3 in range(n3_start, n3_stop + 1):
			f3 = input_clock_freq / n3
			n2_min = math.ceil(4850 / f3)
			n2_max = math.floor(5670 / f3)
			n2_hs_start = 11
			n2_hs_stop = 4
			# print("n3:", n3, n3_start, n3_stop, f3)
			for n2_hs in range(n2_hs_start, n2_hs_stop - 1, -1):
				# print("n2_hs", n2_hs, n2_hs_start, n2_hs_stop)
				n2_ls_start = math.ceil(n2_min / n2_hs) // 2 * 2 + 2
				n2_ls_stop = math.floor(n2_max / n2_hs) // 2 * 2
				for n2_ls in range(n2_ls_start, n2_ls_stop + 1, 2):
					f_osc = f3 * n2_ls * n2_hs
					# print("n2_ls", n2_ls, n2_ls_start, n2_ls_stop, f_osc)
					n1_hs_start = min(11, math.ceil(f_osc / output_clock_freq))
					n1_hs_stop = max(4, math.floor(f_osc / output_clock_freq / 2 ** 20))
					# print("n1_hs:", n1_hs_start, n1_hs_stop)
					# return
					for n1_hs in range(n1_hs_start, n1_hs_stop - 1, -1):
						n1_ls_start = max(1, math.floor(f_osc / output_clock_freq / n1_hs) // 2 * 2)
						n1_ls_stop = min(2 ** 20, math.ceil(f_osc / output_clock_freq / n1_hs // 2 * 2 + 2))
						if n1_ls_start == 1:
							for n1_ls in [1] + list(range(2, n1_ls_stop + 1, 2)):
								f_out = input_clock_freq / n3 * n2_hs * n2_ls / n1_hs / n1_ls
								# print("n1_hs:", n1_hs)
								# print("n1_ls:", n1_ls, n1_ls_start, n1_ls_stop)
								# print("fout:", f_out)
								# return
								if f_out == output_clock_freq:
									exact += [n3, n2_hs, n2_ls, n1_hs, n1_ls]
									# break
									return exact
								elif abs(output_clock_freq - f_out) < inexact[5]:
									inexact = [n3, n2_hs, n2_ls, n1_hs, n1_ls, abs(output_clock_freq - f_out)]
						else:
							for n1_ls in range(n1_ls_start, n1_ls_stop + 1, 2):
								f_out = input_clock_freq / n3 * n2_hs * n2_ls / n1_hs / n1_ls
								# print("n1_hs:", n1_hs)
								# print("n1_ls:", n1_ls, n1_ls_start, n1_ls_stop)
								# print("fout:", f_out)
								# return
								if f_out == output_clock_freq:
									exact += [n3, n2_hs, n2_ls, n1_hs, n1_ls]
									# break
									return exact
								elif abs(output_clock_freq - f_out) < inexact[5]:
									inexact = [n3, n2_hs, n2_ls, n1_hs, n1_ls, abs(output_clock_freq - f_out)]

		print(exact)
		if exact != []:
			return exact[0]
		else:
			return inexact

	def calculate_current_clock_mult(self, input_clock, output_clock):
		"""Calculates current multiplication value."""
		if input_clock:
			divider_in = self.get_n32()
		else:
			divider_in = self.get_n31()
		if output_clock:
			divider_out = self.get_nc2_ls()
		else:
			divider_out = self.get_nc1_ls()

		mult_ls = self.get_n2_ls() + 1
		mult_hs = self.get_n2_hs() + 4
		mult = mult_ls * mult_hs
		divider1 = self.get_n1_hs() + 4
		print(mult_ls, mult_hs, divider_in, divider1, divider_out)
		print(mult)

		return mult / divider_in / divider1 / divider_out


def si5324_init(si):
	file_path = "double_15MHz.reg"

	# si.set_free_run(0)
	# si.set_ckout_always_on(0)
	# si.set_bypass_reg(0)
	# si.set_dhold(0)
	# si.set_bwsel_reg(8)#0xA
	# si.set_sfout2_reg(0x5)
	# si.set_sfout1_reg(0x7)
	# si.set_fosrefsel(0x2)
	# si.set_hlog_2(0)
	# si.set_hlog_1(0)
	# si.set_hist_avg(0x18)
	# si.set_pd_ck2(0)
	si.set_pd_ck1(0)
	# si.set_fos_en(0)
	# si.set_fos_thr(1)
	# si.set_valtime(1)
	# si.set_lockt(1)
	# si.set_ck2_bad_pin(1)
	# si.set_ck1_bad_pin(1)
	# si.set_lol_pin(1)
	# si.set_int_pin(0)
	# si.set_ck1_actv_pin(1)
	# si.set_fosrefsel(2)
	# si.set_fastlock(1)

	si.set_clock_input_priority(1)
	si.set_clock_input_frequency(100, 1)

	# last argument 1 - for kasli 1.0, 0 - for 1.1
	si.set_clock_multiplication(153.3, 1, 0)

	# si.write_current_state_to_file(file_path)
	si.write_current_state_to_device()
	# si.read_state_from_file(file_path)


if __name__ == '__main__':
	mask = 0x13  # in, in,in  Out, In, In, out, out
	gpio = GpioController()
	gpio.open_from_url('ftdi://ftdi:4232h/1', mask)
	port = I2CPort(gpio)
	switch1 = I2CDevice(port, 0x70)
	switch1.i2c_write_byte_to(0xFF)
	switch2 = I2CDevice(port, 0x71)
	# switch2.i2c_write_byte_to(0x08)
	si5324 = I2CDevice(port, 0x69)
	si = Si5324(port, si5324)
	while True:
		si5324_init(si)
	switch2.i2c_write_byte_to(0x00)

	rj45 = I2CDevice(port, 0x3E)
	switch1.i2c_write_byte_to(0x80)  # EEM0
	rj45.i2c_write_byte_to(0xFF)
	switch1.i2c_write_byte_to(0x20)  # EEM1
	rj45.i2c_write_byte_to(0x00)
	switch1.i2c_write_byte_to(0x10)  # EEM2
	rj45.i2c_write_byte_to(0xFF)
	switch1.i2c_write_byte_to(0x08)  # EEM3
	rj45.i2c_write_byte_to(0x00)
