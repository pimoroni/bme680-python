# Change Log
All notable changes to the BME680 Sensor API will be documented in this file.

## v3.5.1, 5 Jul 2017
### Changed
 - Fixed bug with overwriting of the result with communication results
 - Added member in the dev structure to store communication results
 - Updated set profile duration API to not return a result.
 - Added new API to get the duration for the existing profile
 - Fixed bug with setting gas configuration. Reduced to writing only relevant bytes
 - Updated readme
 - Updated documentation for the type definitions
 - Removed mode check for get sensor data and setting and getting profile dur
 

## v3.5.0, 28 Jun 2017
### Changed
- Fixed bug with getting and setting mem pages
- Changed initialization sequence to be more robust
- Added additional tries while reading data in case of inadequate delay


## v3.4.0, 8 Jun 2017
### Changed
- Modified the bme680_get_sensor_data API. User has to now pass the struct that stores the data rather than retrieving from the bme680_dev structure.
- Fixed possible bugs

## v3.3.0, 24 May 2017
### Changed
- Name changes in the BME680 device structure.
- Removed sequential and parallel modes.
- Removed ODR related sensor settings
- Modified get sensor settings API with user selection.
- Removed sort sensor data and swap fields API which are not required.

### Added
- BME680 set profile duration API.

## v3.2.1, 17 May 2017
### Added
- Took the reference as base version 3.2.1 of BME680 sensor and added.

