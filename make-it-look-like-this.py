#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib
import threading


GObject.threads_init()
Gst.init(None)

gst = Gst


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


class DemoApp(object):

    """GStreamer/PocketSphinx Demo Application"""

    def __init__(self):
        """Initialize a DemoApp object"""
        self.init_gst()

    def init_gst(self):
        """Initialize the speech components"""
        parse_launch_array = ['autoaudiosrc ! audioconvert ! audioresample '
                              + '! pocketsphinx name=asr ! fakesink']
        self.pipeline = gst.parse_launch(
            ' ! '.join(parse_launch_array))

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.element_message)

        self.pipeline.set_state(gst.State.PAUSED)

    def set_ready(self):
        PWD = os.path.dirname(os.path.abspath(__file__))
        LM_PATH = "{}/1602.lm".format(PWD)
        DICT_PATH = "{}/9812.dic".format(PWD)
        PROP_HMM_DIR = "{}/hmm/en_US/hub4wsj_sc_8k".format(PWD)
        ps_device = 'hw:1'
        silprob = 0.1
        wip = 1e-4
        bestpath = 0

        asr = self.pipeline.get_by_name('asr')
        asr.set_property('lm', LM_PATH)
        asr.set_property('dict', DICT_PATH)
        asr.set_property('hmm', PROP_HMM_DIR)
        asr.set_state(gst.State.PLAYING)


    def element_message(self, bus, msg):
        """Receive element messages from the bus."""
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return

        if msg.get_structure()['final']:
            self.final_result(
                msg.get_structure()['hypothesis'], msg.get_structure()['confidence'])
            self.pipeline.set_state(gst.State.PAUSED)
        elif msg.get_structure()['hypothesis']:
            self.partial_result(msg.get_structure()['hypothesis'])

    def partial_result(self, hyp):
        """Delete any previous selection, insert text and select it."""
        # All this stuff appears as one single action
        print hyp

    def final_result(self, hyp, confidence):
        """Insert the final result."""
        # All this stuff appears as one single action
        print hyp
        print confidence

app = DemoApp()
app.set_ready()
# GLib.MainLoop()

g_loop = threading.Thread(target=GLib.MainLoop().run)
g_loop.daemon = False
g_loop.start()
