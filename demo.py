#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from IPython.core.debugger import Tracer
from IPython.core import ultratb

sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                     color_scheme='Linux',
                                     call_pdb=True,
                                     ostream=sys.__stdout__)

from colorlog import ColoredFormatter

import logging


def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "(%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        },
        secondary_log_colors={
            'message': {
                'ERROR':    'red',
                'CRITICAL': 'red',
                'DEBUG': 'yellow'
            }
        },
        style='%'
    )

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


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

# old pocketsphinx launch array
use_legacy_parse_launch = False

if use_legacy_parse_launch:
    parse_launch_array = ['alsasrc device=' +
           ps_device,
           'queue silent=false leaky=2 max-size-buffers=0 max-size-time=0 max-size-bytes=0',  # noqa
           'audioconvert',
           'audioresample',
           'audio/x-raw-int, rate=16000, width=16, depth=16, channels=1',
           'audioresample',
           'audio/x-raw-int, rate=8000',
           'pocketsphinx name=asr',
           'fakesink dump=1']
else:
    # source:
    # https://github.com/smartin015/gstreamer_pocketsphinx_demo/blob/master/demo.py
    # parse_launch_array = ['pulsesrc ! audioconvert ! audioresample '
    #                       + '! vader name=vad auto-threshold=true '
    #                       + '! pocketsphinx name=asr ! fakesink']

    # source: pocketsphinx upstream
    # http://webcache.googleusercontent.com/search?q=cache:W7uIWyLxLDAJ:cmusphinx.sourceforge.net/wiki/gstreamer+&cd=2&hl=en&ct=clnk&gl=us
    parse_launch_array = ['autoaudiosrc ! audioconvert ! audioresample '
                          + '! pocketsphinx name=asr ! fakesink']

# Initialize GST
GObject.threads_init()
Gst.init(None)

gst = Gst

global logger
logger = setup_logger()


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


def asr_element_message(asr, bus, msg):
    """Receive element messages from the bus."""
    logger.debug("msg: " + msg)
    logger.debug("msg.get_structure(): " + msg.get_structure())
    msgtype = msg.get_structure().get_name()
    if msgtype != 'pocketsphinx':
        return

    if msg.get_structure()['final']:
        asr.final_result(msg.get_structure()['hypothesis'],
                         msg.get_structure()['confidence'])
        asr.pipeline.set_state(gst.State.PAUSED)
    elif msg.get_structure()['hypothesis']:
        asr.partial_result(msg.get_structure()['hypothesis'])


def partial_result(asr, hyp):
    """Delete any previous selection, insert text and select it."""
    logger.debug("hyp: " + hyp)


def final_result(asr, hyp, confidence):
    """Insert the final result."""
    logger.debug("hyp: " + hyp)
    logger.debug("confidence: " + confidence)

# This sets up our pipeline from pulseaudio (input)
# through the vader and into pocketsphinx.
# pipeline = Gst.parse_launch('pulsesrc ! audioconvert ! audioresample '
#                             + '! vader name=vad auto-threshold=true '
#                             + '! pocketsphinx name=asr ! fakesink')
pipeline = Gst.parse_launch(
    ' ! '.join(parse_launch_array))

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect('message::element', asr_element_message)
pipeline.set_state(gst.State.PAUSED)

# Connect our callbacks to pocketsphinx
asr = pipeline.get_by_name('asr')
# asr.connect('partial_result', asr_partial_result)
# asr.connect('result', asr_result)

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
