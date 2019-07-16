# face-lock
Face-recognition based door lock for use in access control systems.

## Hardware:

Raspberry Pi Zero W with Camera Module (USB Camera will suffice)
Solenoid lock
5V Relay
12V battery source
Jumper cables 

(More detailed specifications coming soon)



## How to get DLIB / face_recognition running on Windows:

To be able to use the face_recognition library on Windows, we must install several tools.

1. Install VS Build Tools C++ plugin:
	a. [Download Build Tools for Visual Studio 2019: (Under Tools for VS 2019)](https://visualstudio.microsoft.com/downloads/)
	b.  Run the installer, select and install C++ build stools once available.
2. Install CMake (cmake.org/download) or (pip install cmake)
3. pip install dlib
4. pip install face_recognition

## How to get DLIB / face_recognition running on Raspberry Pi:

To install on a Raspberry Pi is a significantly harder endeavor. 

It is recommended that change your Swap size to (1024/2048/etc) avoid running out of memory when compiling dlib, but do remember to switch it back once you are done). Also, be warned that this will often wear down the SD card or USB drive you are using.

1. Install CMake (cmake.org/download) or (pip(3) install cmake)
2. pip(3) install dlib
3. pip(3) install face_recognition

Ensure you run your pip commands as superuser, and I would recommended the flag -v (verbose) for easier monitoring of progress. If the installation fails, you may try compiling from source as another option. Both the DLIB and face_recognition repositories have in-depth tutorials.
