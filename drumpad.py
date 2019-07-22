from pyfirmata import Arduino
import pyglet

# Set-up Arduino and media player
arduino = Arduino("COM3")
player = pyglet.media.Player()

# Read inout pin numbers
drum_num = int(input('Input pin number for drum: '))
volume_num = int(input('Input pin number for volume: '))
switch_num = int(input('Input pin number for switch: '))

# Create drum sounds queue and set player volume
sounds = [
    '1.wav',
    '2.wav',
    '3.wav'
]
for sound in sounds:
    source = pyglet.media.load('drum_sounds/%s' % sound, streaming=False)
    player.queue(source)

player.volume = float(arduino.analog[volume_num].read()) / 1000

while True:
    if (arduino.digital[drum_num].read()):
        player.play()  # Drum beat
    player.volume = float(arduino.analog[volume_num].read()) / 1000  # Adjust volume
    if (arduino.digital[switch_num].read()):
        player.next_source()  # Choose next drum sound
