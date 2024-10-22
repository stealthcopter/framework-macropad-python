# Framework RGB Macropad Python

This is a Circuit Python implementation of a per-key LED layered macropad. I'm super pumped I could get it working and doens't appear to have any performance issues, I was expecting it wouldn't be able to read key presses or update the LEDs fast enough, but it seems solid.

This code is based on the starter code developed [here](https://github.com/FrameworkComputer/Framework_Inputmodule_CircuitPython), but it was incomplete and somewhat confusing for me. So decided to spend a weekend hacking this little project together. I hope this all makes sense, please shout if something is not clear.

## Motivation & Alternatives

I wanted to be able to tinker with my macropad and rapidly change things on a per-key basis, which makes the circuit cpython build ideal, as there is no need to compile firmware each time. There is also an [OpenRGB firmware](https://community.frame.work/t/guide-how-to-install-openrgb-on-fw16/53358) guide that may be an option to you if you are looking for something different. 

## Firmware

1. Either use the pre-compiled firmware in the [releases](https://github.com/stealthcopter/framework-macropad-python/releases) section or follow the guide for building this yourself in [readme-firmware-build.md](readme-firmware-build.md)
2. Install the firmware, [readme-firmware-install.md](readme-firmware-install.md)

# Configuration

I've attempted to make this as configurable as possible while keeping it as simple as possible. You mostly just need to modify lists and lists and lists in the `config.py`

## Key maps

First we have key maps that define the location of the keys to key presses

```python
KEYMAP_01 = [
    [A, B, C, D],
    [E, F, G, H],
    [I, J, K, L],
    [M, N, O, P],
    [Q, R, S, T],
    [U, V, W, X],
]
```

These also support combinations, for example instead of `L` you could have `[CTRL, ALT, L]`, or `[COMMAND, P]`. Full keycodes can be seen in the adafruit [Keycodes](https://docs.circuitpython.org/projects/hid/en/latest/api.html) docs.

## Color Maps

Then we have color maps that will define what color each key should be:

```python
COLORMAP_01 = [
    [GREEN, GREEN,   GREEN, GREEN],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [AQUA,  AQUA,    AQUA,  AQUA],
    [GREEN, FUSHIA,  AQUA,  GREEN],
]
```

The full list of colors are in `colors.py` and if a whole layer is just one color you can provide a single color instead of a list of list and it will work and save a tiny bit of memory.

## Layers

These are then combined into two lists which will work as our layers.

```python
LAYER_KEYMAPS = [ KEYMAP_01,   KEYMAP_01,   KEYMAP_01   ]
LAYER_COLORS =  [ COLORMAP_01, COLORMAP_02, COLORMAP_03 ]
```

This means that we can have an arbitrary number of layers defined, pretty neat.

## Weird stuff

- The firmware is compiled with 9.x but the adafruit libraries 9.x versions would not work on the device, complained about verison mismatch, where as the 8.x versions worked. Assume this is because it must be based off some janky alpha 9 pre-release?

## TODO

- **Make some nicer set-ups**: I'm terrible as design stuff, so it'd be good to come up with some better default layouts people can build from, maybe an `config.example.py`. Possibly even a config generator if anyone is actually interested in this project.
- **Multiple key presses**: Currently multiple key presses on the macro pad will be ignored and only the first key in the loop will be considered. This should be easy enough to update though.
- **USB Communication**: The serial stuff works fine and REPL (interactive shell) is good but the firmware doesn't allow for use of this connection and a USB data connection at the same time. This feature seems to be something you can enable using some flags, but I've not managed to get it working yet. 
- **Rebase and rebuild firmware**: Should probably take the minor changes in the PR and my fixes and rebase to the latest circuit python, might fix the weirdness with library versions

# Contributing

Happily accepting [issues](https://github.com/stealthcopter/framework-macropad-python/issues), feature suggestions (nothing too complex please) and PRs. 