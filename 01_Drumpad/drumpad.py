import custom_logger
from pyglet import media  # Sound player
from time import sleep
from multiprocessing import Process
from os import listdir, path
from pyfirmata import Arduino  # Arduino signals reader


def play_sound(device):
    """Plays drum sound on Vibration Sensor beating """
    while True:
        if (device.digital[drum_num].read()):
            if (not player.playing):
                player.play()
                sleep(player.source.duration)
                player.pause()

            player.seek(0)


def change_volume(device):
    """Changes player volume on Rotation Sensor adjustment"""
    while True:
        rotation_value = device.analog[volume_num].read()
        if (rotation_value):
            player.volume = float(rotation_value) / 1000


def change_sound(device):
    """Changes drum sound to next from sounds queue on Digital Push button press"""
    while True:
        if (device.digital[switch_num].read()):
            if (player.playing):
                player.pause()

            player.next_source()
            player.seek(0)
            player.play()


if __name__ == '__main__':

    logger = custom_logger.get_logger('drumpad')

    # Read input pin numbers
    arduino_port = int(input('Input the port number for your Arduino: '))
    drum_num = int(input('Input pin number for drum: '))
    volume_num = int(input('Input pin number for volume: '))
    switch_num = int(input('Input pin number for switch: '))

    # Set-up Arduino and media player
    arduino = Arduino("COM{}".format(arduino_port))
    player = media.Player()

    # Importing sounds
    sounds = listdir('drum_sounds')
    for sound in sounds:
        logger.info('Found {} file as a drum sound'.format(sound))
        source = media.load(path.join('drum_sounds', sound), streaming=False)
        player.queue(source)

    # Setting player volume
    rotation_value = arduino.analog[volume_num].read()
    if (rotation_value):
        player.volume = float(rotation_value) / 1000
    logger.info('Player volume is set to {}'.format(player.volume))

    # Creating processes and starting
    p1 = Process(target=play_sound, args=(arduino,))
    p2 = Process(target=change_volume, args=(arduino,))
    p3 = Process(target=change_sound, args=(arduino,))

    p1.start()
    p2.start()
    p3.start()
