import custom_logger
import os
from multiprocessing import Process
from pyfirmata import Arduino, util
from serial.serialutil import SerialException
from xml.etree import ElementTree


class ArduinoBase():

    def __init__(self, logger_name, program_id):
        self.logger = custom_logger.get_logger(logger_name)

        config_xml = ElementTree.ElementTree(
            file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pin_configs.xml')
        )
        arduino_port = config_xml.find('./arduino').text
        self.logger.debug('Arduino port is configured as {}'.format(arduino_port))

        # Set-up Arduino
        try:

            self.arduino = Arduino(arduino_port)

        except SerialException:
            self.logger.error('Could not create Arduino device from port {}'.format(arduino_port))
            return

        iterator = util.Iterator(self.arduino)
        iterator.start()

        self.processes = []
        self.pins = {}

        pins = config_xml.find('./program[{}]'.format(program_id))
        self.logger.debug('Found pins:')
        for pin in pins.findall('pin'):
            name = pin.attrib['name']
            pin_type = pin.attrib['type']
            io = pin.attrib['put']
            number = int(pin.text)
            self.pins[name] = self.arduino.get_pin('{}:{}:{}'.format(pin_type, number, io))
            self.logger.debug('Name: {}, pin number: {}, type: {}, I/O: {}'.format(name, number, pin_type, io))

    def __del__(self):
        self.arduino.exit()

    def load_processes(self, funcs):
        for func in funcs:
            p = Process(target=func[0], args=func[1])
            self.processes.append(p)

    def start_processes(self):
        for process in self.processes:
            process.start()
