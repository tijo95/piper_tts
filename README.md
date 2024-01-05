# piper_tts
An extension for the [text-generation-webui by oobabooga](https://github.com/oobabooga/text-generation-webui) that uses [Piper](https://github.com/rhasspy/piper) for fast voice generation.

This project is a Web user interface (WebUI) for text generation using Gradio and a Piper text-to-speech (TTS) model. The main objective is to provide a user-friendly experience for text generation with audio.

![Mon Image](https://drive.google.com/uc?export=view&id=1TOnHWGWDqHWgNNn6HFOfvEv9egC1z7g-) 


## Features

- 16/11/2023 -- Speaker ID :** Some model may contain several voices, so to find out which ID to use, refer to the model's JSON file.
- 16/11/2023 -- Sentence silence :** allows you to specify the duration, in seconds, of silence to be added after each sentence during text-to-speech.
- Enable/Disable :** Enable or disable the TTS extension.
- Autoplay :** Choose to automatically read generated text.
- Text display :** Choose to show or hide generated text.
- Custom settings :** Adjust audio parameters such as noise, phoneme length and noise width.
- Template selection :** Choose from different templates available for text generation.
- WAV save :** Audio files are saved in the `outputs` folder.
- Save settings :** Save your settings. 
- Remove WAV :** delete all WAV files from the directory to free up storage space. 

## Saved settings

Selected settings are saved in a JSON file `settings.json` so that the user can retrieve his preferences each time he uses the device.

## Initial configuration

Make sure you install all necessary dependencies and configure your environment according to the project instructions.

## Installation

1. Clone the repository in the extensions directory.
   
```bash 
git clone https://github.com/tijo95/piper_tts.git
```


2. download the appropriate binay for your platform from piper repository:

For windows, download `https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip`
Unzip all contents into `piper_tts`

![Mon Image](https://drive.google.com/uc?export=view&id=1bO8QyVR7v7gwoLsUdXquTeZx5rEwF7EY)

For linux:
```bash
cd piper_tts/
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xvf piper_linux_x86_64.tar.gz
rm piper_linux_x86_64.tar.gz 
```

3. Download the .onnx model and their .json files and place them in the `piper_tts/model` directory.

    The models are available at this address: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0

   ![Mon Image](https://drive.google.com/uc?export=view&id=16JkRmOfCL-E37Xe6V6jm7MJShZzNHTyr)
   

5. Run the main script and have fun surprising your AI.

## Contributions

Contributions are welcome! Feel free to open an issue or propose an extraction request to improve this project.

## Piper Github

Github : https://github.com/rhasspy/piper#running-in-python

Listen to voice samples : https://rhasspy.github.io/piper-samples
