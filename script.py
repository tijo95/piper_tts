import subprocess
import time
import gradio as gr
from pathlib import Path
import json 
from modules import shared
import os

settings_file = 'extensions/win_tts_piper/settings.json'

params = {
    "display_name": "Win tts piper",
    "active": True,
    "autoplay": True,
    "show_text": True,
    "selected_model": "",
    "noise_scale": 0.667,
    "length_scale": 1.0,
    "noise_w": 0.8,    
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

piper_path = Path('extensions/win_tts_piper/piper/piper.exe')
output_folder = Path('extensions/win_tts_piper/outputs')

def clean_text(text):
    cleaned_text = text
    cleaned_text = cleaned_text.replace('&#x27;', "'").replace('&quot;', '"')
    cleaned_text = cleaned_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    cleaned_text = cleaned_text.replace('&nbsp;', ' ').replace('&copy;', '©').replace('&reg;', '®')
    # Ajoutez d'autres remplacements au besoin
    return cleaned_text

def tts(text, output_file):
    cleaned_text = clean_text(text)
    print(f"tts: {cleaned_text} -> {output_file}")
    
    selected_model = params.get('selected_model', '')
    model_path = Path(f'extensions/win_tts_piper/model/{selected_model}')
    
    output_file_path = output_folder / output_file
    output_file_str = output_file.as_posix()
    
    process = subprocess.Popen(
        [
            piper_path.as_posix(),
            '--noise_scale', str(params['noise_scale']),
            '--length_scale', str(params['length_scale']),
            '--noise_w', str(params['noise_w']),
            '--model', model_path.as_posix(),
            '--output_file', output_file_str,
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
        output_file = Path(f'extensions/win_tts_piper/outputs/{state["character_menu"]}_{int(time.time())}.wav')
        tts(string, output_file)
        autoplay = 'autoplay' if params['autoplay'] else ''
        html_string = f'<audio src="file/{output_file.as_posix()}" controls {autoplay}></audio>'
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
    directory = Path('extensions/win_tts_piper/outputs')
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
    model_folder = Path('extensions/win_tts_piper/model')
    available_models = [model.name for model in model_folder.glob('*.onnx')]

    # Charge les paramètres depuis le fichier JSON
    load_settings()

    if available_models and not params["selected_model"]:
        # Utilise le modèle du fichier JSON si disponible
        initial_model = params.get("selected_model", available_models[0])
        params.update({
            "selected_model": initial_model,
            "active": True,
            "autoplay": True,
            "show_text": True
        })

# Appelle set_initial_model()
set_initial_model()

def save_settings():
    settings = {
        "active": params["active"],
        "autoplay": params["autoplay"],
        "show_text": params["show_text"],
        "selected_model": params["selected_model"],
        "noise_scale": params["noise_scale"],
        "length_scale": params["length_scale"],
        "noise_w": params["noise_w"],
    }

    with open(settings_file, 'w') as json_file:
        json.dump(settings, json_file, indent=4)
    

def ui():
    model_folder = Path('extensions/win_tts_piper/model')

    with gr.Accordion(params["display_name"], open=False):
    
        activate = gr.Checkbox(value=params['active'], label='Active extension')
        autoplay = gr.Checkbox(value=params['autoplay'], label='Play TTS automatically')
        show_text = gr.Checkbox(value=params['show_text'], label='Show message text under audio player')
        
        noise_scale_slider = gr.Slider(minimum=0.0, maximum=1.0, label=f'Noise Scale : Default (0.66)', value=params['noise_scale'])
        length_scale_slider = gr.Slider(minimum=0.0, maximum=2.0, label='Length Scale : Default (1)', value=params['length_scale'])
        noise_w_slider = gr.Slider(minimum=0.0, maximum=1.0, label='Noise Width : Default (0.8)', value=params['noise_w'])
        
        activate.change(lambda x: params.update({'active': x}), activate, None)
        autoplay.change(lambda x: params.update({'autoplay': x}), autoplay, None)
        show_text.change(lambda x: params.update({'show_text': x}), show_text, None)
        
        noise_scale_slider.change(lambda x: params.update({'noise_scale': x}), noise_scale_slider, None)
        length_scale_slider.change(lambda x: params.update({'length_scale': x}), length_scale_slider, None)
        noise_w_slider.change(lambda x: params.update({'noise_w': x}), noise_w_slider, None)
        
        # Utilise params["selected_model"] comme valeur initiale du menu déroulant
        model_dropdown = create_model_dropdown(model_folder)
        
        save_button = gr.Button("Save Settings")
        save_button.click(save_settings, None)

        remove_directory_button = gr.Button("Remove WAV Directory")
        remove_directory_button.click(remove_directory, None)

        gr.Row([model_dropdown, remove_directory_button])
