BME680
======

https://shop.pimoroni.com/products/bme680

The state-of-the-art BME680 breakout lets you measure temperature,
pressure, humidity, and indoor air quality.

Installing
----------

Full install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've created an easy installation script that will install all
pre-requisites and get your BME680 up and running with minimal efforts.
To run it, fire up Terminal which you'll find in Menu -> Accessories ->
Terminal on your Raspberry Pi desktop, as illustrated below:

.. figure:: http://get.pimoroni.com/resources/github-repo-terminal.png
   :alt: Finding the terminal

In the new terminal window type the command exactly as it appears below
(check for typos) and follow the on-screen instructions:

.. code:: bash

    curl https://get.pimoroni.com/bme680 | bash

Manual install:
~~~~~~~~~~~~~~~

Library install for Python 3:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    sudo pip3 install bme680

Library install for Python 2:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    sudo pip2 install bme680

Development:
~~~~~~~~~~~~

If you want to contribute, or like living on the edge of your seat by
having the latest code, you should clone this repository, ``cd`` to the
library directory, and run:

.. code:: bash

    sudo python3 setup.py install

(or ``sudo python setup.py install`` whichever your primary Python
environment may be)

In all cases you will have to enable the i2c bus.

Documentation & Support
-----------------------

-  Guides and tutorials - https://learn.pimoroni.com/bme680
-  Get help - http://forums.pimoroni.com/c/support

