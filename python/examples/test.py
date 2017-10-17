"""
        Pressure     Temperature    Humidity
128,0,  79,186,128,  122,185,0,     76,55,      128,0,0,   29,39,

128,0,  79,186,144,  122,185,64,    76,59,      128,0,0,   220,120,
2017-10-13 22:51:50 T: 26.67 degC, P: 1011.79 hPa, H: 49.64 %rH , G: 24487 ohms

128,0,  79,186,160,  122,186,32,    76,61,      128,0,0,   70,56,
2017-10-13 22:51:53 T: 26.68 degC, P: 1011.79 hPa, H: 49.65 %rH , G: 37891 ohms

128,0,  79,186,224,  122,187,0,     76,61,      128,0,0,   205,55,
2017-10-13 22:51:56 T: 26.68 degC, P: 1011.79 hPa, H: 49.65 %rH , G: 51080 ohms

128,0,  79,186,224,  122,187,224,   76,62,      128,0,0,   127,247,
2017-10-13 22:51:59 T: 26.68 degC, P: 1011.79 hPa, H: 49.66 %rH , G: 63052 ohms

128,0,  79,187,32,   122,188,64,    76,58,      128,0,0,   78,119,
2017-10-13 22:52:02 T: 26.69 degC, P: 1011.79 hPa, H: 49.63 %rH , G: 74195 ohms

128,0,  79,187,112,  122,189,64,    76,48,      128,0,0,   46,183,
2017-10-13 22:52:05 T: 26.69 degC, P: 1011.77 hPa, H: 49.57 %rH , G: 83681 ohms

128,0,  79,187,128,  122,189,160,   76,45,      128,0,0,   25,55,
2017-10-13 22:52:08 T: 26.69 degC, P: 1011.77 hPa, H: 49.55 %rH , G: 91612 ohms

128,0,  79,187,144,  122,189,240,   76,48,      128,0,0,   223,182,
2017-10-13 22:52:11 T: 26.69 degC, P: 1011.77 hPa, H: 49.57 %rH , G: 97109 ohms

128,0,  79,187,160,  122,190,80,    76,49,      128,0,0,   198,118,
2017-10-13 22:52:14 T: 26.70 degC, P: 1011.77 hPa, H: 49.58 %rH , G: 103197 ohms
"""


import bme680

example_calibration = [
#         T2L   T2H   T3    TP    P1L   P1H   P2L
    192,  108,  103,  3,    47,   80,   144,  236,
#   P2H   P3    -     P4L   P4H   P5L   P5H   P7
    214,  88,   255,  42,   30,   169,  255,  54,
#   P6    -     -     P8L   P8H   P9L   P9H   P10
    30,   0,    0,    199,  239,  69,   248,  30,
#   H2H   H2L   H1L   H1H   H3    H4    H5    H6
    1,    64,   206,  39,   0,    45,   20,   120,
#   H7    T1L   T1H   GH2L  GH2H  GH1   GH3
    156,  24,   102,  142,  171,  226,  18,   16,
    0
]

example_heat_range = 22
example_heat_value = 44
example_sw_error = 227

sensor = bme680.BME680()

sensor.calibration_data.set_from_array(example_calibration)
sensor.calibration_data.set_other(
    example_heat_range,
    example_heat_value,
    example_sw_error)

for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            print("{}: {}".format(name, value))

sensor.ambient_temperature = 25

"""
result = []
for x in range(63, 4033):
    result.append((x, sensor._calc_heater_duration(x)))

print(result)

result = []
for x in range(200, 401):
    result.append(sensor._calc_heater_resistance(x))

print(result)
"""

"""
        Pressure     Temperature    Humidity               Gas
128,0,  79,187,160,  122,190,80,    76,49,      128,0,0,   198,118,
2017-10-13 22:52:14 T: 26.70 degC, P: 1011.77 hPa, H: 49.58 %rH , G: 103197 ohms
"""

regs = [128,0,  79,186,144,  122,185,64,    76,59,      128,0,0,   220,120]
vals = [26.67, 1011.79, 49.64, 24487]

adc_pres = (regs[2] << 12) | (regs[3] << 4) | (regs[4] >> 4)
adc_temp = (regs[5] << 12) | (regs[6] << 4) | (regs[7] >> 4)
adc_hum = (regs[8] << 8) | regs[9]
adc_gas_res = (regs[13] << 2) | (regs[14] >> 6)
gas_range = regs[14] & bme680.constants.GAS_RANGE_MSK

result = sensor._calc_temperature(adc_temp) / 100
print("Temperature: Raw: {}: {} {}".format(adc_temp, vals[0], result))

result = sensor._calc_pressure(adc_pres)
print("Pressure:    Raw: {}: {} {}".format(adc_pres, vals[1], result))

result = sensor._calc_humidity(adc_hum) / 1000
print("Humidity:    Raw: {}:  {}% {}%".format(adc_hum, vals[2], result))

result = sensor._calc_gas_resistance(adc_gas_res, gas_range)
print("Resistance:  Raw: {}:    {} {}".format(adc_gas_res, vals[3], result))
