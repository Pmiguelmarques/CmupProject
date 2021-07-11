# PerSpy

PerSpy is an application that is directed to capture the movements of the user, directed for software development, offering also an extension that blocks the potentially distracting websites.

## Installation

```bash
$ python --version
3.9.6
```

### Create a virtual environment ###

```bash
$ python -m venv env

$ source env/bin/activate
```

### Install the packages ### 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements needed for the application.

```bash
$ pip install -r requirements.txt
```
### Load the extension ###

The extension is only suported in Chrome.
To load the extension in the browser:
- Got to Chrome Extensions Page, in chrome://extensions
- Enable developer mode
- Click in Load unpacked extension and select the folder of the extension.
- The extension should be added and it should be running by now.

## Usage

```bash
# run coordinator
python coordinator.py

# run inputMonitor
python inputMonitor.py
```
The extension connects automatically to the coordinator. 👍

## License
[MIT](https://github.com/Pmiguelmarques/CmupProject/blob/main/LICENSE)
