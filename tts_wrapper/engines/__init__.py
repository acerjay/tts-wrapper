import sys
from .google import *
from .microsoft import *
from .pico import *
from .polly import *
from .sapi import *
from .watson import *
from .elevenlabs import *
from .uwp import *
from .witai import *
from .mms import *
from .sherpaonnx import *
from .googleTrans import *
if sys.platform == "linux":
    from .piper import *
