
# TTS-Wrapper

[![PyPI version](https://badge.fury.io/py/tts-wrapper.svg)](https://badge.fury.io/py/tts-wrapper)
![build](https://github.com/mediatechlab/tts-wrapper/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/mediatechlab/tts-wrapper/branch/master/graph/badge.svg?token=79IG7GAK0B)](https://codecov.io/gh/mediatechlab/tts-wrapper)
[![Maintainability](https://api.codeclimate.com/v1/badges/b327dda20742c054bcf0/maintainability)](https://codeclimate.com/github/mediatechlab/tts-wrapper/maintainability)

> **Contributions are welcome! Check our [contribution guide](./CONTRIBUTING.md).**

_TTS-Wrapper_ simplifies using text-to-speech APIs by providing a unified interface across multiple services, allowing easy integration and manipulation of TTS capabilities.

## Supported Services

- AWS Polly
- Google TTS
- Microsoft Azure TTS
- IBM Watson
- ElevenLabs
- Wit.Ai 

### Experimental (Not fully featured or in a state of WIP)

- PicoTTS
- SAPI (Microsoft Speech API)
- UWP (WinRT) Speech system (win 10+)
- Piper TTS (experimental and Linux Only)
- MMS ([Massively Multilingual Speech from Meta](https://ai.meta.com/blog/multilingual-model-speech-recognition/)) 

## Features
- **Text to Speech**: Convert text into spoken audio.
- **SSML Support**: Use Speech Synthesis Markup Language to enhance speech synthesis.
- **Voice and Language Selection**: Customize the voice and language for speech synthesis.
- **Streaming and Direct Play**: Stream audio or play it directly.
- **Pause, Resume, and Stop Controls**: Manage audio playback dynamically.
- **File Output**: Save spoken audio to files in various formats.
- **Unified Voice handling** Get Voices across all TTS engines with alike keys

## To-Do

- Improve the implementation of changing rate, volume, etc. (work in progress). This is a priority. 
    - Add more tests and logging code for better debugging and exception handling.
- Verify the functionality of UWP (Universal Windows Platform).
- Investigate other audio engines. PyAudio is a pain to install on windows
- Look at Piper. The speed is wierd. It needs to be feature full

and an aside

- Explore the possibilities of using libraries like [OpenTTS](https://github.com/synesthesiam/opentts/) and [Orca](https://github.com/synesthesiam/orca).

### Using pip

```sh
pip install tts-wrapper[google, watson, polly, elevenlabs, microsoft, mms]
```

NB: On Mac you may need to do 

```sh
pip install tts-wrapper"[google, watson, polly, elevenlabs, microsoft, mms]"
```

You will need to install `portaudio19-dev` on Linux

If you are *only* getting voices you can use the optional extra `no_playback`. It will skip trying to install pyaudio as you wont need it. eg 

```sh
pip install tts-wrapper"[no_playback, google, watson, polly, elevenlabs, microsoft, mms]"
```

### Using pip - detailed

1. Clone the repository:
   ```sh
   git clone https://github.com/mediatechlab/tts-wrapper.git
   cd tts-wrapper
   ```

2. Install the package and system dependencies:
   ```sh
   pip install .
   ```

   To install optional dependencies, use:
   ```sh
   pip install .[google, watson, polly, elevenlabs, microsoft]
   ```

This will install Python dependencies and system dependencies required for this project. Note that system dependencies will only be installed automatically on Linux.

### Using Poetry

1. Clone the repository:
   ```sh
   git clone https://github.com/mediatechlab/tts-wrapper.git
   cd tts-wrapper
   ```

2. Install Python dependencies:
   ```sh
   poetry install
   ```

3. Install system dependencies (Linux only):
   ```sh
   poetry run postinstall
   ```

4. Run your project:
   ```sh
   poetry run python your_project_script.py
   ```

## System Dependencies

This project requires the following system dependencies on Linux:

- `portaudio19-dev`

You can install these dependencies using the provided setup script or manually with the appropriate package manager (e.g., `apt-get` for Debian-based systems). The setup script will only run on Linux systems.


### For PicoTTS on Debian systems:

```sh
sudo apt-get install libttspico-utils
```

## Basic Usage

```python
from tts_wrapper import PollyClient
pollyClient = PollyClient(credentials=('aws_key_id', 'aws_secret_access_key'))

from tts_wrapper import PollyTTS

tts = PollyTTS(pollyClient)
ssml_text = tts.ssml.add('Hello, <break time="500ms"/> world!')
tts.speak(ssml_text)
```

You can use SSML or plain text

```python
from tts_wrapper import PollyClient
pollyClient = PollyClient(credentials=('aws_key_id', 'aws_secret_access_key'))
from tts_wrapper import PollyTTS

tts = PollyTTS(pollyClient)
tts.speak('Hello world')
```

for a full demo see the examples folder. You'll need to fill out the credentials.json (or credentials-private.json). Use them from cd'ing into the examples folder. 
Tips on gaining keys are below.

## Authorization
Each service uses different methods for authentication:

### Polly

```python
from tts_wrapper import PollyTTS, PollyClient
client = PollyClient(credentials=('aws_region','aws_key_id', 'aws_secret_access_key'))

tts = PollyTTS(client)
```

### Google

```python
from tts_wrapper import GoogleTTS, GoogleClient
client = GoogleClient(credentials=('path/to/creds.json'))

tts = GoogleTTS(client)
```

### Microsoft

```python
from tts_wrapper import MicrosoftTTS, MicrosoftClient
client = MicrosoftClient(credentials=('subscription_key','subscription_region'))

tts = MicrosoftTTS(client)
```

### Watson

```python
from tts_wrapper import WatsonTTS, WatsonClient
client = WatsonClient(credentials=('api_key', 'region', 'instance_id'))

tts = WatsonTTS(client)
```

### ElevenLabs

```python
from tts_wrapper import ElevenLabsTTS, ElevenLabsClient
client = ElevenLabsClient(credentials=('api_key'))
tts = ElevenLabsTTS(client)
```

- **Note**: ElevenLabs does not support SSML.

### Wit.Ai

```python
from tts_wrapper import WitAiTTS, WitAiClient
client = WitAiClient(credentials=('token'))
tts = WitAiTTS(client)
```

### UWP

```python
from tts_wrapper import UWPTTS, UWPClient
client = UWPClient()
tts = UWPTTS(client)
```

### Piper

```python
from tts_wrapper import PiperTTS, PiperClient
client = PiperClient()
tts = PiperTTS(client)
```

- **Note:** Piper is experimental and only works on Linux only right now. Please also note SSML is not supported so SSML tags will just be rendered as text.

### MMS

```python
from tts_wrapper import MMSTTS, MMSClient


client = MMSClient((model_dir,lang))
tts = MMSTTS(client)

```

- model_dir can be None - and it will create one for you in ~/mms_models
- you can just provide a lang code. See lang codes (and TTS supported) at https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html

eg. 


```python
from tts_wrapper import MMSTTS, MMSClient


client = MMSClient((None, 'spa'))
tts = MMSTTS(client)
text = "Hola, este es mms hablando en español"
tts.speak(text)

```

or 

```python
from tts_wrapper import MMSTTS, MMSClient


client = MMSClient(('spa'))
tts = MMSTTS(client)
text = "Hola, este es mms hablando en español"
tts.speak(text)

```
or 

```python

from tts_wrapper import MMSTTS, MMSClient
import json
import time
from pathlib import Path
import os

# Initialize the client with custom model_dir and lang parameters
custom_model_dir = "/path/to/custom_model_dir"
custom_lang = "spa"
client_custom = MMSClient((custom_model_dir, custom_lang))
tts_custom = MMSTTS(client_custom)
text_custom = "Hola, este es mms hablando en español"
tts_custom.speak(text_custom)
```

- **Note:** MMS is WIP. It could break, and aspects like SSML aren't supported. 


You then can perform the following methods.

## Advanced Usage

### SSML

Even if you don't use SSML features that much its wise to use the same syntax - so pass SSML not text to all engines

```python
ssml_text = tts.ssml.add('Hello world!')
```

### Plain Text

If you want to keep things simple each engine will convert plain text to SSML if its not.

```python
tts.speak('Hello World!')
```

### Speak 

This will use the default audio output of your device to play the audio immediately

```python
tts.speak(ssml_text)
```

### Streaming and Playback Control

```python
tts.speak_streamed(ssml_text)

tts.pause_audio()
tts.resume_audio()
tts.stop_audio()
```

here's an example of this in use

```python
ssml_text = tts.ssml.add('Hello world!')

tts.speak_streamed(ssml_text)
input("Press enter to pause...")
tts.pause_audio()
input("Press enter to resume...")
tts.resume_audio()
input("Press enter to stop...")
tts.stop_audio()
```

### File Output

```python
tts.synth_to_file(ssml_text, 'output.mp3', format='mp3')
```
there is also "synth" method which is legacy

```Python
tts.synth('<speak>Hello, world!</speak>', 'hello.mp3', format='mp3)
```

### Fetch Available Voices

```python
voices = tts.get_voices()
print(voices)
```

NB: All voices will have a id, dict of language_codes, name and gender. Just note not all voice engines provide gender

### Voice Selection

```python
tts.set_voice(voice_id,lang_code=en-US)
```

e.g.

```python
tts.set_voice('en-US-JessaNeural','en-US')
```

Use the id - not a name

### SSML

```python
ssml_text = tts.ssml.add('Hello, <break time="500ms"/> world!')
tts.speak(ssml_text)
```

### Using callbacks on word level boundaries

Note only **Polly, Microsoft, Google, UWP, SAPI and Watson** can do this **correctly**. We can't do this in anything else but we do do a estimated tonings for all other engines (ie elevenlabs, witAi and Piper)

```python
def my_callback(word: str, start_time: float):
    print(f'Word "{word}" spoken at {start_time} ms')

def on_start():
    print('Speech started')

def on_end():
    print('Speech ended')

try:
    text = "Hello, This is a word timing test"
    ssml_text = tts.ssml.add(text)
    tts.connect('onStart', on_start)
    tts.connect('onEnd', on_end)
    tts.start_playback_with_callbacks(ssml_text, callback=my_callback)
except Exception as e:
    print(f"Error: {e}")
```

and it will output

```bash
Speech started
Word "Hello" spoken at 0.05 ms
Word "," spoken at 0.65 ms
Word "This" spoken at 0.7125 ms
Word "is" spoken at 0.8875 ms
Word "a" spoken at 1.0 ms
Word "word" spoken at 1.0875 ms
Word "timing" spoken at 1.3625 ms
Word "test" spoken at 1.7375 ms
Speech ended
```

#### PicoTTS, SAPI & UWP

These clients dont't require authorization since they run offline.

```python
from tts_wrapper import PicoClient, SAPIClient
client = PicoClient()
# or
client = SAPIClient()
```

## Supported File Formats

By default, all engines output audio in the WAV format, but can be configured to output MP3 or other formats where supported.

```Python
tts.synth('<speak>Hello, world!</speak>', 'hello.mp3', format='mp3)
```


## Developer's Guide: Adding a New Engine to TTS Wrapper

This guide provides a step-by-step approach to adding a new engine to the existing Text-to-Speech (TTS) wrapper system.

### Step 1: Create Engine Directory Structure

1. **Create a new folder** for your engine within the `engines` directory. Name this folder according to your engine, such as `witai` for Wit.ai.

   Directory structure:
   ```
   engines/witai/
   ```

2. **Create necessary files** within this new folder:
   - `__init__.py` - Makes the directory a Python package.
   - `client.py` - Handles all interactions with the TTS API.
   - `engine.py` - Contains the TTS class that integrates with your abstract TTS system.
   - `ssml.py` - Defines any SSML handling specific to this engine.

   Final directory setup:
   ```
   engines/
   └── witai/
       ├── __init__.py
       ├── client.py
       ├── engine.py
       └── ssml.py
   ```

### Step 2: Implement Client Functionality in `client.py`

Implement authentication and necessary setup for API connection. This file should manage tasks such as sending synthesis requests and fetching available voices.

```python
class TTSClient:
    def __init__(self, api_key):
        self.api_key = api_key
        # Setup other necessary API connection details here

    def synth(self, text, options):
        # Code to send a synthesis request to the TTS API
        pass

    def get_voices(self):
        # Code to retrieve available voices from the TTS API
        pass
```

### Step 3: Define the TTS Engine in `engine.py`

This class should inherit from the abstract TTS class and implement required methods such as `get_voices` and `synth_to_bytes`.

```python
from .client import TTSClient
from your_tts_module.abstract_tts import AbstractTTS

class WitTTS(AbstractTTS):
    def __init__(self, api_key):
        super().__init__()
        self.client = TTSClient(api_key)

    def get_voices(self):
        return self.client.get_voices()

    def synth_to_bytes(self, text, format='wav'):
        return self.client.synth(text, {'format': format})
```

### Step 4: Implement SSML Handling in `ssml.py`

If the engine has specific SSML requirements or supports certain SSML tags differently, implement this logic here.

```python
from your_tts_module.abstract_ssml import BaseSSMLRoot, SSMLNode

class EngineSSML(BaseSSMLRoot):
    def add_break(self, time='500ms'):
        self.root.add(SSMLNode('break', attrs={'time': time}))
```

### Step 5: Update `__init__.py`

Make sure the `__init__.py` file properly imports and exposes the TTS class and any other public classes or functions from your engine.

```python
from .engine import WitTTS
from .ssml import EngineSSML
```


## Tips

### Getting keys

#### Watson

This is not straightforward

#### Polly

#### Microsoft 

#### Google

1. 

#### Wit.Ai

1. https://wit.ai/apps
2. Look for `Bearer` token. Its in the Curl example

#### ElevenLabs

1. Login at https://elevenlabs.io/app/speech-synthesis
2. Go to your profile and click on "Profile + API Key"
3. Click on Popup and copy "API Key"

## License

This project is licensed under the [MIT License](./LICENSE).
