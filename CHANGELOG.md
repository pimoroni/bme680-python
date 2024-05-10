2.0.0
-----

* Repackage to hatch/pyproject.toml
* Drop Python 2.7 support
* Switch from smbu2 to smbus2

1.1.1
-----

* New: constants to clarify heater on/off states

1.1.0
-----

* New: support for BME688 "high" gas resistance variant
* New: set/get gas heater disable bit
* Enhancement: fail with descriptive RuntimeError when chip is not detected

1.0.5
-----

* New: set_temp_offset to calibrate temperature offset in degrees C

1.0.4
-----

* Fix to range_sw_err for extremely high gas readings
* Convert to unsigned int to fix negative gas readings

1.0.3
-----

* Merged temperature compensation fix from Bosch's BME680_driver 3.5.3

1.0.2
-----

* Fixed set_gas_heater_temperature to avoid i2c TypeError

1.0.1
-----

* Added Manifest to Python package

1.0.0
-----

* Initial release

