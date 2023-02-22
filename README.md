# led-matrix-demo

This repository contains examples for displaying images or playing games on a 2D LED matrix running [WLED](https://github.com/Aircoookie/WLED).

## led_matrix.py

- Implements a simple way to update the LED matrix with a custom image in a `.bmp` or `.png` format.
- Showcases how to pack the pixel data and use the [WLED JSON API](https://kno.wled.ge/interfaces/json-api/).

To use this:

1) Simply change the `IP` variable to the IP address of your WLED instance,
2) uncomment one of the example lines at the end of the file,
3) run with `python led_matrix.py`.

You can also import the `update_matrix` and `from_img` functions and use them in your own code.