#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import argparse

# insert path so we can access things w/o having to re-install everything
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

PWD = os.path.dirname(os.path.abspath(__file__))

print PWD

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib
import threading

GObject.threads_init()
Gst.init(None)

print '********************************************************'
print GObject.pygobject_version
print '********************************************************'

Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

from IPython.core.debugger import Tracer
from IPython.core import ultratb

sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                     color_scheme='Linux',
                                     call_pdb=True,
                                     ostream=sys.__stdout__)

from colorlog import ColoredFormatter

import logging

gst = Gst


def get_pocketsphinx_definition(device, hmm, lm, dic):
    return ['alsasrc device=' +
            device,
            'queue silent=false leaky=2 max-size-buffers=0 max-size-time=0 max-size-bytes=0',
            'audioconvert',
            'audioresample',
            'audio/x-raw,format=S16LE,channels=1,layout=interleaved',
            'pocketsphinx name=asr bestpath=0',
            'queue leaky=2',
            'fakesink']


def run_pipeline(device=None, hmm=None, lm=None, dict=None):
    pipeline = Gst.parse_launch(' ! '.join(
                                get_pocketsphinx_definition(device,
                                                            hmm,
                                                            lm,
                                                            dict)))

    pocketsphinx = pipeline.get_by_name('asr')
    if hmm:
        pocketsphinx.set_property('hmm', hmm)
    if lm:
        pocketsphinx.set_property('lm', lm)
    if dict:
        pocketsphinx.set_property('dict', dict)

    bus = pipeline.get_bus()

    # Start playing
    pipeline.set_state(Gst.State.PLAYING)

    # Wait until error or EOS
    while True:
        try:
            msg = bus.timed_pop(Gst.CLOCK_TIME_NONE)
            if msg:
                # if msg.get_structure():
                #    print(msg.get_structure().to_string())

                if msg.type == Gst.MessageType.EOS:
                    break
                struct = msg.get_structure()
                if struct and struct.get_name() == 'pocketsphinx':
                    if struct['final']:
                        logger.info(struct['hypothesis'])
        except KeyboardInterrupt:
            pipeline.send_event(Gst.Event.new_eos())

    # Free resources
    pipeline.set_state(Gst.State.NULL)


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

if __name__ == '__main__':
    global logger
    logger = setup_logger()
    LANGUAGE_VERSION = 1473
    HOMEDIR = "/home/pi"
    LANGUAGE_FILE_HOME = "{}/dev/bossjones-github/scarlett-gstreamer-pocketsphinx-demo".format(
        HOMEDIR)
    LM_PATH = "{}/{}.lm".format(LANGUAGE_FILE_HOME, LANGUAGE_VERSION)
    DICT_PATH = "{}/{}.dic".format(LANGUAGE_FILE_HOME, LANGUAGE_VERSION)
    HMM_PATH = "{}/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us".format(
        HOMEDIR)
    bestpath = 0
    PS_DEVICE = 'plughw:CARD=Device,DEV=0'

    parser = argparse.ArgumentParser(description='Recognize speech from audio')
    parser.add_argument('--device',
                        default=PS_DEVICE,
                        help='Pocketsphinx audio source device')
    parser.add_argument('--hmm',
                        default=HMM_PATH,
                        help='Path to a pocketsphinx HMM data directory')
    parser.add_argument('--lm',
                        default=LM_PATH,
                        help='Path to a pocketsphinx language model file')
    parser.add_argument('--dict',
                        default=DICT_PATH,
                        help='Path to a pocketsphinx CMU dictionary file')
    args = parser.parse_args()
    run_pipeline(**vars(args))
