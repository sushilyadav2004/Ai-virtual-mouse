# AI Virtual Mouse

Proton is a Windows desktop assistant that combines a browser-based chat window, voice commands, and webcam-based hand gestures. It can move and click the mouse, scroll, and adjust system volume and brightness.

## Features

- Browser chat interface served locally with Eel.
- Voice commands using your microphone and speech recognition.
- Hand gesture control through your webcam.
- Mouse, scrolling, volume, and brightness controls.
- Web search, maps lookup, date/time responses, and basic file navigation.

## Requirements

- Windows 10 or 11.
- Python 3.10 or 3.11 recommended.
- A webcam and microphone.
- Google Chrome installed (the Eel app is configured to launch Chrome).
- Internet access for speech recognition and web searches.

## Setup

Open PowerShell in the project folder and run:

```powershell
cd src
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r ..\requirements.txt
```

If PowerShell blocks virtual environment activation, use this command for the current terminal session, then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

`SpeechRecognition` requires PyAudio for microphone input. It is included in `requirements.txt`; if its installation fails, install a compatible PyAudio wheel for your Python version and Windows architecture, then rerun the requirements installation.

## Run Proton

From the `src` folder, with the virtual environment active:

```powershell
python Proton.py
```

The program starts its local web server and opens the chat UI in Chrome at `http://localhost:27005/index.html`. Allow microphone and webcam access when prompted. Speak commands beginning with **“Proton”**, or type a command beginning with lowercase **“proton”** into the chat window.

For example:

- `proton what time is it`
- `proton search for weather`
- `proton launch gesture recognition`
- `proton stop gesture recognition`
- `proton exit`

To run only the hand gesture controller without the voice assistant or chat UI:

```powershell
python Gesture_Controller.py
```

Press **Enter** in the gesture controller window to stop it.

## Gesture controls

The standard gesture controller uses the right hand as the major hand by default.

| Gesture | Action |
| --- | --- |
| V sign | Enable click mode and move the cursor |
| Middle finger | Left-click while click mode is enabled |
| Index finger | Right-click while click mode is enabled |
| Two closed fingers | Double-click while click mode is enabled |
| Fist | Hold the left mouse button and move to drag |
| Pinch with the major/right hand | Adjust brightness horizontally and volume vertically |
| Pinch with the minor/left hand | Scroll horizontally or vertically |

Gesture detection requires good lighting and a webcam view of your hand. Gestures that control the mouse can interact with other applications, so close or pause the controller before typing sensitive information.

## Project layout

```text
src/
  Proton.py                   Main voice assistant and application entry point
  app.py                      Eel chat UI server and Python/browser bridge
  Gesture_Controller.py       Standard webcam hand gesture controller
  Gesture_Controller_Gloved.py Experimental marker/glove-based controller
  web/                        HTML, JavaScript, CSS, and UI images
  MyFirstApp/                 Separate .NET sample project
requirements.txt              Python dependencies
```

`Gesture_Controller_Gloved.py` is an experimental alternative and is not selected by the main application. It may require OpenCV's contrib modules and additional calibration images. The main application uses `Gesture_Controller.py`.

## Troubleshooting

- **Chrome does not open:** Install Chrome, then open `http://localhost:27005/index.html` manually while Proton is running.
- **Camera is unavailable:** Close other applications using the camera and check Windows camera privacy settings.
- **Microphone errors:** Check Windows microphone permissions and confirm PyAudio installed successfully.
- **Speech is not recognized:** Speak a clear command beginning with “Proton”; online recognition also requires internet access.
- **Volume or brightness controls fail:** Some displays do not expose software brightness controls. Run the program on Windows with access to the audio device and display.
- **Dependency installation errors:** Confirm that the active Python version is 3.10 or 3.11 and that the virtual environment is activated.

## Publishing to GitHub

After creating an empty repository on GitHub, run these commands from the project root (the folder containing this README):

```powershell
git init
git add README.md .gitignore requirements.txt src
git commit -m "Add Proton AI virtual mouse project"
git branch -M main
git remote add origin https://github.com/sushilyadav2004/new.git
git push -u origin main
```

The commands below target the public repository `https://github.com/sushilyadav2004/new`. GitHub will prompt you to authenticate if needed. Do not put passwords, access tokens, or other secrets in the repository or remote URL.
