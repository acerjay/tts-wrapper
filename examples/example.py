# if running within the project dir
# export PYTHONPATH="/Users/willwade/GitHub/tts-wrapper:$PYTHONPATH"
# python examples/example.py
import sys
import json
import logging
from pathlib import Path
from tts_wrapper import PollyTTS, PollyClient, MicrosoftTTS, MicrosoftClient, WatsonTTS, WatsonClient, GoogleTTS, GoogleClient, ElevenLabsTTS, ElevenLabsClient,  WitAiTTS, WitAiClient, SherpaOnnxTTS, SherpaOnnxClient
import signal
import sys
import time
import os
import types
from load_credentials import load_credentials


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def create_tts_client(service):
    if service == "polly":
        region = os.getenv('POLLY_REGION')
        aws_key_id = os.getenv('POLLY_AWS_KEY_ID')
        aws_access_key = os.getenv('POLLY_AWS_ACCESS_KEY')
        client = PollyClient(credentials=(region, aws_key_id, aws_access_key))
        tts = PollyTTS(client=client, voice='Joanna')
    elif service == "microsoft":
        token = os.getenv('MICROSOFT_TOKEN')
        region = os.getenv('MICROSOFT_REGION')
        client = MicrosoftClient(credentials=(token, region))
        tts = MicrosoftTTS(client=client)
    elif service == "watson":
        api_key = os.getenv('WATSON_API_KEY')
        region = os.getenv('WATSON_REGION')
        instance_id = os.getenv('WATSON_INSTANCE_ID')
        client = WatsonClient(credentials=(api_key, region, instance_id))
        tts = WatsonTTS(client=client)
    elif service == "google":
        creds_path = os.getenv('GOOGLE_CREDS_PATH')
        client = GoogleClient(credentials=creds_path)
        tts = GoogleTTS(client=client)
    elif service == "elevenlabs":
        api_key = os.getenv('ELEVENLABS_API_KEY')
        client = ElevenLabsClient(credentials=api_key)
        tts = ElevenLabsTTS(client=client)
    elif service == "witai":
        api_key = os.getenv('WITAI_TOKEN')
        client = WitAiClient(credentials=(api_key))
        tts = WitAiTTS(client=client)
    elif service == "mms":
        client =  MMSClient(('spa'))
        tts = MMSTTS(client)
    elif service == "sherpaonnx":
        client = SherpaOnnxClient(model_path=None, tokens_path=None)
        tts = SherpaOnnxTTS(client)
    elif service == "watson":
        api_key = os.getenv('WATSON_API_KEY')
        region = os.getenv('WATSON_REGION')
        instance_id = os.getenv('WATSON_INSTANCE_ID')
        client = WatsonClient(credentials=(api_key, region, instance_id))
        tts = WatsonTTS(client=client)
    else:
        raise ValueError("Unsupported TTS service")
    return tts
    
def test_tts_engine(tts, service_name):

    text_read = 'Hello, world! This is a text of plain text sending'
    try:
        print(f"Testing {service_name} TTS engine...in a plain text demo")
        tts.speak_streamed(text_read)            
    except Exception as e:
        print(f"Error testing {service_name} TTS engine at speak with plain text: {e}")
        
    try:
        text_read = 'Hello, world!'
        text_with_prosody = tts.construct_prosody_tag(text_read)    
        
        tts.ssml.clear_ssml()
        ssml_text = tts.ssml.add(text_with_prosody)  # Assuming there's a method to add SSML correctly
       
        try:
            print(f"Testing {service_name} TTS engine...volume control")
            tts.speak_streamed(ssml_text)

            time.sleep(3)
            tts.ssml.clear_ssml()

            tts.set_property("volume","90")
            tts.set_property("pitch","x-high")
            
            text_read_2 = "This is louder than before"

            text_with_prosody = tts.construct_prosody_tag(text_read_2)
            time.sleep(0.5)
            ssml_text = tts.ssml.add(text_with_prosody)

            #print ("Testing setting volume to 90")
            print ("Testing setting volume to extra loud")
            tts.speak_streamed(ssml_text)
        
            time.sleep(1)
            
        except Exception as e:
            print(f"Error testing {service_name} TTS engine at speak_streamed (58-75): {e}")
        

    except Exception as e:
        print(f"Error testing {service_name} TTS engine: {e}")

    tts.ssml.clear_ssml()
    ssml_text = tts.ssml.add('Lets save to an audio file')  
    # Demonstrate saving audio to a file
    output_file = Path(f"output_{service_name}.wav")
    tts.synth(ssml_text, str(output_file))
    # or you could do
    #tts.speak(ssml_text)
    print(f"Audio content saved to {output_file}")

    # Change voice and test again if possible
    voices = tts.get_voices()
    print('Getting voices')
    for voice in voices[:4]:  # Show details for first four voices
        language_codes = voice.get('language_codes', [])
        display_name = voice.get('name', 'Unknown voice')
        # Safely get the first language code, default to 'Unknown' if not available
        first_language_code = language_codes[0] if language_codes else 'Unknown'
        print(f"{display_name} ({first_language_code}): {voice['id']}")
    # Change voice if more than one is available
    if len(voices) > 1:
        new_voice_id = voices[1].get('id')
        # Attempt to get the first language from the second voice's language codes
        new_lang_codes = voices[1].get('language_codes', [])
        new_lang_id = new_lang_codes[0] if new_lang_codes else 'Unknown'
        print(f"Running with {new_voice_id} and {new_lang_id}")
        tts.set_voice(new_voice_id, new_lang_id)
        ssml_text_part2 = tts.ssml.add('Continuing with a new voice!')
        tts.speak_streamed(ssml_text_part2)

def main():
    service = sys.argv[1] if len(sys.argv) > 1 else "all"
    # Load credentials
    load_credentials('credentials-private.json')
    services = ["elevenlabs", "google", "microsoft", "mms", "polly", "watson", "witai"] if service == "all" else [service]
    for svc in services:
        print(f"Testing {svc.upper()} TTS engine.")
        tts = create_tts_client(svc)
        #microsoft test with absolute value
        #tts.set_property("volume", "20")

        #google test with predefined words or decibels
        tts.set_property("volume", "5")
        tts.set_property("rate", "x-slow")
        tts.set_property("pitch", "x-low")
        test_tts_engine(tts, svc)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
