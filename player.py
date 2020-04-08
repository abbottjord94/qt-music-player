#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from UImainwindow import Ui_MainWindow


class MyFirstGuiProgram(QMainWindow, Ui_MainWindow):

        player = QMediaPlayer()
        playlist = QMediaPlaylist()
        playing = False

        def __init__(self):
            super(MyFirstGuiProgram,self).__init__()
            Ui_MainWindow.__init__(self)
            self.setupUi(self)

            self.volumeSlider.valueChanged.connect(self.volumeSliderChanged)
            self.progressSlider.valueChanged.connect(self.player.setPosition)
            self.actionOpen_File.triggered.connect(self.openMediaFilesDialog)
            self.actionOpen_Playlist.triggered.connect(self.openPlaylistFileDialog)
            self.actionSave_Playlist.triggered.connect(self.save_playlist)
            self.playButton.clicked.connect(self.play)
            self.skipNext.clicked.connect(self.skip_next)
            self.skipPrev.clicked.connect(self.skip_prev)
            self.player.error.connect(self.player_error)
            self.player.durationChanged.connect(self.setMax)
            self.player.positionChanged.connect(self.moveSlider)

            self.thread = threading.Thread(target=self.play_counter)
            self.thread.start()
            self.player.setPlaylist(self.playlist)

        def setMax(self,duration):
            print("DurationChanged: ", duration)
            self.progressSlider.setMaximum(duration)

        def moveSlider(self,position):
            print("PositionChanged: ", position, self.player.duration())
            self.progressSlider.setMaximum(self.player.duration())
            self.progressSlider.setValue(position)

        def play(self):
            if not self.playing:
                if self.player.currentMedia().isNull():
                    self.skip_next()
                else:
                    self.player.play()

                self.playing = True
            elif self.playing:
                self.player.pause()
                self.playing = False

        def load_playlist(self,file_path):
            self.playlist.load(QUrl.fromLocalFile(file_path))
            with open(file_path) as file:
                lines = file.readlines()
                for l in lines:
                    self.playlist_UI.addItem(os.path.basename(l))
                file.close()

        def save_playlist(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Playlist","","M3U (*.m3u)", options=options)
            if fileName:
                self.playlist.save(QUrl.fromLocalFile(fileName + ".m3u"), "m3u")

        def open_files(self,files):
            for f in files:
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(f)))
                self.playlist_UI.addItem(os.path.basename(f))

        def skip_prev(self):
            if self.playlist.currentMedia().isNull():
                pass
            else:
                self.playlist.prev()

        def skip_next(self):
            if self.playlist.currentMedia().isNull():
                self.playlist.setCurrentIndex(1)
                self.player.play()
            else:
                self.playlist.next()

        def search(self):
            pass

        def volumeSliderChanged(self):
            self.player.setVolume(self.volumeSlider.value())

        def play_counter(self):
            while True:
                if(self.playing):
                    self.playButton.setText("Pause")
                else:
                    self.playButton.setText("Play")

        def track_slider(self):
            print(self.player.position(), self.player.duration())

        def openMediaFilesDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self,"Select Media Files", "","All Files (*)", options=options)
            if files:
                self.open_files(files)

        def openPlaylistFileDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileName(self,"Select Playlist", "","M3U Files (*.m3u)", options=options)
            if files:
                self.load_playlist(files)

        def player_error(self):
            print(self.player.error())


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = MyFirstGuiProgram()
        window.show()
        sys.exit(app.exec_())
