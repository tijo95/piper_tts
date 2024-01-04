import subprocess
import time
import gradio as gr
from pathlib import Path
import json 
from modules import shared
import os
import re

settings_file = 'extensions/piper_tts/settings.json'

params = {
    "display_name": "Piper TTS",
    "active": True,
    "autoplay": True,
    "show_text": True,
    "quiet": False,
    "selected_model": "",
    "speaker_id": 0,
    "noise_scale": 0.667,
    "length_scale": 1.0,
    "noise_w": 0.8,
    "sentence_silence": 0.2,
    "ignore_asterisk_text": False,    
}

def load_settings():
    try:
        with open(settings_file, 'r') as json_file:
            settings = json.load(json_file)
            params.update(settings)
    except FileNotFoundError:
        pass

# Charge les paramètres depuis le fichier JSON au début du script
load_settings()

piper_path = Path('extensions/piper_tts/piper/piper.exe')
output_folder = Path('extensions/piper_tts/outputs')

def clean_text(text):
    cleaned_text = text
    
    replacements = {
        '&#x27;': "'",
        '&quot;': '"',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&nbsp;': ' ',
        '&copy;': '©',
        '&reg;': '®'
    }

    for key, value in replacements.items():
        cleaned_text = cleaned_text.replace(key, value)
        
    cleaned_text = cleaned_text.replace("***", "*").replace("**", "*")
    cleaned_text = re.sub(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", "", cleaned_text)
    
    # Ignorer le texte entre astérisques si l'option est activée
    if params["ignore_asterisk_text"]:
        while '*' in cleaned_text:
            start = cleaned_text.find('*')
            end = cleaned_text.find('*', start + 1)
            if start != -1 and end != -1 and start < end:
                excluded_text = cleaned_text[start:end + 1]
                cleaned_text = cleaned_text.replace(excluded_text, '')
  
    return cleaned_text


def tts(text, output_file):
    cleaned_text = clean_text(text)
    print(f"tts: {cleaned_text} -> {output_file}")

    selected_model = params.get('selected_model', '')
    model_path = Path(f'extensions/piper_tts/model/{selected_model}')
    
    output_file_path = output_folder / output_file
    output_file_str = output_file.as_posix()
    
    process = subprocess.Popen(
        [
            piper_path.as_posix(),
            '--sentence_silence', str(params['sentence_silence']),
            '--noise_scale', str(params['noise_scale']),
            '--length_scale', str(params['length_scale']),
            '--noise_w', str(params['noise_w']),
            '--speaker', str(params['speaker_id']),
            '--model', model_path.as_posix(),
            '--output_file', output_file_str,
            '--quiet' if params['quiet'] else '',
        ],
        stdin=subprocess.PIPE, 
        text=True
    )

    process.communicate(input=cleaned_text)

def output_modifier(string, state):

    if not params['active']:
        return string

    if string == '':
        string = '*Empty reply, try regenerating*'
    else:
        output_file = Path(f'extensions/piper_tts/outputs/{state["character_menu"]}_{int(time.time())}.wav')
        tts(string, output_file)
        autoplay = 'autoplay' if params['autoplay'] else ''
        html_string = f'<audio style="height: 30px;" src="file/{output_file.as_posix()}" controls {autoplay}></audio>'
        if params['show_text']:
            string = f'{html_string}\n\n{string}'
        else:
            string = html_string
    
    shared.processing_message = "*Is typing...*"
    return string

def history_modifier(history):
    if len(history['internal']) > 0:
        history['visible'][-1] = [
            history['visible'][-1][0],
            history['visible'][-1][1].replace('controls autoplay>', 'controls>')
        ]

    return history
    
def remove_directory():
    directory = Path('extensions/piper_tts/outputs')
    for file in directory.glob('*.wav'):
        file.unlink()    

def custom_update_selected_model(selected_model, model_folder):
    if selected_model:
        model_path = model_folder / selected_model
        params.update({'selected_model': selected_model, 'model_path': model_path})

def create_model_dropdown(model_folder):
    available_models = [model.name for model in model_folder.glob('*.onnx')]
    
    model_dropdown = gr.Dropdown(choices=available_models, label="Choose Model", value=params["selected_model"])
    
    def update_selected_model(selected_model):
        custom_update_selected_model(selected_model, model_folder)

    model_dropdown.change(update_selected_model, model_dropdown, None)

    return model_dropdown
    
def set_initial_model():
    model_folder = Path('extensions/piper_tts/model')
    available_models = [model.name for model in model_folder.glob('*.onnx')]

    load_settings()

    if not params["selected_model"] and available_models:
        initial_model = params.get("selected_model", available_models[0])
        
        params.update({
            "selected_model": initial_model,
            "active": params.get("active", True),
            "autoplay": params.get("autoplay", True),
            "show_text": params.get("show_text", True),
        })

# Appelle set_initial_model()
set_initial_model()

def save_settings():
    settings = {
        "active": params["active"],
        "autoplay": params["autoplay"],
        "show_text": params["show_text"],
        "quiet": params["quiet"],
        "selected_model": params["selected_model"],
        "speaker_id": params["speaker_id"],
        "noise_scale": params["noise_scale"],
        "length_scale": params["length_scale"],
        "noise_w": params["noise_w"],
        "sentence_silence": params["sentence_silence"],
        "ignore_asterisk_text": params["ignore_asterisk_text"],
    }

    with open(settings_file, 'w') as json_file:
        json.dump(settings, json_file, indent=4)
    
def ui():
    model_folder = Path('extensions/piper_tts/model')

    with gr.Accordion(params["display_name"], open=False):
    
        activate = gr.Checkbox(value=params['active'], label='Active extension')
        autoplay = gr.Checkbox(value=params['autoplay'], label='Play TTS automatically')
        show_text = gr.Checkbox(value=params['show_text'], label='Show message text under audio player')
        ignore_asterisk_checkbox = gr.Checkbox(value=params["ignore_asterisk_text"], label="*Ignore text inside asterisk*")
        quiet_checkbox = gr.Checkbox(value=False, label='Disable log')
        
        noise_scale_slider = gr.Slider(minimum=0.0, maximum=1.0, label=f'Noise Scale : Default (0.66)', value=params['noise_scale'])
        length_scale_slider = gr.Slider(minimum=0.0, maximum=2.0, label='Length Scale : Default (1)', value=params['length_scale'])
        noise_w_slider = gr.Slider(minimum=0.0, maximum=1.0, label='Noise Width : Default (0.8)', value=params['noise_w'])
        sentence_silence_slider = gr.Slider(minimum=0.0, maximum=1.0, label='Sentence Silence : Default (0.2)', value=params['sentence_silence'])
        
        activate.change(lambda x: params.update({'active': x}), activate, None)
        autoplay.change(lambda x: params.update({'autoplay': x}), autoplay, None)
        show_text.change(lambda x: params.update({'show_text': x}), show_text, None)
        ignore_asterisk_checkbox.change(lambda x: params.update({"ignore_asterisk_text": x}), ignore_asterisk_checkbox, None)
        quiet_checkbox.change(lambda x: params.update({'quiet': x}), quiet_checkbox, None)
        
        noise_scale_slider.change(lambda x: params.update({'noise_scale': x}), noise_scale_slider, None)
        length_scale_slider.change(lambda x: params.update({'length_scale': x}), length_scale_slider, None)
        noise_w_slider.change(lambda x: params.update({'noise_w': x}), noise_w_slider, None)
        sentence_silence_slider.change(lambda x: params.update({'sentence_silence': x}), sentence_silence_slider, None)
        
        # Utilise params["selected_model"] comme valeur initiale du menu déroulant
        model_dropdown = create_model_dropdown(model_folder)
        
        speaker_id_input = gr.Number(value=params["speaker_id"], label="Speaker ID : Default (0) See the model JSON file to find out which ID are available for the selected model.")
        speaker_id_input.change(lambda x: params.update({'speaker_id': int(x)}), speaker_id_input, None)
        
        with gr.Row():    
            save_button = gr.Button("Save Settings")
            save_button.click(save_settings, None)

            remove_directory_button = gr.Button("Remove WAV")
            remove_directory_button.click(remove_directory, None)

