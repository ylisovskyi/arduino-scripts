import pyglet
import time
from multiprocessing import Process
from os import listdir
from pyfirmata import Arduino


def play_sound():
    while True:
        if (arduino.digital[drum_num].read()):
            player.play()
            time.sleep(player.source.duration)
            player.pause()
            player.seek(0)


def change_volume():
    while True:
        player.volume = float(arduino.analog[volume_num].read()) / 1000  # Adjust volume


def change_sound():
    while True:
        if (arduino.digital[switch_num].read()):
            if (player.playing):
                player.pause()
                player.next_source()  # Choose next drum sound
                player.seek(0)
                player.play()


if __name__ == '__main__':

    # Set-up Arduino and media player
    arduino = Arduino("COM3")
    player = pyglet.media.Player()

    # Read inout pin numbers
    drum_num = int(input('Input pin number for drum: '))
    volume_num = int(input('Input pin number for volume: '))
    switch_num = int(input('Input pin number for switch: '))

    # Create drum sounds queue and set player volume
    sounds = listdir('drum_sounds/')
    # Importing sounds
    for sound in sounds:
        print('Found {} file as a drum sound'.format(sound))
        source = pyglet.media.load('drum_sounds/{}'.format(sound), streaming=False)
        player.queue(source)

    # Setting volume
    player.volume = 0.5
    player.volume = float(arduino.analog[volume_num].read()) / 1000

    # Creating processes and starting
    p1 = Process(target=play_sound)
    p2 = Process(target=change_volume)
    p3 = Process(target=change_sound)

    p1.start()
    p2.start()
    p3.start()
