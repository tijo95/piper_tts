# win_tts_piper
Fast generation voice - piper oobabooga

This project is a Web user interface (WebUI) for text generation using Gradio and a Piper text-to-speech (TTS) model. The main objective is to provide a user-friendly experience for text generation with audio.

![Mon Image](https://drive.google.com/uc?export=view&id=1TOnHWGWDqHWgNNn6HFOfvEv9egC1z7g-) 
![Mon Image](https://drive.google.com/uc?export=view&id=16JkRmOfCL-E37Xe6V6jm7MJShZzNHTyr)


## Features

- Enable/Disable:** Enable or disable the TTS extension.
- Autoplay:** Choose to automatically read generated text.
- Text display:** Choose to show or hide generated text.
- Custom settings:** Adjust audio parameters such as noise, phoneme length and noise width.
- Template selection:** Choose from different templates available for text generation.
- WAV save:** Audio files are saved in the `outputs` folder.
- Save settings:** Save your settings. 
- Remove WAV:** delete all WAV files from the directory to free up storage space. 

## Saved settings

Selected settings are saved in a JSON file `settings.json` so that the user can retrieve his preferences each time he uses the device.

## Initial configuration

Make sure you install all necessary dependencies and configure your environment according to the project instructions.

## Installation

1. Clone the repository in the extensions directory.
   
```bash 
git clone https://github.com/tijo95/win_tts_piper.git
```

2. download the following windows piper repository: https://github.com/rhasspy/piper/releases/download/2023.9.27-1/piper_windows_amd64.zip

Unzip all contents into `win_tts_piper`

![Mon Image](https://drive.google.com/uc?export=view&id=1bO8QyVR7v7gwoLsUdXquTeZx5rEwF7EY)

3. Download the .onnx model and their .json files and place them in the repository win_tts_piper `model`.

    The models are available at this address: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0

4. Run the main script and have fun surprising your AI.

## Contributions

Contributions are welcome! Feel free to open an issue or propose an extraction request to improve this project.

## Piper Github

Github : https://github.com/rhasspy/piper#running-in-python

Listen to voice samples : https://rhasspy.github.io/piper-samples
