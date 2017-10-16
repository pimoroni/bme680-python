import bme680

sensor = bme680.BME680()

for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            print("{}: {}".format(name, value))


sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_power_mode(bme680.FORCED_MODE)

sensor.get_sensor_data()

for name in dir(sensor.data):
    value = getattr(sensor.data, name)
    print("{}: {}".format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)

try:
    while True:
        sensor.set_power_mode(bme680.FORCED_MODE)
        sensor.get_sensor_data()

        for name in dir(sensor.data):
            value = getattr(sensor.data, name)
            if not name.startswith('_'):
                print("{}: {}".format(name, value))

except KeyboardInterrupt:
    pass

