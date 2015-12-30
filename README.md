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
