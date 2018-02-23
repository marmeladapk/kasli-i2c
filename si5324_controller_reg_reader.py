from bitstring import BitArray


class Si5324_controller_reg_reader:
	"""A class that handles getting meaningful values from registers.

	Currently only getting divider values is supported.
	"""

	def __init__(self, regs):
		self.regs = regs


	# def set_free_run(self, value):
	# 	"""Internal to the device, route XA/XB to CKIN2. This allows the device to lock to its XA-XB reference.
	# 	0: Disable
	# 	1: Enable
	# 	"""
	# 	self.regs[0][-7] = value
	#
	# def set_ckout_always_on(self, value):
	# 	"""This will bypass the SQ_ICAL function. Output will be available even if SQ_ICAL is on and ICAL is not complete or successful.
	# 	0: Squelch output until part is calibrated (ICAL).
	# 	1: Provide an output.
	# 	Notes:
	# 	1. The frequency may be significantly off until the part is calibrated.
	# 	2. Must be 1 to control output to output skew.
	# 	"""
	# 	self.regs[0][-6] = value
	#
	# def set_bypass_reg(self, value):
	# 	"""This bit enables or disables the PLL bypass mode. Use only when the device is in digital hold or before the first ICAL. Bypass mode is not supported for CMOS output clocks.
	# 	0: Normal operation
	# 	1: Bypass mode. Selected input clock is connected to CKOUT buffers, bypassing PLL.
	# 	"""
	# 	self.regs[0][-2] = value
	#
	# def set_ck_prior2(self, value):
	# 	"""Selects which of the input clocks will be 2nd priority in the autoselection state machine.
	# 	0: CKIN1 is 2nd priority.
	# 	1: CKIN2 is 2nd priority.
	# 	"""
	# 	self.regs[1][-3] = value
	#
	# def set_ck_prior1(self, value):
	# 	"""Selects which of the input clocks will be 1st priority in the autoselection state machine.
	# 	00: CKIN1 is 1st priority.
	# 	01: CKIN2 is 1st priority.
	# 	"""
	# 	self.regs[1][-1] = value
	#
	# def set_bwsel_reg(self, value):
	# 	"""Selects nominal f3dB bandwidth for PLL. See the DSPLLsim for settings. After BWSEL_REG is written with a new value, an ICAL is required for the change to take effect."""
	# 	self.regs[2][-8:-4] = value
	#
	# def set_cksel_reg(self, value):
	# 	"""If the device is operating in register-based manual clock selection mode (AUTOSEL_REG = 00), and CKSEL_PIN = 0, then these bits select which input clock will be the active input clock. If CKSEL_PIN = 1 and AUTOSEL_REG = 00, the CS_CA input pin continues to control clock selection and CKSEL_REG is of no consequence .
	# 	0: CKIN_1 selected.
	# 	1: CKIN_2 selected.
	# 	"""
	# 	self.regs[3][-7] = value
	#
	# def set_dhold(self, value):
	# 	"""Forces the part into digital hold. This bit overrides all other manual and automatic clock selection controls.
	# 	0: Normal operation.
	# 	1: Force digital hold mode. Overrides all other settings and ignores the quality of all of the input clocks.
	# 	"""
	# 	self.regs[3][-6] = value
	#
	# def set_sq_ical(self, value):
	# 	"""This bit determines if the output clocks will remain enabled or be squelched (disabled) during an internal calibration.
	# 	0: Output clocks enabled during ICAL.
	# 	1: Output clocks disabled during ICAL.
	# 	"""
	# 	self.regs[3][-5] = value
	#
	# def set_autosel_reg(self, value):
	# 	"""Selects method of input clock selection to be used.
	# 	00: Manual (either register or pin controlled, see CKSEL_PIN)
	# 	01: Automatic Non-Revertive
	# 	10: Automatic Revertive
	# 	11: Reserved
	# 	"""
	# 	if value == 3:
	# 		raise NameError("Value 11 is reserved")
	# 	self.regs[4][-8:-6] = value
	#
	# def set_hist_del(self, value):
	# 	"""Selects amount of delay to be used in generating the history information used for Digital Hold.
	# 	"""
	# 	self.regs[4][3:8] = value
	#
	# def set_icmos(self, value):
	# 	"""When the output buffer is set to CMOS mode, these bits determine the output buffer drive strength. The first number below refers to 3.3 V operation; the second to 1.8 V operation. These values assume CKOUT+ is tied to CKOUT-.
	# 	00: 8mA/2mA.
	# 	01: 16mA/4mA
	# 	10: 24mA/6mA
	# 	11: 32mA/8mA
	# 	"""
	# 	self.regs[5][0:2] = value
	#
	# def set_sfout2_reg(self, value):
	# 	"""Controls output signal format and disable for CKOUT2 output buffer. Bypass mode is not supported for CMOS output clocks.
	# 	000: Reserved
	# 	001: Disable
	# 	010: CMOS
	# 	011: Low swing LVDS
	# 	100: Reserved
	# 	101: LVPECL
	# 	110: CML
	# 	111: LVDS
	# 	"""
	# 	if value == 0b000 or value == 0b100:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[6][-6:-3] = value
	#
	# def set_sfout1_reg(self, value):
	# 	"""Controls output signal format and disable for CKOUT1 output buffer. Bypass mode is not supported for CMOS output clocks.
	# 	000: Reserved
	# 	001: Disable
	# 	010: CMOS
	# 	011: Low swing LVDS
	# 	100: Reserved
	# 	101: LVPECL
	# 	110: CML
	# 	111: LVDS
	# 	"""
	# 	if value == 0b000 or value == 0b100:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[6][5:8] = value
	#
	# def set_fosrefsel(self, value):
	# 	"""Selects which input clock is used as the reference frequency for Frequency Off-Set (FOS) alarms.
	# 	00: XA/XB (External reference)
	# 	01: CKIN1
	# 	10: CKIN2
	# 	11: Reserved
	# 	"""
	# 	if value == 3:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[7][5:8] = value
	#
	# def set_hlog_2(self, value):
	# 	"""00: Normal operation
	# 	01: Holds CKOUT2 output at static logic 0.
	# 	Entrance and exit from this state will occur without glitches or runt pulses.
	# 	10:Holds CKOUT2 output at static logic 1.
	# 	Entrance and exit from this state will occur without glitches or runt pulses.
	# 	11: Reserved
	# 	"""
	# 	if value == 3:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[8][0:2] = value
	#
	# def set_hlog_1(self, value):
	# 	"""00: Normal operation
	# 	01: Holds CKOUT1 output at static logic 0.
	# 	Entrance and exit from this state will occur without glitches or runt pulses.
	# 	10:Holds CKOUT1 output at static logic 1.
	# 	Entrance and exit from this state will occur without glitches or runt pulses.
	# 	11: Reserved
	# 	"""
	# 	if value == 3:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[8][2:4] = value
	#
	# def set_hist_avg(self, value):
	# 	"""Selects amount of averaging time to be used in generating the history information for Digital Hold.
	# 	"""
	# 	self.regs[9][0:5] = value
	#
	# def set_dsbl2_reg(self, value):
	# 	"""This bit controls the powerdown of the CKOUT2 output buffer. If disable mode is selected, the NC2_LS output divider is also powered down.
	# 	0: CKOUT2 enabled.
	# 	1: CKOUT2 disabled.
	# 	"""
	# 	self.regs[10][-4] = value
	#
	# def set_dsbl1_reg(self, value):
	# 	"""This bit controls the powerdown of the CKOUT1 output buffer. If disable mode is selected, the NC1_LS output divider is also powered down.
	# 	0: CKOUT1 enabled.
	# 	1: CKOUT1 disabled.
	# 	"""
	# 	self.regs[10][-3] = value
	#
	# def set_pd_ck2(self, value):
	# 	"""This bit controls the powerdown of the CKIN2 input buffer.
	# 	0: CKIN2 enabled.
	# 	1: CKIN2 disabled.
	# 	"""
	# 	self.regs[11][-2] = value
	#
	# def set_pd_ck1(self, value):
	# 	"""This bit controls the powerdown of the CKIN1 input buffer.
	# 	0: CKIN1 enabled.
	# 	1: CKIN1 disabled.
	# 	"""
	# 	self.regs[11][-1] = value
	#
	# def set_fos_en(self, value):
	# 	"""Frequency Offset Enable globally disables FOS. See the individual FOS enables (FOS-x_EN, register 139).
	# 	0: FOS disable
	# 	1: FOS enabled by FOSx_EN
	# 	"""
	# 	self.regs[19][0] = value
	#
	# def set_fos_thr(self, value):
	# 	"""Frequency Offset at which FOS is declared:
	# 	00: ± 11 to 12 ppm (Stratum 3/3E compliant, with a Stratum 3/3E used for REFCLK
	# 	01: ± 48 to 49 ppm (SMC)
	# 	10: ± 30 ppm (SONET Minimum Clock (SMC), with a Stratum 3/3E used for REFCLK.
	# 	11: ± 200 ppm
	# 	"""
	# 	self.regs[19][1:3] = value
	#
	# def set_valtime(self, value):
	# 	"""Sets amount of time for input clock to be valid before the associated alarm is removed.
	# 	00: 2 ms
	# 	01: 100 ms
	# 	10: 200 ms
	# 	11: 13 seconds
	# 	"""
	# 	self.regs[19][3:5] = value
	#
	# def set_lockt(self, value):
	# 	"""Sets retrigger interval for one shot monitoring phase detector output. One shot is triggered by phase slip in DSPLL. Refer to the Family Reference Manual for more details. To minimize lock time, the value 001 for LOCKT is recommended (see “ AN803: Lock and Settling Time Considerations for Si5324/27/69/74 Any-Frequency Jitter Attenuating Clock ICs” for additional details).
	# 	000: 106 ms
	# 	001: 53 ms
	# 	010: 26.5 ms
	# 	011: 13.3 ms
	# 	100: 6.6 ms
	# 	101: 3.3 ms
	# 	110: 1.66 ms
	# 	111: .833 ms
	# 	"""
	# 	self.regs[19][5:8] = value
	#
	# def set_ck2_bad_pin(self, value):
	# 	"""The CK2_BAD status can be reflected on the C2B output pin.
	# 	0: C2B output pin tristated
	# 	1: C2B status reflected to output pin
	# 	"""
	# 	self.regs[20][-4] = value
	#
	# def set_ck1_bad_pin(self, value):
	# 	"""The CK1_BAD status can be reflected on the C1B output pin.
	# 	0: C1B output pin tristated
	# 	1: C1B status reflected to output pin
	# 	"""
	# 	self.regs[20][-3] = value
	#
	# def set_lol_pin(self, value):
	# 	"""The LOL_INT status bit can be reflected on the LOL output pin.
	# 	0: LOL output pin tristated
	# 	1: LOL_INT status reflected to output pin
	# 	"""
	# 	self.regs[20][-2] = value
	#
	# def set_int_pin(self, value):
	# 	"""Reflects the interrupt status on the INT_C1B output pin.
	# 	0: Interrupt status not displayed on INT_C1B output pin. If CK1_BAD_PIN = 0, INT_C1B output pin is tristated.
	# 	1: Interrupt status reflected to output pin. Instead, the INT_C1B pin indicates when CKIN1 is bad.
	# 	"""
	# 	self.regs[20][-1] = value
	#
	# def set_ck1_actv_pin(self, value):
	# 	"""The CK1_ACTV_REG status bit can be reflected to the CS_CA output pin using the CK1_ACTV_PIN enable function. CK1_ACTV_PIN is of consequence only when pin controlled clock selection is not being used.
	# 	0: CS_CA output pin tristated.
	# 	1: Clock Active status reflected to output pin.
	# 	"""
	# 	self.regs[21][-2] = value
	#
	# def set_cksel_pin(self, value):
	# 	"""If manual clock selection is being used, clock selection can be controlled via the CKSEL_REG[1:0] register bits or the CS_CA input pin. This bit is only active when AUTOSEL_REG = Manual.
	# 	0: CS_CA pin is ignored. CKSEL_REG[1:0] register bits control clock selection.
	# 	1: CS_CA input pin controls clock selection.
	# 	"""
	# 	self.regs[21][-1] = value
	#
	# def set_ck_actv_pol(self, value):
	# 	"""Sets the active polarity for the CS_CA signals when reflected on an output pin.
	# 	0: Active low
	# 	1: Active high
	# 	"""
	# 	self.regs[22][-4] = value
	#
	# def set_ck_bad_pol(self, value):
	# 	"""Sets the active polarity for the INT_C1B and C2B signals when reflected on output pins.
	# 	0: Active low
	# 	1: Active high
	# 	"""
	# 	self.regs[22][-3] = value
	#
	# def set_lol_pol(self, value):
	# 	"""Sets the active polarity for the LOL status when reflected on an output pin.
	# 	0: Active low
	# 	1: Active high
	# 	"""
	# 	self.regs[22][-2] = value
	#
	# def set_int_pol(self, value):
	# 	"""Sets the active polarity for the interrupt status when reflected on the INT_C1B output pin.
	# 	0: Active low
	# 	1: Active high
	# 	"""
	# 	self.regs[22][-1] = value
	#
	# def set_los2_msk(self, value):
	# 	"""Determines if a LOS on CKIN2 (LOS2_FLG) is used in the generation of an interrupt. Writes to this register do not change the value held in the LOS2_FLG register.
	# 	0: LOS2 alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: LOS2_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[23][-3] = value
	#
	# def set_los1_msk(self, value):
	# 	"""Determines if a LOS on CKIN1 (LOS1_FLG) is used in the generation of an interrupt. Writes to this register do not change the value held in the LOS1_FLG register.
	# 	0: LOS1 alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: LOS1_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[23][-2] = value
	#
	# def set_losx_msk(self, value):
	# 	"""Determines if a LOS on XA/XB(LOSX_FLG) is used in the generation of an interrupt. Writes to this register do not change the value held in the LOSX_FLG register.
	# 	0: LOSX alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: LOSX_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[23][-1] = value
	#
	# def set_fos2_msk(self, value):
	# 	"""Determines if the FOS2_FLG is used to in the generation of an interrupt. Writes to this register do not change the value held in the FOS2_FLG register.
	# 	0: FOS2 alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: FOS2_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[24][-3] = value
	#
	# def set_fos1_msk(self, value):
	# 	"""Determines if the FOS1_FLG is used in the generation of an interrupt. Writes to this register do not change the value held in the FOS1_FLG register.
	# 	0: FOS1 alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: FOS1_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[24][-2] = value
	#
	# def set_lol_msk(self, value):
	# 	"""Determines if the LOL_FLG is used in the generation of an interrupt. Writes to this register do not change the value held in the LOL_FLG register.
	# 	0: LOL alarm triggers active interrupt on INT_C1B output (if INT_PIN=1).
	# 	1: LOL_FLG ignored in generating interrupt output.
	# 	"""
	# 	self.regs[24][-1] = value
	#
	def get_n1_hs(self):
		"""Gets value for N1 high speed divider which drives NCn_LS (n = 1 to 2) low-speed divider.

		000: N1= 4


		001: N1= 5

		010: N1=6

		011: N1= 7

		100: N1= 8

		101: N1= 9

		110: N1= 10

		111: N1= 11
		"""
		return self.regs[25][0:3].uint

	def get_nc1_ls(self):
		"""Gets value for NC1 low-speed divider, which drives CKOUT1 output. Must be 0 or odd.

		00000000000000000000 = 1

		00000000000000000001 = 2

		00000000000000000011 = 4

		00000000000000000101 = 6

		...

		11111111111111111111=2^20

		Valid divider values=[1, 2, 4, 6, ..., 2^20]
		"""
		value = BitArray(length=20)
		value[0:4] = self.regs[31][4:8]
		value[4:12] = self.regs[32]
		value[12:20] = self.regs[33]
		return value.uint

	def get_nc2_ls(self):

		"""Gets value for NC2 low-speed divider, which drives CKOUT2 output. Must be 0 or odd.

		00000000000000000000 = 1

		00000000000000000001 = 2

		00000000000000000011 = 4

		00000000000000000101 = 6

		...

		11111111111111111111=2^20

		Valid divider values=[1, 2, 4, 6, ..., 2^20]
		"""
		value = BitArray(length=20)
		value[0:4] = self.regs[34][4:8]
		value[4:12] = self.regs[35]
		value[12:20] = self.regs[36]
		return value.uint

	def get_n2_hs(self):
		"""Gets value for N2 high speed divider which drives N2LS low-speed divider.

		000: 4

		001: 5

		010: 6

		011: 7

		100: 8

		101: 9

		110: 10

		111: 11
		"""
		return self.regs[40][0:3].uint

	def get_n2_ls(self):
		"""Gets value for N2 low-speed divider, which drives phase detector.

		00000000000000000001 = 2

		00000000000000000011 = 4

		00000000000000000101 = 6

		...

		11111111111111111111 = 2^20

		Valid divider values = [2, 4, 6, ..., 2^20 ]
		"""
		value = BitArray(length=20)
		value[0:4] = self.regs[40][4:8]
		value[4:12] = self.regs[41]
		value[12:20] = self.regs[42]
		return value.uint

	def get_n31(self):
		"""Gets value for input divider for CKIN1.

		0000000000000000000 = 1

		0000000000000000001 = 2

		0000000000000000010 = 3

		...

		1111111111111111111 = 2^19

		Valid divider values = [1, 2, 3, ..., 2^19 ]
		"""
		value = BitArray(length=19)
		value[0:3] = self.regs[43][5:8]
		value[3:11] = self.regs[44]
		value[11:19] = self.regs[45]
		return value.uint

	def get_n32(self):
		"""Gets value for input divider for CKIN2.

		0000000000000000000 = 1

		0000000000000000001 = 2

		0000000000000000010 = 3

		...

		1111111111111111111 = 2^19

		Valid divider values = [1, 2, 3, ..., 2^19 ]
		"""
		value = BitArray(length=19)
		value[0:3] = self.regs[46][5:8]
		value[3:11] = self.regs[47]
		value[11:19] = self.regs[48]
		return value.uint
	#
	# def set_clkin2rate(self, value):
	# 	"""CKINn frequency selection for FOS alarm monitoring.
	# 	000: 10–27 MHz
	# 	001: 25–54 MHz
	# 	002: 50–105 MHz
	# 	003: 95–215 MHz
	# 	004: 190–435 MHz
	# 	005: 375–710 MHz
	# 	006: Reserved
	# 	007: Reserved
	# 	"""
	# 	if value == 6 or value == 7:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[55][-6:-3] = value
	#
	# def set_clkin1rate(self, value):
	# 	"""CKINn frequency selection for FOS alarm monitoring.
	# 	000: 10–27 MHz
	# 	001: 25–54 MHz
	# 	002: 50–105 MHz
	# 	003: 95–215 MHz
	# 	004: 190–435 MHz
	# 	005: 375–710 MHz
	# 	006: Reserved
	# 	007: Reserved
	# 	"""
	# 	if value == 6 or value == 7:
	# 		raise NameError("Value %d is reserved" % value)
	# 	self.regs[55][5:8] = value
	#
	#
	# # registers 128 to 130 are R/O
	#
	# def set_los2_flg(self, value):
	# 	"""CKIN2 Loss-of-Signal Flag.
	# 	0: Normal operation.
	# 	1: Held version of LOS2_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by LOS2_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[131][-3] = value
	#
	# def set_los1_flg(self, value):
	# 	"""CKIN1 Loss-of-Signal Flag.
	# 	0: Normal operation
	# 	1: Held version of LOS1_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by LOS1_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[131][-2] = value
	#
	# def set_losx_flg(self, value):
	# 	"""External Reference (signal on pins XA/XB) Loss-of-Signal Flag.
	# 	0: Normal operation
	# 	1: Held version of LOSX_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by LOSX_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[131][-1] = value
	#
	# def set_fos2_flg(self, value):
	# 	"""CLKIN_2 Frequency Offset Flag.
	# 	0: Normal operation.
	# 	1: Held version of FOS2_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by FOS2_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[132][-4] = value
	#
	# def set_fos1_flg(self, value):
	# 	"""CLKIN_1 Frequency Offset Flag.
	# 	0: Normal operation
	# 	1: Held version of FOS1_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by FOS1_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[132][-3] = value
	#
	# def set_lol_flg(self, value):
	# 	"""PLL Loss of Lock Flag.
	# 	0: PLL locked
	# 	1: Held version of LOL_INT. Generates active output interrupt if output interrupt pin is enabled (INT_PIN = 1) and if not masked by LOL_MSK bit. Flag cleared by writing 0 to this bit.
	# 	"""
	# 	self.regs[132][-2] = value
	#
	#
	# # registers 134 and 135 are R/O
	#
	# def set_rst_reg(self, value):
	# 	"""Internal Reset (Same as Pin Reset).
	# 	Note: The I2C (or SPI) port may not be accessed until 10 ms after RST_REG is asserted.
	# 	0: Normal operation.
	# 	1: Reset of all internal logic. Outputs disabled or tristated during reset.
	# 	"""
	# 	self.regs[136][0] = value
	#
	# def set_ical(self, value):
	# 	"""Start an Internal Calibration Sequence.
	# 	For proper operation, the device must go through an internal calibration sequence.
	# 	ICAL is a self-clearing bit. Writing a one to this location initiates an ICAL. The calibration is complete once the LOL alarm goes low. A valid stable clock (within 100 ppm) must be present to begin ICAL.
	# 	Note: Any divider, CLKINn_RATE or BWSEL_REG changes require an ICAL to take effect.
	# 	0: Normal operation.
	# 	1: Writing a "1" initiates internal self-calibration. Upon completion of internal self-calibration, LOL will go low.
	# 	"""
	# 	self.regs[136][1] = value
	#
	# def set_fastlock(self, value):
	# 	"""This bit must be set to 1 to enable FASTLOCK. This improves initial lock time by dynamically changing the loop bandwidth.
	# 	"""
	# 	self.regs[137][-1] = value
	#
	# def set_los2_en(self, value):
	# 	"""Enable CKIN2 LOS Monitoring on the Specified Input (2 of 2).
	# 	Note: LOS2_EN is split between two registers.
	# 	00: Disable LOS monitoring.
	# 	01: Reserved.
	# 	10: Enable LOSA monitoring.
	# 	11: Enable LOS monitoring.
	# 	LOSA is a slower and less sensitive version of LOS. See the Family Reference Manual for details.
	# 	"""
	# 	if value == 1:
	# 		raise NameError("Value %d is reserved" % value)
	# 	value = BitArray(uint=value, length=2)
	# 	self.regs[138][-2] = value[0]
	# 	self.regs[139][-6] = value[1]
	#
	# def set_los1_en(self, value):
	# 	"""Enable CKIN1 LOS Monitoring on the Specified Input (1 of 2).
	# 	Note: LOS1_EN is split between two registers.
	# 	00: Disable LOS monitoring.
	# 	01: Reserved.
	# 	10: Enable LOSA monitoring.
	# 	11: Enable LOS monitoring.
	# 	LOSA is a slower and less sensitive version of LOS. See the Family Reference Manual for details.
	# 	"""
	# 	if value == 1:
	# 		raise NameError("Value %d is reserved" % value)
	# 	value = BitArray(uint=value, length=2)
	# 	self.regs[138][-1] = value[0]
	# 	self.regs[139][-5] = value[1]
	#
	# def set_fos2_en(self, value):
	# 	"""Enables FOS on a Per Channel Basis.
	# 	0: Disable FOS monitoring.
	# 	1: Enable FOS monitoring.
	# 	"""
	# 	self.regs[139][-2] = value
	#
	# def set_fos1_en(self, value):
	# 	"""Enables FOS on a Per Channel Basis.
	# 	0: Disable FOS monitoring.
	# 	1: Enable FOS monitoring.
	# 	"""
	# 	self.regs[139][-1] = value
	#
	# def set_independentskew1(self, value):
	# 	"""INDEPENDENTSKEW1.
	# 	8 bit field that represents a twos complement of the phase offset in terms of clocks from the high speed output divider. Default = 0.
	# 	"""
	# 	value = BitArray(uint=value, length=8)
	# 	self.regs[142] = value
	#
	# def set_independentskew2(self, value):
	# 	"""INDEPENDENTSKEW2.
	# 	8 bit field that represents a twos complement of the phase offset in terms of clocks from the high speed output divider. Default = 0.
	# 	"""
	# 	value = BitArray(uint=value, length=8)
	# 	self.regs[143] = value