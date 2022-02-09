# BME68x

[![Build Status](https://travis-ci.org/pimoroni/bme680-python.svg?branch=master)](https://travis-ci.org/pimoroni/bme680-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/bme680-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/bme680-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/bme680.svg)](https://pypi.python.org/pypi/bme680)
[![Python Versions](https://img.shields.io/pypi/pyversions/bme680.svg)](https://pypi.python.org/pypi/bme680)

BME68x is a series of state-of-the-art environmental sensors that let you measure temperature, pressure, humidity and indoor air quality.

This library is designed to work with the following products:

* BME680 Breakout - https://shop.pimoroni.com/products/bme680
* BME688 4-in-1 Air Quality Breakout - https://shop.pimoroni.com/products/bme688-breakout

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your BME68x
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/bme680 | bash
```

### Manual install:

#### Library install for Python 3:

```bash
sudo pip3 install bme680
```

#### Library install for Python 2:

```bash
sudo pip2 install bme680
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo python3 setup.py install
```
(or `sudo python setup.py install` whichever your primary Python environment may be)

In all cases you will have to have I2C enabled (`sudo raspi-config`, under 'Interfacing Options').

## Documentation & Support

* Guides and tutorials - https://learn.pimoroni.com/bme680-breakout
* Get help - http://forums.pimoroni.com/c/support
