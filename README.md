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

## snake.py

- Implements a simple snake game to play on an LED matrix.

To use this:

1) Install the [`keyboard`](https://pypi.org/project/keyboard/) package with `pip install keyboard` (this is needed for user input),
2) run with `python snake.py`,
3) use arrow keys to steer the snake or `esc` to end the game.

This might need admin rights (`sudo`) in order to read pressed keyboard keys.

You can also display the game simultaneously on your screen and on the LED matrix.
To do this, change the `MATRIX` and `SCREEN` switches (`True` or `False`) accordingly.
If `SCREEN` is `True`, the [`pygame`](https://pypi.org/project/pygame/) package needs to be installed with `pip install pygame` for on-screen rendering.
