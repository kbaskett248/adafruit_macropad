# App Pad

A derivative of the
[Macropad Hotkeys](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/LICENSE)
example from the
[Adafruit Learning System Guide](https://learn.adafruit.com/macropad-hotkeys/project-code).

## Why use this version

I wanted to define more complex configurations than what was easily possible with the original Adafruit Macropad Hotkeys code. This project has several advanced features beyond the original project.

* Rather than switching macro sets with the encoder, you may choose to switch macro sets with keys. This allows you to define menu-based switchers, making it much faster to get to the desired set. It also frees up the rotary encoder for use as a volume knob, scrubber, or anything else.
* Each key can define an OS-specific variant. This allows you to switch up which keystrokes are sent depending on the OS you've selected.
* Double-tap support so you can define a second command for each key, giving you 24 possible commands per macro set.
* Basic timers that run callbacks. This can be used for many things, including disabling the key LEDs after a period of inactivity.
* An App-based model where the App is responsible for control flow. This allows including other types of Apps with completely different behavior, like games, alongside your macros.

## Using
Just like with the original Macropad Hotkeys code, copy all the files over to your Circuitpy drive.

The existing layout has a Home App with the following features:

* A key for selecting the platform (Linux, Mac OS, or Windows).
* Media playback controls
* The rotary encoder controls volume, and the button mutes.
* Keys for jumping to the following apps
  * Numpad
  * Navigation cluster, with arrows, Home, End, Page Up, and Page Down
  * Function Keys
  * A Window Management app which allows switching virtual desktops and quickly resizing windows. Note that this requires defining hotkeys on the host computer.
  * An app switcher you can use to quickly swap to your most used desktop programs. Some programs may have their own associated macro apps which open when switching to them. Note that this may also require defining hotkeys on the host computer.

## Customizing

There are two methods to tailor the macropad to your specific use case.
The preferred method avoids modifying any versioned files,
so you can continue to pull in updates from this project.
The second method may be easier for those without as much `git` or `python` experience.

### Preferred

The preferred way to customize your apps and hotkeys is by creating a `user` module or package.
If that module or package defines `DEFAULT_APP`, then that app will be loaded when the macropad starts.

1. Clone this repo.
2. In the base of the repo, create either `user.py` or create a directory called `user` with a file called `__init__.py`.
3. In whichever file you created, define a callable called `DEFAULT_APP`.
   The callable should accept an `AppPad` instance.
   For example, the default configuration assumes the host OS is windows.
   If you wanted to set the default host OS to MacOS instead, you could define `user.py` as follows.

   ```py
   # user.py
   from apps.home import HomeApp
   from utils.constants import OS_SETTING, OS_MAC, PREVIOUS_APP_SETTING

   app_settings = {
       OS_SETTING: OS_MAC,
       PREVIOUS_APP_SETTING: [],
   }

   DEFAULT_APP = lambda app_pad: HomeApp(app_pad, app_settings)
   ```

That's all there is to it.

### Method 2

If you aren't interested in pulling down future updates,
then feel free to make any tweaks you'd like to make in the `apps` folder or any other code.


# Contributors

Thanks for your interest in contributing!

This project uses [`black`](https://github.com/psf/black) and [`isort`](https://pycqa.github.io/isort/) to maintain code style. Both of these tools are configured to run via [`pre-commit`](https://pre-commit.com/index.html). After installing `pre-commit` using your preferred method, install the git hooks for this repository.

```
pre-commit install
```

The first commit may take some time while `pre-commit` installs the hooks. Subsequent commits will be faster.

In addition, there is a Github action which will run these checks on any pull request.
