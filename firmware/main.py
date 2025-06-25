# A "should" work firmware, might subject to change in the future

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import OLED, OLEDScreen
from kmk.extensions.rgb import RGB

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28)  # KB_COL1~3
keyboard.row_pins = (board.GP3, board.GP4, board.GP2)  # KB_ROW1~3
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [
        KC.A, KC.B, KC.C,
        KC.D, KC.E, KC.F,
        KC.G, KC.H, KC.NO
    ]
]

encoder = EncoderHandler()
encoder.pins = ((board.GP0, board.GP29, None),)  # ROTATE_A, ROTATE_B, no switch
encoder.map = [
    (lambda: keyboard.send(KC.VOLD), lambda: keyboard.send(KC.VOLU))
]
keyboard.modules.append(encoder)

oled = OLED(
    rotation=OLEDRotation.ROT_0,
    sda=board.GP6,  # OLED_SDA
    scl=board.GP7,  # OLED_SCL
)
oled.init_display()
oled.set_display_content(
    OLEDScreen(lambda: ['Hello World', 'KMK Firmware'])
)
keyboard.modules.append(oled)

rgb = RGB(
    pixel_pin=board.GP1,  # LED_DATA
    num_pixels=12,         # Total number of SK6812Mini-E
    rgb_order=(1, 0, 2),   # Usually GRB, but double-check yours!
    auto_update=True
)
rgb.effect = "rainbow"
keyboard.extensions.append(rgb)

if __name__ == '__main__':
    keyboard.go()
