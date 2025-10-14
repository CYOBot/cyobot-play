from lib.display import Matrix
import time

matrix = Matrix()
matrix.reset()

apple = [
    ([2,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23], (255,0,0)),   # red body
    ([2], (0,255,0))                                               # green stem (blink this one)
]

drumstick = [
    # Meat (orange-brown, main body)
    ([1,2,3,5,6,7,8,10,11,12,13,16,17], (255,120,0)),

    # Highlight (brighter yellow-orange area)
    ([7,11,12], (255,180,50)),

    # Bone (bottom tip, white)
    ([20,21], (255,255,255))
]
def draw_icon(icon):
    for layer in icon:
        matrix.set_character("", indices=layer[0], red=layer[1][0], green=layer[1][1], blue=layer[1][2])

draw_icon(apple)