from GL_Studio import *
import copy
import random


# por renderizar una imagen negra con un punto blanco en una ubicación random dentro de la imagen.
def bullet_one(width, heigth):

    gl_create_window(width, heigth)
    filename('Punto_Random.bmp')

    gl_view_port(0, 0, width, heigth)
    thisy = random.uniform(-1, 1)
    thisx = random.uniform(-1, 1)

    realx = normalize(thisx, width)
    realy = normalize(thisy, heigth)
    gl_vertex(realx, realy)
    gl_finish()


# por renderizar una imagen negra con un punto blanco en cada esquina.
def bullet_two(width, height):
    gl_create_window(600, 800)
    gl_clear()
    filename('Puntos_Esquina.bmp')

    gl_view_port(0, 0, width -1, height -1)
    #Este es top right
    top_left_x = normalize(-1, width)
    top_left_y = normalize(1, height)

    top_right_x = normalize(1, width)
    top_right_y = normalize(1, height)

    bottom_left_x = normalize(-1, width)
    bottom_left_y = normalize(-1, height)

    bottom_right_x = normalize(1, width)
    bottom_right_y = normalize(-1, height)

    gl_vertex(top_left_x, top_left_y)
    gl_vertex(top_right_x, top_right_y)
    gl_vertex(bottom_left_x, bottom_left_y)
    gl_vertex(bottom_right_x, bottom_right_y)
    line(-1, -1, 0.8, 1, width, height)

    gl_finish()


# por renderizar un cubo de 100 pixeles en el centro de su imagen.
#Basandose en el pseudocodigo del algoritmo de bresenham.
def line(startx, starty, endx, endy, width, height):

    startx = normalize(startx, width)
    starty = normalize(starty, height)
    endx = normalize(endx, width)
    endy = normalize(endy, height)

    if abs(endy - starty) < abs(endx - startx):
        if startx > endx:
            lineLow(endx, endy, startx, starty)
        else:
            lineLow(startx, starty, endx, endy)
    else:
        if starty > endy:
            lineHigh(endx, endy, startx, starty)
        else:
            lineHigh(startx, starty, endx, endy)
    return


def lineLow(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi =1
    if dy < 0:
        yi = -1
        dy = -dy
    D = 2*dy - dx
    y = y0

    x = x0
    for x in range(x1):
        gl_vertex(x, y)
        if D > 0:
            y = y + yi
            D = D - 2*dx
        D = D + 2*dy
    return


def lineHigh(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2 * dx - dy
    x = x0

    y = y0
    for y in range(y1):
        gl_vertex(x, y)
        if D > 0:
            x = x + xi
            D = D - 2 * dy
        D = D + 2 * dx
    return


def bullet_three():


    pass


# por renderizar líneas blancas en toda la orilla de su imagen (4 lineas)
def bullet_four():
    pass


# por renderizar una línea blanca en diagonal por el centro de su imagen.
def bullet_five():
    pass


# por llenar su imagen entera de puntos blancos y negros (las posibilidades de que un punto sea blanco o negro son de
# 50%)
def bullet_six():
    pass


# por llenar su imagen entera de puntos de colores random
def bullet_seven():
    pass


# por crear una escena de un cielo con estrellas
def bullet_eight():
    pass


# por crear una escena de 80 x 96 pixeles o 160 x 192 pixeles representando un frame de un juego de Atari. Sólo pueden
# usar los colores NTSC de
def bullet_nine():
    pass


bullet_one(600,800)
bullet_two(600,800)


