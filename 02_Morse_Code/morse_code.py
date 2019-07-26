from . import *
from arduino_base import ArduinoBase
from time import sleep


def play_sound(pin, duration):
    pin.write(1)
    sleep(DURATIONS[duration])
    pin.write(0)


def play_character(pin, char):
    for sound in MORSE_MAP[char]:
        arduino.logger.info('Playing {}({})'.format(char, MORSE_MAP[char]))
        play_sound(pin, sound)
        sleep(0.1)


def play_word(pin, word):
    for c in word:
        play_character(pin, c)
        sleep(0.3)


def play_sentence(pin, words):
    words = words.split(' ')
    for word in words:
        play_word(pin, word)
        sleep(0.7)


if __name__ == '__main__':

    arduino = ArduinoBase(logger_name='morse', program_id=2)
    sound_pin = arduino.pins['sound']

    sentence = ''
    while sentence != 'q':
        sentence = input('Enter your sentence (q for quit): ')
        play_sentence(sound_pin, sentence)
