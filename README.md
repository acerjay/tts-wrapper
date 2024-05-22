
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
- PicoTTS
- SAPI (Microsoft Speech API)
- UWP (WinRT) Speech system (win 10+)

## Features
- **Text to Speech**: Convert text into spoken audio.
- **SSML Support**: Use Speech Synthesis Markup Language to enhance speech synthesis.
- **Voice and Language Selection**: Customize the voice and language for speech synthesis.
- **Streaming and Direct Play**: Stream audio or play it directly.
- **Pause, Resume, and Stop Controls**: Manage audio playback dynamically.
- **File Output**: Save spoken audio to files in various formats.
- **Unified Voice handling** Get Voices across all TTS engines with alike keys

## To-Do

- Add support for piper TTS
- Fix and do a better job of changing rate, volume etc (use getproperty and setProperty like pyttsx3)
- Add more tests and more logging code throughout. And exception handling
- look at https://github.com/synesthesiam/opentts/
- look at Orca
- check uwp. very quick untested write 

## Installation

```sh
pip install TTS-Wrapper
```

### Dependencies
Install additional dependencies based on the services you want to use:

```sh
pip install "TTS-Wrapper[google, watson, polly, elevenlabs, microsoft]"
```

For PicoTTS on Debian systems:

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

for a full demo see the examples folder. You'll need to fill out the credentials.json

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
client = GoogleClient(credentials='path/to/creds.json')

tts = GoogleTTS(client)
```

### Microsoft

```python
from tts_wrapper import MicrosoftTTS, MicrosoftClient
client = MicrosoftClient(credentials='subscription_key',region='subscription_region')

tts = MicrosoftTTS(client)
```

### Watson

```python
from tts_wrapper import WatsonTTS, WatsonClient
client = WatsonClient(credentials=('api_key', 'api_url'))

tts = WatsonTTS(client)
```

### ElevenLabs

```python
from tts_wrapper import ElevenLabsTTS, ElevenLabsClient
client = ElevenLabsClient(credentials=('api_key'))
tts = ElevenLabsTTS(client)
```

### UWP

```python
from tts_wrapper import UWPTTS, UWPClient
client = UWPClient()
tts = UWPTTS(client)
```

You then can perform the following methods.

## Advanced Usage

### SSML

Even if you don't use SSML features that much its wise to use the same syntax - so pass SSML not text to all engines

```python
ssml_text = tts.ssml.add('Hello world!')
```

### Speak 

This will use the default audio output of your device to play the audio immediatley

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

Note only **Polly, Microsoft and Watson** can do this. We can't do this in anything else

```python
def my_callback(word: str, start_time: float):
        print(f'Word "{word}" spoken at {start_time} ms')

text = "Hello, This is a word timing test"
ssml_text = tts.ssml.add(text)
tts.start_playback_with_callbacks(ssml_text, callback=my_callback)
```

and it will output

```bash
Word "Hello" spoken at 0.05 ms
Word "," spoken at 0.65 ms
Word "This" spoken at 0.7125 ms
Word "is" spoken at 0.8875 ms
Word "a" spoken at 1.0 ms
Word "word" spoken at 1.0875 ms
Word "timing" spoken at 1.3625 ms
Word "test" spoken at 1.7375 ms
```

#### PicoTTS & SAPI

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

## License

This project is licensed under the [MIT License](./LICENSE).
