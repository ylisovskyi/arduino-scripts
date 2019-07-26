from arduino_base import ArduinoBase
from time import sleep

durations = {'.': 0.1, '-': 0.3}
morse_map = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----',
    '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}


def play_sound(pin, duration):
    pin.write(1)
    sleep(durations[duration])
    pin.write(0)


def play_character(pin, char):
    for sound in morse_map[char]:
        arduino.logger.info('Playing {}({})'.format(char, morse_map[char]))
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
