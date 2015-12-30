# scarlett-gstreamer-pocketsphinx-demo
Basic demo to make sure all gstreamer + pocketsphinx dependencies were installed correctly, and STT works w/ pocketphinx gst plugin for scarlett


# IMPORTANT NOTE:
Currently assumes `hmm` folder is located at `./hmm` FYI. Will need to figure out if this is still required in newer versions of pocketpshinx or not.


# NOTE:
This demo uses `autoenv` (see: https://github.com/kennethreitz/autoenv ) to set environment variables to find pocketphinx static libs, eg:

```
  using virtualenv: scarlett-dbus-poc scarlett-ansible in ~
○ → ls -lta /home/pi/.virtualenvs/scarlett-dbus-poc/lib/
total 6324
drwxrwxr-x 2 pi pi    4096 Dec 29 19:08 pkgconfig
drwxrwxr-x 2 pi pi    4096 Dec 29 19:08 gstreamer-1.0
drwxrwxr-x 5 pi pi    4096 Dec 29 19:08 .
-rw-r--r-- 1 pi pi 1941766 Dec 29 19:08 libpocketsphinx.a
-rwxr-xr-x 1 pi pi    1393 Dec 29 19:08 libpocketsphinx.la
lrwxrwxrwx 1 pi pi      24 Dec 29 19:08 libpocketsphinx.so -> libpocketsphinx.so.3.0.0
lrwxrwxrwx 1 pi pi      24 Dec 29 19:08 libpocketsphinx.so.3 -> libpocketsphinx.so.3.0.0
-rwxr-xr-x 1 pi pi 1147601 Dec 29 19:08 libpocketsphinx.so.3.0.0
-rw-r--r-- 1 pi pi   18938 Dec 29 18:59 libsphinxad.a
-rwxr-xr-x 1 pi pi    1096 Dec 29 18:59 libsphinxad.la
lrwxrwxrwx 1 pi pi      20 Dec 29 18:59 libsphinxad.so -> libsphinxad.so.3.0.0
lrwxrwxrwx 1 pi pi      20 Dec 29 18:59 libsphinxad.so.3 -> libsphinxad.so.3.0.0
-rwxr-xr-x 1 pi pi   21677 Dec 29 18:59 libsphinxad.so.3.0.0
-rw-r--r-- 1 pi pi 2074892 Dec 29 18:59 libsphinxbase.a
-rwxr-xr-x 1 pi pi    1049 Dec 29 18:59 libsphinxbase.la
lrwxrwxrwx 1 pi pi      22 Dec 29 18:59 libsphinxbase.so -> libsphinxbase.so.3.0.0
lrwxrwxrwx 1 pi pi      22 Dec 29 18:59 libsphinxbase.so.3 -> libsphinxbase.so.3.0.0
-rwxr-xr-x 1 pi pi 1222864 Dec 29 18:59 libsphinxbase.so.3.0.0
drwxrwxr-x 8 pi pi    4096 Dec 24 12:09 ..
drwxrwxr-x 4 pi pi    4096 Dec 23 16:25 python2.7
```

If you don't have `autoenv` installed, simply run `source /path/to/scarlett-gstreamer-pocketsphinx-demo/.env`


# gst-inspect-1.0 pocketsphinx default values:

```
± |master ✓| → gst-inspect-1.0 pocketsphinx
Current configuration:
[NAME]          [DEFLT]     [VALUE]
-agc            none        none
-agcthresh      2.0     2.000000e+00
-allphone
-allphone_ci        no      no
-alpha          0.97        9.700000e-01
-ascale         20.0        2.000000e+01
-aw         1       1
-backtrace      no      no
-beam           1e-48       1.000000e-48
-bestpath       yes     yes
-bestpathlw     9.5     9.500000e+00
-ceplen         13      13
-cmn            current     current
-cmninit        8.0     40,3,-1
-compallsen     no      no
-debug                  0
-dict                   /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/cmudict-en-us.dict
-dictcase       no      no
-dither         no      no
-doublebw       no      no
-ds         1       1
-fdict                  /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/noisedict
-feat           1s_c_d_dd   1s_c_d_dd
-featparams             /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/feat.params
-fillprob       1e-8        1.000000e-08
-frate          100     100
-fsg
-fsgusealtpron      yes     yes
-fsgusefiller       yes     yes
-fwdflat        yes     yes
-fwdflatbeam        1e-64       1.000000e-64
-fwdflatefwid       4       4
-fwdflatlw      8.5     8.500000e+00
-fwdflatsfwin       25      25
-fwdflatwbeam       7e-29       7.000000e-29
-fwdtree        yes     yes
-hmm                    /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us
-input_endian       little      little
-jsgf
-keyphrase
-kws
-kws_delay      10      10
-kws_plp        1e-1        1.000000e-01
-kws_threshold      1       1.000000e+00
-latsize        5000        5000
-lda
-ldadim         0       0
-lifter         0       22
-lm                 /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us.lm.bin
-lmctl
-lmname
-logbase        1.0001      1.000100e+00
-logfn
-logspec        no      no
-lowerf         133.33334   1.300000e+02
-lpbeam         1e-40       1.000000e-40
-lponlybeam     7e-29       7.000000e-29
-lw         6.5     6.500000e+00
-maxhmmpf       30000       30000
-maxwpf         -1      -1
-mdef                   /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/mdef
-mean                   /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/means
-mfclogdir
-min_endfr      0       0
-mixw
-mixwfloor      0.0000001   1.000000e-07
-mllr
-mmap           yes     yes
-ncep           13      13
-nfft           512     512
-nfilt          40      25
-nwpen          1.0     1.000000e+00
-pbeam          1e-48       1.000000e-48
-pip            1.0     1.000000e+00
-pl_beam        1e-10       1.000000e-10
-pl_pbeam       1e-10       1.000000e-10
-pl_pip         1.0     1.000000e+00
-pl_weight      3.0     3.000000e+00
-pl_window      5       5
-rawlogdir
-remove_dc      no      no
-remove_noise       yes     yes
-remove_silence     yes     yes
-round_filters      yes     yes
-samprate       16000       1.600000e+04
-seed           -1      -1
-sendump                /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/sendump
-senlogdir
-senmgau
-silprob        0.005       5.000000e-03
-smoothspec     no      no
-svspec                 0-12/13-25/26-38
-tmat                   /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/transition_matrices
-tmatfloor      0.0001      1.000000e-04
-topn           4       4
-topn_beam      0       0
-toprule
-transform      legacy      dct
-unit_area      yes     yes
-upperf         6855.4976   6.800000e+03
-uw         1.0     1.000000e+00
-vad_postspeech     50      50
-vad_prespeech      20      20
-vad_startspeech    10      10
-vad_threshold      2.0     2.000000e+00
-var                    /home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us/variances
-varfloor       0.0001      1.000000e-04
-varnorm        no      no
-verbose        no      no
-warp_params
-warp_type      inverse_linear  inverse_linear
-wbeam          7e-29       7.000000e-29
-wip            0.65        6.500000e-01
-wlen           0.025625    2.562500e-02

Factory Details:
  Rank                     none (0)
  Long-name                PocketSphinx
  Klass                    Filter/Audio
  Description              Convert speech to text
  Author                   CMUSphinx-devel <cmusphinx-devel@lists.sourceforge.net>

Plugin Details:
  Name                     pocketsphinx
  Description              PocketSphinx plugin
  Filename                 /home/pi/.virtualenvs/scarlett-dbus-poc/lib/gstreamer-1.0/libgstpocketsphinx.so
  Version                  5prealpha
  License                  BSD
  Source module            pocketsphinx
  Binary package           PocketSphinx
  Origin URL               http://cmusphinx.sourceforge.net/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstPocketSphinx

Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      audio/x-raw
                 format: { S16LE }
               channels: 1
                   rate: 16000

  SRC template: 'src'
    Availability: Always
    Capabilities:
      text/plain


Element Flags:
  no flags set

Element Implementation:
  Has change_state() function: gst_element_change_state_func

Element has no clocking capabilities.
Element has no indexing capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Implementation:
      Has chainfunc(): 0x7f8017bad1c0
      Has custom eventfunc(): 0x7f8017bad160
      Has custom queryfunc(): gst_pad_query_default
      Has custom iterintlinkfunc(): gst_pad_iterate_internal_links_default
    Pad Template: 'sink'
  SRC: 'src'
    Implementation:
      Has custom eventfunc(): gst_pad_event_default
      Has custom queryfunc(): gst_pad_query_default
      Has custom iterintlinkfunc(): gst_pad_iterate_internal_links_default
    Pad Template: 'src'

Element Properties:
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "pocketsphinx0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  hmm                 : Directory containing acoustic model parameters
                        flags: readable, writable
                        String. Default: "/home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us"
  lm                  : Language model file
                        flags: readable, writable
                        String. Default: "/home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/en-us.lm.bin"
  lmctl               : Language model control file (for class LMs)
                        flags: readable, writable
                        String. Default: null
  lmname              : Language model name (to select LMs from lmctl)
                        flags: readable, writable
                        String. Default: null
  dict                : Dictionary File
                        flags: readable, writable
                        String. Default: "/home/pi/.virtualenvs/scarlett-dbus-poc/share/pocketsphinx/model/en-us/cmudict-en-us.dict"
  fsg                 : Finite state grammar file
                        flags: readable, writable
                        String. Default: null
  fsg-model           : Finite state grammar object (fsg_model_t *)
                        flags: writable
                        Pointer. Write only
  fwdflat             : Enable Flat Lexicon Search
                        flags: readable, writable
                        Boolean. Default: true
  bestpath            : Enable Graph Search
                        flags: readable, writable
                        Boolean. Default: true
  maxhmmpf            : Maximum number of HMMs searched per frame
                        flags: readable, writable
                        Integer. Range: 1 - 100000 Default: 30000
  maxwpf              : Maximum number of words searched per frame
                        flags: readable, writable
                        Integer. Range: 1 - 100000 Default: -1
  beam                : Beam width applied to every frame in Viterbi search
                        flags: readable, writable
                        Double. Range:              -1 -               1 Default:           1e-48
  wbeam               : Beam width applied to phone transitions
                        flags: readable, writable
                        Double. Range:              -1 -               1 Default:           7e-29
  pbeam               : Beam width applied to phone transitions
                        flags: readable, writable
                        Double. Range:              -1 -               1 Default:           1e-48
  dsratio             : Evaluate acoustic model every N frames
                        flags: readable, writable
                        Integer. Range: 1 - 10 Default: 1
  latdir              : Output Directory for Lattices
                        flags: readable, writable
                        String. Default: null
  decoder             : The underlying decoder
                        flags: readable
                        Boxed pointer of type "PSDecoder"
  configured          : Set this to finalize configuration
                        flags: readable, writable
                        Boolean. Default: true
```

