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

# Layout on the PCB:
#
# EC11 7 8
#   4  5 6
#   1  2 3

keyboard.keymap = [
    [
        KC.LEFT, KC.RIGHT, KC.NO,
        KC.F13, KC.F15, KC.F17,
        KC.F14, KC.F16, KC.F18
    ]
]

encoder = EncoderHandler()
encoder.pins = ((board.GP0, board.GP29, None))  # ROTATE_A, ROTATE_B, no switch
encoder.map = [
    (lambda: keyboard.send(KC.VOLD), lambda: keyboard.send(KC.VOLU))
]
keyboard.modules.append(encoder)

i2c_bus = busio.I2C(board.GP7, board.GP6)
display_driver = SSD1306(
    i2c=i2c_bus,
)

display = Display(
    display=display_driver,
    entries=[
        TextEntry(text="SmolPad", x=0, y=0),
        TextEntry(text="I think it's working now", x=0, y=32, y_anchor='B'),
    ],
    width=128,
    height=32,
    dim_time=10,
    dim_target=0.2,
    off_time=60,
    brightness=1,
)

rgb = RGB(
    pixel_pin     = board.GP10,
    num_pixels    = 12,
    hue_default   = 240,
    sat_default   = 255,
    val_default   = 100,
    animation_speed = 2
)

keyboard.extensions.append(rgb)
rgb.effect = "knight"


if __name__ == '__main__':
    keyboard.go()
