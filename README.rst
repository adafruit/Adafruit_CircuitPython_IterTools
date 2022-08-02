Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-itertools/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/itertools/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_IterTools/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_IterTools/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Python's itertools for CircuitPython


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.


Usage Example
=============

.. code-block:: python

    import time
    import board
    import busio
    import adafruit_si7021
    from adafruit_itertools.adafruit_itertools import count
    from adafruit_itertools.adafruit_itertools_extras import repeatfunc

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_si7021.SI7021(i2c)

    def read_temperature():
        return sensor.temperature

   def now():
       return time.monotonic()

    datapoints = zip(count(1), repeatfunc(now), map(int, repeatfunc(read_temperature)))

    while True:
        print(next(datapoints))
        time.sleep(20.0)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/itertools/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_itertools/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
