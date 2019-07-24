import default_logger
from pyglet import media  # Sound player
from time import sleep
from multiprocessing import Process
from os import listdir, path
from pyfirmata import Arduino  # Arduino signals reader


def play_sound():
    """Plays drum sound on Vibration Sensor beating """
    while True:
        if (arduino.digital[drum_num].read()):
            if (player.playing):
                player.seek(0)

            player.play()
            sleep(player.source.duration)
            player.pause()
            player.seek(0)


def change_volume():
    """Changes player volume on Rotation Sensor adjustment"""
    while True:
        player.volume = float(arduino.analog[volume_num].read()) / 1000


def change_sound():
    """Changes drum sound to next from sounds queue on Digital Push button press"""
    while True:
        if (arduino.digital[switch_num].read()):
            if (player.playing):
                player.pause()

            player.next_source()
            player.seek(0)
            player.play()


if __name__ == '__main__':

    logger = default_logger.get_logger('drumpad')

    # Read input pin numbers
    arduino_port = int(input('Input the port number for your Arduino: '))
    drum_num = int(input('Input pin number for drum: '))
    volume_num = int(input('Input pin number for volume: '))
    switch_num = int(input('Input pin number for switch: '))

    # Set-up Arduino and media player
    arduino = Arduino("COM{}".format(arduino_port))
    player = media.Player()

    # Importing sounds
    sounds = listdir(path.dirname(path.realpath(__file__)) + '\\drum_sounds\\')
    for sound in sounds:
        logger.info('Found {} file as a drum sound'.format(sound))
        source = media.load(path.dirname(path.realpath(__file__)) + '\\drum_sounds\\{}'.format(sound), streaming=False)
        player.queue(source)

    # Setting player volume
    player.volume = float(arduino.analog[volume_num].read()) / 1000
    logger.info('Player volume is set to {}'.format(player.volume))

    # Creating processes and starting
    p1 = Process(target=play_sound)
    p2 = Process(target=change_volume)
    p3 = Process(target=change_sound)

    p1.start()
    p2.start()
    p3.start()
