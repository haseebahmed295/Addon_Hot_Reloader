# Addon Hot Reloader

A Blender addon that automatically reloads a specific addon after a set time.

## Description

The Addon Hot Reloader is a development tool for Blender that allows developers to automatically reload their addons at specified intervals without manually restarting Blender or manually reloading the addon. This significantly speeds up the addon development process by eliminating the need for repetitive manual reloading.

## Features

- Automatic reloading of selected addons at customizable time intervals
- UI panel in the 3D Viewport for easy configuration
- Option to reload submodules of the addon
- Start/stop timer functionality
- Integration with Blender's top bar menu for quick access
- Error handling with informative reporting

## Requirements

- Blender 3.6.0 or higher (may work with earlier versions not tested)

## Installation

1. Download or clone this repository
2. In Blender, go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the downloaded folder
4. Enable the addon by checking the box next to "Development: Addon Hot Reloader"

## Usage

Warning: This addon tries to even if addon operator is still running.It can crash blender.

1. After installation, you'll find a "Hot Reloader" panel in the 3D Viewport sidebar (press `N` to toggle sidebar)
2. Select the addon you want to reload from the dropdown menu
3. Set the time interval (in seconds) for automatic reloading
4. Choose whether to reload submodules
5. Click "Start Timer" to begin the automatic reloading process
6. To stop the timer, click the "Stop Timer" button

You can also access the timer controls from the top bar menu in Blender.

## How It Works

The Addon Hot Reloader works by:

1. Using Blender's timer system to trigger reload events at specified intervals
2. Unregistering the target addon before reloading to prevent conflicts
3. Using Python's `importlib.reload()` function to reload the addon module
4. Optionally reloading submodules recursively for complex addons
5. Re-registering the addon after reload

The addon includes error handling to catch exceptions during the unregister/register process and provides informative feedback to the user.

## Examples

### Basic Usage

1. Set up the addon in the 3D Viewport panel:
   - Select an addon to reload from the dropdown
   - Set time interval to 5 seconds
   - Click "Start Timer"

2. Modify your addon code and save the files

3. The addon will automatically reload every 5 seconds, incorporating your changes

### Advanced Usage

Enable "Reload Submodules" for addons with code base on seperate files.

