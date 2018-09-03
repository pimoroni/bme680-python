#!/usr/bin/env python
import bme680

print("""Display Temperature, Pressure and Humidity with different offsets.
""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)


def display_data(offset=0):
    sensor.set_temp_offset(offset)
    sensor.get_sensor_data()
    output = '{0:.2f} C, {1:.2f} hPa, {2:.3f} %RH'.format(
        sensor.data.temperature,
        sensor.data.pressure,
        sensor.data.humidity)
    print(output)
    print('')


print('Initial readings')
display_data()

print('SET offset 4 degrees celsius')
display_data(4)

print('SET offset -1.87 degrees celsius')
display_data(-1.87)

print('SET offset -100 degrees celsius')
display_data(-100)

print('SET offset 0 degrees celsius')
display_data(0)
