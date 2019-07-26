from arduino_base import ArduinoBase
from pyglet import media  # Sound player
from time import sleep
from os import listdir, path


def play_sound(pin):
    """Plays drum sound on Vibration Sensor beating """
    while True:
        if (pin.read()):
            if (not player.playing):
                player.play()
                sleep(player.source.duration)
                player.pause()

            player.seek(0)


def change_volume(pin):
    """Changes player volume on Rotation Sensor adjustment"""
    while True:
        rotation_value = pin.read()
        if (rotation_value):
            player.volume = float(rotation_value) / 1000


def change_sound(pin):
    """Changes drum sound to next from sounds queue on Digital Push button press"""
    while True:
        if (pin.read()):
            if (player.playing):
                player.pause()

            player.next_source()
            player.seek(0)
            player.play()


if __name__ == '__main__':

    arduino = ArduinoBase(logger_name='drumpad', program_id=1)
    player = media.Player()

    # Importing sounds
    sounds = listdir('drum_sounds')
    for sound in sounds:
        arduino.logger.info('Found {} file as a drum sound'.format(sound))
        source = media.load(path.join('drum_sounds', sound), streaming=False)
        player.queue(source)

    # Setting player volume
    player.volume = 0.5
    arduino.logger.info('Player volume is set to {}'.format(player.volume))

    funcs = [
        (play_sound, (arduino.pins['vibration'],)),
        (change_volume, (arduino.pins['rotation'],)),
        (change_sound, (arduino.pins['button'],))
    ]
    arduino.load_processes(funcs=funcs)
    arduino.start_processes()
