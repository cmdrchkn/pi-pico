"""i2c testing"""

# === Import === #
import machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import ssd1306
from time import sleep
import utime
from random import randint
import SourceCodePro_Light


# == Functions == #
def full_update_lcd(display, altitude, altitude_unit, speed, speed_unit, apoapsis, apoapsis_unit, periapsis, periapsis_unit):
    display.move_to(0, 0)
    display.putstr(""" Altitude {: >6} {: <3}
    Speed {: >6} {: <3}
 Apoapsis {: >6} {: <3}
Periapsis {: >6} {: <3}""".format(
    altitude,  altitude_unit,
    speed,     speed_unit,
    apoapsis,  apoapsis_unit,
    periapsis, periapsis_unit
   ))

def update_lcd(display, altitude, altitude_unit, speed, speed_unit, apoapsis, apoapsis_unit, periapsis, periapsis_unit):
    display.move_to(10, 0)
    display.putstr("""{: >6} {: <3}""".format(altitude,  altitude_unit))
    display.move_to(10, 1)
    display.putstr("""{: >6} {: <3}""".format(speed,     speed_unit))
    display.move_to(10, 2)
    display.putstr("""{: >6} {: <3}""".format(apoapsis,  apoapsis_unit))
    display.move_to(10, 3)
    display.putstr("""{: >6} {: <3}""".format(periapsis, periapsis_unit))

def full_update_oled(display, altitude, altitude_unit, speed, speed_unit, apoapsis, apoapsis_unit, periapsis, periapsis_unit):
    display.fill(0)
    display.setfont('ArialMT_Plain_24')
    display.text("""{: >6} {: <3}""".format(altitude,  altitude_unit), 0, 0)
    #display.text("""{: >6} {: <3}""".format(speed,     speed_unit),    0, 16)
    #display.text("""{: >6} {: <3}""".format(apoapsis,  apoapsis_unit), 0, 32)
    #display.text("""{: >6} {: <3}""".format(periapsis, periapsis_unit),0, 48)

# === Main === #
def main():
    # - Set up interface
    sdaPIN = machine.Pin(0)
    sclPIN = machine.Pin(1)
    i2c = machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=600000)
    
    # -- Scan for devices
    print('Scanning for i2c devices...')
    devices = i2c.scan()
    if len(devices) == 0:
        print("\tNo i2c devices detected!")
    else:
        print('\tDetected {} i2c devices:'.format( len(devices) ) )
    for device in devices:
        print("\t -", hex(device))

    # -- Test 20x4 char display
    #print('Testing 20x4')
    #lcd1 = I2cLcd(i2c, 0x3f, 4, 20)
    #lcd1.putstr("""12345678901234567890
#12345678901234567890
#12345678901234567890
#12345678901234567890""")
    
    # -- Test 128x64 pixel oled
    print('Test oled')
    oled1 = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
    #oled1.text('1234567890123456', 0, 0)
    #oled1.text('1234567890123456', 0, 16)
    #oled1.text('1234567890123456', 0, 32)
    #oled1.text('1234567890123456', 0, 48)
    oled1.rotate(False)
    #oled1.show()
    full_update_oled(oled1, 0, 'm', 0, 'm/s', 0, 'km', 0, 'm')
    
    print('Approximating display')
    #lcd1.move_to(0, 0)
    #full_update_lcd(lcd1, 0, 'm', 0, 'm/s', 0, 'km', 0, 'm')
    oled1.fill(0)
    oled1.rect(9, 9, 118, 53, 1)
    oled1.show()
    
    loops = 0
    alt = 0
    spd = 0
    apo = 0
    per = 0
    
    altu = 'm'
    spdu = 'm/s'
    apou = 'm'
    peru = 'm'
    
    while True:
        if spd > 4500:
            spd = 4500
        if alt > 999999:
            alt = alt / 1000
            altu = 'km'
        if apo > 999999:
            apo = apo / 1000
            apou = 'km'
        if per > 999999:
            per = per / 1000
            peru = 'km'
        
        loops+=1
        print('Starting @', utime.localtime())
        
        # char lcd
        #update_lcd(lcd1, alt, altu, spd, spdu, apo, apou, per, peru)
        full_update_oled(oled1, alt, altu, spd, spdu, apo, apou, per, peru)
        
        # oled
        #oled1.fill(0)
        #oled1.fill_rect(9, 9, randint(11,120), 53, 1)
        #oled1.rect(9, 9, 118, 53, 1)
        
        oled1.show()
        
        alt += spd * 2
        if loops % 2 == 0:
            apo = alt + 3 * spd
        if loops % 5 == 0:
            if alt < 10000:
                spd = 120
            elif alt < 30000:
                spd += 30
            elif alt < 100000:
                spd += 200
            else:
                spd = 4500
        
        print('Completed @', utime.localtime())
        #sleep(.2)

# === Hook === #
if __name__ == '__main__':
    main()
    