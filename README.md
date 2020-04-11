# QT Music Player
A music player written in Python using the Python QT bindings


# Usage
This program requires PyQt5, requests, and youtube-dl to work. Additionally, an OAuth2 key for the YouTube API is required to use the YouTube search feature, and should be placed as a string in "key.file"

# Bugs
The main issue is that the progress slider does not work. This is either due to a problem with the files I've been testing with, a problem with PyQt5, or an issue in Ubuntu itself. The problem is due to the program being unable to find the duration of an audio file, and always returns 0 for that value. In addition, the durationChanged signal is never sent by the QMediaPlayer object, and this may also be causing the problem.

# Demo

![MusicPlayerDemo](https://github.com/abbottjord94/qt-music-player/blob/master/Peek%202020-04-11%2012-12.gif)
