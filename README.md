# Discrete event LSL stream viewer for Python
Online viewer for Lab Streaming Layer (LSL) events in discrete and continuous streams in Pyhton.
## Installation
* Prerequisites
  * PyQt: set of Python v2 and v3 bindings for the Qt application framework. Normally, they come by default with a default Qt installation.
  * [`liblsl`](https://github.com/sccn/labstreaminglayer/wiki/INSTALL) built from source code.
  * [`pylsl`](https://labstreaminglayer.readthedocs.io/dev/app_dev.html#python-apps): Python interface to the Lab Streaming Layer (LSL).
* Download and copy the files to the Lab Streaming Layer directory in your computer.
* (Optional) To allow the keyboard shortcuts (variation of time range, scaling), install the [`keyboard`](https://pypi.org/project/keyboard/) module for Python

## Usage
* Start a LSL stream by linking a device with the computer with its corresponding application. 
* Run `viewer.py`. A Dialog where the user can choose between the different available streams in order to display their associated events will appear. Select the desired streams and press OK.
* A new window with the event viewer will appear.

###### 
