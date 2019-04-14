from GL_Studio import *
import copy
import random


# por renderizar una imagen negra con un punto blanco en una ubicación random dentro de la imagen.
def bullet_one():

    gl_create_window(600, 800)
    filename('Punto_Random.bmp')

    gl_view_port(0, 0, 600, 800)
    thisy = random.uniform(-1, 1)
    thisx = random.uniform(-1, 1)
    print(thisy)
    print(thisx)

    realx = normalize(thisx, 600)
    realy = normalize(thisy, 800)
    gl_vertex(realx, realy)
    gl_finish()


# por renderizar una imagen negra con un punto blanco en cada esquina.
def bullet_two():
    gl_create_window(600, 800)
    gl_clear()
    filename('Puntos_Esquina.bmp')

    gl_view_port(0, 0, 599, 799)
    #Este es top right
    top_left_x = normalize(-1, 600)
    top_left_y = normalize(1, 800)

    top_right_x = normalize(1, 600)
    top_right_y = normalize(1, 800)

    bottom_left_x = normalize(-1, 600)
    bottom_left_y = normalize(-1, 800)

    bottom_right_x = normalize(1, 600)
    bottom_right_y = normalize(-1, 800)

    gl_vertex(top_left_x, top_left_y)
    gl_vertex(top_right_x, top_right_y)
    gl_vertex(bottom_left_x, bottom_left_y)
    gl_vertex(bottom_right_x, bottom_right_y)
    line(-1, -1, 1, 1)

    gl_finish()0


# por renderizar un cubo de 100 pixeles en el centro de su imagen.
#Basandose en el pseudocodigo del algoritmo de bresenham.
def line(startx, starty, endx, endy):

    dy = endy - starty
    dx = endx - startx

    slopey = 0
    slopex = 0
    if dy >= 0:
        slopey = 1
    else:
        dy = -dy
        slopey = -1

    if dx >= 0:
        slopex = 1
    else:
        dx = -dx
        slopex = -1

    #Incrementos de las secciones
    incrementX = 0
    incrementY = 0
    if dx >= dy:
        incrementY = 0
        incrementX = slopex
    else:
        incrementX = 0
        incrementY = slopey

        k = copy.copy(dx)
        dx = copy.copy(dy)
        dy = k

    # Inicializar valores

    X = startx
    Y = starty
    aVR = 2 * dy
    av = aVR - dx
    avI = av - dx

    #Dibujar la linea
    mayor = True
    if startx > endx:
        mayor = False

    replica = endx * -1
    if mayor:
        while startx < endx:
            if av >=0:
                X = X + slopex
                Y = Y + slopey
                av = av + avI
            else:
                X = X + incrementX
                Y = Y + incrementY
                av = av + aVR
            gl_vertex(X, Y)
    else:
        while startx < replica:
            if av >=0:
                X = X + slopex
                Y = Y + slopey
                av = av + avI
            else:
                X = X + incrementX
                Y = Y + incrementY
                av = av + aVR
            gl_vertex(X, Y)

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


bullet_one()
bullet_two()


