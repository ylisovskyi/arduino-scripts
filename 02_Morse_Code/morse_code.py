import custom_logger
from time import sleep
from os import listdir, path
from pyfirmata import Arduino  # Arduino signals reader/writer


if __name__ == '__main__':
    logger = custom_logger.get_logger('drumpad')

    # Read input pin numbers
    arduino_port = int(input('Input the port number for your Arduino: '))
    drum_num = int(input('Input pin number for speaker: '))

    # Set-up Arduino and media player
    arduino = Arduino("COM{}".format(arduino_port))
