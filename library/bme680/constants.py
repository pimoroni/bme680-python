"""BME680 constants, structures and utilities."""

# BME680 General config
POLL_PERIOD_MS = 10

# BME680 I2C addresses
I2C_ADDR_PRIMARY = 0x76
I2C_ADDR_SECONDARY = 0x77

# BME680 unique chip identifier
CHIP_ID = 0x61

# BME680 coefficients related defines
COEFF_SIZE = 41
COEFF_ADDR1_LEN = 25
COEFF_ADDR2_LEN = 16

# BME680 field_x related defines
FIELD_LENGTH = 15
FIELD_ADDR_OFFSET = 17

# Soft reset command
SOFT_RESET_CMD = 0xb6

# Error code definitions
OK = 0
# Errors
E_NULL_PTR = -1
E_COM_FAIL = -2
E_DEV_NOT_FOUND = -3
E_INVALID_LENGTH = -4

# Warnings
W_DEFINE_PWR_MODE = 1
W_NO_NEW_DATA = 2

# Info's
I_MIN_CORRECTION = 1
I_MAX_CORRECTION = 2

# Register map
# Other coefficient's address
ADDR_RES_HEAT_VAL_ADDR = 0x00
ADDR_RES_HEAT_RANGE_ADDR = 0x02
ADDR_RANGE_SW_ERR_ADDR = 0x04
ADDR_SENS_CONF_START = 0x5A
ADDR_GAS_CONF_START = 0x64

# Field settings
FIELD0_ADDR = 0x1d

# Heater settings
RES_HEAT0_ADDR = 0x5a
GAS_WAIT0_ADDR = 0x64

# Sensor configuration registers
CONF_HEAT_CTRL_ADDR = 0x70
CONF_ODR_RUN_GAS_NBC_ADDR = 0x71
CONF_OS_H_ADDR = 0x72
MEM_PAGE_ADDR = 0xf3
CONF_T_P_MODE_ADDR = 0x74
CONF_ODR_FILT_ADDR = 0x75

# Coefficient's address
COEFF_ADDR1 = 0x89
COEFF_ADDR2 = 0xe1

# Chip identifier
CHIP_ID_ADDR = 0xd0

# Soft reset register
SOFT_RESET_ADDR = 0xe0

# Heater control settings
ENABLE_HEATER = 0x00
DISABLE_HEATER = 0x08

# Gas measurement settings
DISABLE_GAS_MEAS = 0x00
ENABLE_GAS_MEAS = 0x01

# Over-sampling settings
OS_NONE = 0
OS_1X = 1
OS_2X = 2
OS_4X = 3
OS_8X = 4
OS_16X = 5

# IIR filter settings
FILTER_SIZE_0 = 0
FILTER_SIZE_1 = 1
FILTER_SIZE_3 = 2
FILTER_SIZE_7 = 3
FILTER_SIZE_15 = 4
FILTER_SIZE_31 = 5
FILTER_SIZE_63 = 6
FILTER_SIZE_127 = 7

# Power mode settings
SLEEP_MODE = 0
FORCED_MODE = 1

# Delay related macro declaration
RESET_PERIOD = 10

# SPI memory page settings
MEM_PAGE0 = 0x10
MEM_PAGE1 = 0x00

# Ambient humidity shift value for compensation
HUM_REG_SHIFT_VAL = 4

# Run gas enable and disable settings
RUN_GAS_DISABLE = 0
RUN_GAS_ENABLE = 1

# Buffer length macro declaration
TMP_BUFFER_LENGTH = 40
REG_BUFFER_LENGTH = 6
FIELD_DATA_LENGTH = 3
GAS_REG_BUF_LENGTH = 20
GAS_HEATER_PROF_LEN_MAX = 10

# Settings selector
OST_SEL = 1
OSP_SEL = 2
OSH_SEL = 4
GAS_MEAS_SEL = 8
FILTER_SEL = 16
HCNTRL_SEL = 32
RUN_GAS_SEL = 64
NBCONV_SEL = 128
GAS_SENSOR_SEL = GAS_MEAS_SEL | RUN_GAS_SEL | NBCONV_SEL

# Number of conversion settings
NBCONV_MIN = 0
NBCONV_MAX = 9  # Was 10, but there are only 10 settings: 0 1 2 ... 8 9

# Mask definitions
GAS_MEAS_MSK = 0x30
NBCONV_MSK = 0X0F
FILTER_MSK = 0X1C
OST_MSK = 0XE0
OSP_MSK = 0X1C
OSH_MSK = 0X07
HCTRL_MSK = 0x08
RUN_GAS_MSK = 0x10
MODE_MSK = 0x03
RHRANGE_MSK = 0x30
RSERROR_MSK = 0xf0
NEW_DATA_MSK = 0x80
GAS_INDEX_MSK = 0x0f
GAS_RANGE_MSK = 0x0f
GASM_VALID_MSK = 0x20
HEAT_STAB_MSK = 0x10
MEM_PAGE_MSK = 0x10
SPI_RD_MSK = 0x80
SPI_WR_MSK = 0x7f
BIT_H1_DATA_MSK = 0x0F

# Bit position definitions for sensor settings
GAS_MEAS_POS = 4
FILTER_POS = 2
OST_POS = 5
OSP_POS = 2
OSH_POS = 0
RUN_GAS_POS = 4
MODE_POS = 0
NBCONV_POS = 0

# Array Index to Field data mapping for Calibration Data
T2_LSB_REG = 1
T2_MSB_REG = 2
T3_REG = 3
P1_LSB_REG = 5
P1_MSB_REG = 6
P2_LSB_REG = 7
P2_MSB_REG = 8
P3_REG = 9
P4_LSB_REG = 11
P4_MSB_REG = 12
P5_LSB_REG = 13
P5_MSB_REG = 14
P7_REG = 15
P6_REG = 16
P8_LSB_REG = 19
P8_MSB_REG = 20
P9_LSB_REG = 21
P9_MSB_REG = 22
P10_REG = 23
H2_MSB_REG = 25
H2_LSB_REG = 26
H1_LSB_REG = 26
H1_MSB_REG = 27
H3_REG = 28
H4_REG = 29
H5_REG = 30
H6_REG = 31
H7_REG = 32
T1_LSB_REG = 33
T1_MSB_REG = 34
GH2_LSB_REG = 35
GH2_MSB_REG = 36
GH1_REG = 37
GH3_REG = 38

# BME680 register buffer index settings
REG_FILTER_INDEX = 5
REG_TEMP_INDEX = 4
REG_PRES_INDEX = 4
REG_HUM_INDEX = 2
REG_NBCONV_INDEX = 1
REG_RUN_GAS_INDEX = 1
REG_HCTRL_INDEX = 0

# Look up tables for the possible gas range values
lookupTable1 = [2147483647, 2147483647, 2147483647, 2147483647,
                2147483647, 2126008810, 2147483647, 2130303777, 2147483647,
                2147483647, 2143188679, 2136746228, 2147483647, 2126008810,
                2147483647, 2147483647]

lookupTable2 = [4096000000, 2048000000, 1024000000, 512000000,
                255744255, 127110228, 64000000, 32258064,
                16016016, 8000000, 4000000, 2000000,
                1000000, 500000, 250000, 125000]


def bytes_to_word(msb, lsb, bits=16, signed=False):
    """Convert a most and least significant byte into a word."""
    # TODO: Reimpliment with struct
    word = (msb << 8) | lsb
    if signed:
        word = twos_comp(word, bits)
    return word


def twos_comp(val, bits=16):
    """Convert two bytes into a two's compliment signed word."""
    # TODO: Reimpliment with struct
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val


class FieldData:
    """Structure for storing BME680 sensor data."""

    def __init__(self):  # noqa D107
        # Contains new_data, gasm_valid & heat_stab
        self.status = None
        self.heat_stable = False
        # The index of the heater profile used
        self.gas_index = None
        # Measurement index to track order
        self.meas_index = None
        # Temperature in degree celsius x100
        self.temperature = None
        # Pressure in Pascal
        self.pressure = None
        # Humidity in % relative humidity x1000
        self.humidity = None
        # Gas resistance in Ohms
        self.gas_resistance = None


class CalibrationData:
    """Structure for storing BME680 calibration data."""

    def __init__(self):  # noqa D107
        self.par_h1 = None
        self.par_h2 = None
        self.par_h3 = None
        self.par_h4 = None
        self.par_h5 = None
        self.par_h6 = None
        self.par_h7 = None
        self.par_gh1 = None
        self.par_gh2 = None
        self.par_gh3 = None
        self.par_t1 = None
        self.par_t2 = None
        self.par_t3 = None
        self.par_p1 = None
        self.par_p2 = None
        self.par_p3 = None
        self.par_p4 = None
        self.par_p5 = None
        self.par_p6 = None
        self.par_p7 = None
        self.par_p8 = None
        self.par_p9 = None
        self.par_p10 = None
        # Variable to store t_fine size
        self.t_fine = None
        # Variable to store heater resistance range
        self.res_heat_range = None
        # Variable to store heater resistance value
        self.res_heat_val = None
        # Variable to store error range
        self.range_sw_err = None

    def set_from_array(self, calibration):
        """Set paramaters from an array of bytes."""
        # Temperature related coefficients
        self.par_t1 = bytes_to_word(calibration[T1_MSB_REG], calibration[T1_LSB_REG])
        self.par_t2 = bytes_to_word(calibration[T2_MSB_REG], calibration[T2_LSB_REG], bits=16, signed=True)
        self.par_t3 = twos_comp(calibration[T3_REG], bits=8)

        # Pressure related coefficients
        self.par_p1 = bytes_to_word(calibration[P1_MSB_REG], calibration[P1_LSB_REG])
        self.par_p2 = bytes_to_word(calibration[P2_MSB_REG], calibration[P2_LSB_REG], bits=16, signed=True)
        self.par_p3 = twos_comp(calibration[P3_REG], bits=8)
        self.par_p4 = bytes_to_word(calibration[P4_MSB_REG], calibration[P4_LSB_REG], bits=16, signed=True)
        self.par_p5 = bytes_to_word(calibration[P5_MSB_REG], calibration[P5_LSB_REG], bits=16, signed=True)
        self.par_p6 = twos_comp(calibration[P6_REG], bits=8)
        self.par_p7 = twos_comp(calibration[P7_REG], bits=8)
        self.par_p8 = bytes_to_word(calibration[P8_MSB_REG], calibration[P8_LSB_REG], bits=16, signed=True)
        self.par_p9 = bytes_to_word(calibration[P9_MSB_REG], calibration[P9_LSB_REG], bits=16, signed=True)
        self.par_p10 = calibration[P10_REG]

        # Humidity related coefficients
        self.par_h1 = (calibration[H1_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H1_LSB_REG] & BIT_H1_DATA_MSK)
        self.par_h2 = (calibration[H2_MSB_REG] << HUM_REG_SHIFT_VAL) | (calibration[H2_LSB_REG] >> HUM_REG_SHIFT_VAL)
        self.par_h3 = twos_comp(calibration[H3_REG], bits=8)
        self.par_h4 = twos_comp(calibration[H4_REG], bits=8)
        self.par_h5 = twos_comp(calibration[H5_REG], bits=8)
        self.par_h6 = calibration[H6_REG]
        self.par_h7 = twos_comp(calibration[H7_REG], bits=8)

        # Gas heater related coefficients
        self.par_gh1 = twos_comp(calibration[GH1_REG], bits=8)
        self.par_gh2 = bytes_to_word(calibration[GH2_MSB_REG], calibration[GH2_LSB_REG], bits=16, signed=True)
        self.par_gh3 = twos_comp(calibration[GH3_REG], bits=8)

    def set_other(self, heat_range, heat_value, sw_error):
        """Set other values."""
        self.res_heat_range = (heat_range & RHRANGE_MSK) // 16
        self.res_heat_val = heat_value
        self.range_sw_err = (sw_error & RSERROR_MSK) // 16


class TPHSettings:
    """Structure for storing BME680 sensor settings.

    Comprises of output data rate, over-sampling and filter settings.

    """

    def __init__(self):  # noqa D107
        # Humidity oversampling
        self.os_hum = None
        # Temperature oversampling
        self.os_temp = None
        # Pressure oversampling
        self.os_pres = None
        # Filter coefficient
        self.filter = None


class GasSettings:
    """Structure for storing BME680 gas settings and status."""

    def __init__(self):  # noqa D107
        # Variable to store nb conversion
        self.nb_conv = None
        # Variable to store heater control
        self.heatr_ctrl = None
        # Run gas enable value
        self.run_gas = None
        # Pointer to store heater temperature
        self.heatr_temp = None
        # Pointer to store duration profile
        self.heatr_dur = None


class BME680Data:
    """Structure to represent BME680 device."""

    def __init__(self):  # noqa D107
        # Chip Id
        self.chip_id = None
        # Device Id
        self.dev_id = None
        # SPI/I2C interface
        self.intf = None
        # Memory page used
        self.mem_page = None
        # Ambient temperature in Degree C
        self.ambient_temperature = None
        # Field Data
        self.data = FieldData()
        # Sensor calibration data
        self.calibration_data = CalibrationData()
        # Sensor settings
        self.tph_settings = TPHSettings()
        # Gas Sensor settings
        self.gas_settings = GasSettings()
        # Sensor power modes
        self.power_mode = None
        # New sensor fields
        self.new_fields = None
