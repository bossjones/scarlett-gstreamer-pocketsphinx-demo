#!/usr/bin/env python

import sys
import os

# insert path so we can access things w/o having to re-install everything
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

PWD = os.path.dirname(os.path.abspath(__file__))

print PWD

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import threading

# Here's where you edit the vocabulary.
# Point these variables to your *.lm and *.dic files. A default exists,
# but new models can be created for better accuracy. See instructions at:
# http://cmusphinx.sourceforge.net/wiki/tutoriallm
LM_PATH = "{}/1602.lm".format(PWD)
DICT_PATH = "{}/9812.dic".format(PWD)
HMM_PATH = "{}/hmm/en_US/hub4wsj_sc_8k".format(PWD)
ps_device = 'hw:1'
silprob = 0.1
wip = 1e-4
bestpath = 0

# ps_lm = "{}/1602.lm".format(PWD)
# ps_dict = "{}/9812.dic".format(PWD)
# ps_hmm = "{}/hmm/en_US/hub4wsj_sc_8k".format(PWD)

parse_launch_array = [
                'alsasrc device=' +
                ps_device,
                'queue silent=false leaky=2 max-size-buffers=0 max-size-time=0 max-size-bytes=0',  # noqa
                'audioconvert',
                'audioresample',
                'audio/x-raw-int, rate=16000, width=16, depth=16, channels=1',
                'audioresample',
                'audio/x-raw-int, rate=8000',
                'vader name=vad auto-threshold=true',
                'pocketsphinx name=asr',
                'fakesink dump=1']

# Initialize GST
GObject.threads_init()
Gst.init(None)


def asr_partial_result(asr, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio.
    """
    print "ASR partial", uttid, ":", text


def asr_result(asr, text, uttid):
    """ This function is called when pocketsphinx gets a
        full result (spoken command with a pause)
    """
    print "ASR result", uttid, ":", text

# This sets up our pipeline from pulseaudio (input)
# through the vader and into pocketsphinx.
# pipeline = Gst.parse_launch('pulsesrc ! audioconvert ! audioresample '
#                             + '! vader name=vad auto-threshold=true '
#                             + '! pocketsphinx name=asr ! fakesink')
pipeline = Gst.parse_launch(
    ' ! '.join(parse_launch_array))

# Connect our callbacks to pocketsphinx
asr = pipeline.get_by_name('asr')
asr.connect('partial_result', asr_partial_result)
asr.connect('result', asr_result)

# Optional: set the language model and dictionary.
if LM_PATH and DICT_PATH:
    asr.set_property('lm', LM_PATH)
    asr.set_property('dict', DICT_PATH)
    asr.set_property('hmm', DICT_PATH)

# Now tell gstreamer and pocketsphinx to start converting speech!
asr.set_property('configured', True)
pipeline.set_state(Gst.State.PLAYING)

# This loops the program until Ctrl+C is pressed
g_loop = threading.Thread(target=GObject.MainLoop().run)
g_loop.daemon = False
g_loop.start()
