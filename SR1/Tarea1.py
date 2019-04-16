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

    gl_finish()


def bullet_three(width, height):
    gl_create_window(width, width)
    gl_clear()
    filename('Cubo.bmp')

    gl_view_port(0, 0, width-1, width-1)

    #Primer Cuadrado
    line(-0.1, 0.1, 0.1, 0.1, width, height)
    line(0.1, 0.1, 0.1, -0.1, width, height)
    line(0.1, -0.1, -0.1, -0.1, width, height)
    line(-0.1, -0.1, -0.1, 0.1, width, height)

    #Segundo Cuadro
    line(-0.05, 0.15, 0.15, 0.15, width, height)
    line(0.15, 0.15, 0.15, -0.05, width, height)
    line(0.15, -0.05, -0.05, -0.05, width, height)
    line(-0.05, -0.05, -0.05, 0.15, width, height)

    #Conexiones
    line(-0.1, 0.1, -0.05, 0.15, width, height)
    line(0.1, 0.1, 0.15, 0.15, width, height)
    line(0.1, -0.1, 0.15, -0.05, width, height)
    line(-0.1, -0.1, -0.05, -0.05, width, height)
    gl_finish()
    return


# por renderizar líneas blancas en toda la orilla de su imagen (4 lineas)
def bullet_four(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Bordes.bmp')

    gl_view_port(0, 0, width-1, width-1)

    line(-1, 1, 1, 1, width, height)
    line(1, 1, 1, -1, width, height)
    line(1, -1, -1, -1, width, height)
    line(-1, -1, -1, 1, width, height)

    gl_finish()
    return


# por renderizar una línea blanca en diagonal por el centro de su imagen.
def bullet_five(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Diagonal.bmp')

    gl_view_port(0, 0, width-1, width-1)
    line(-1, -1, 1, 1, width, height)
    gl_finish()

    return


# por llenar su imagen entera de puntos blancos y negros (las posibilidades de que un punto sea blanco o negro son de
# 50%)
def bullet_six(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Random.bmp')

    gl_view_port(0, 0, width-1, width-1)
    for x in range(width):
        for y in range(height):
            number = random.randint(0, 1)
            if number:
                gl_vertex(x, y)
    gl_finish()
    return


# por llenar su imagen entera de puntos de colores random
def bullet_seven(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Random_Colors.bmp')

    gl_view_port(0, 0, width-1, width-1)
    for x in range(width):
        for y in range(height):
            number = random.randint(0, 1)
            if number:
                pintura = random_color()
                gl_clear_color(pintura[0], pintura[1], pintura[2])
                gl_vertex(x, y)
    gl_finish()
    return


def random_color():
    return [round(random.random()), round(random.random()), round(random.random())]


# por crear una escena de un cielo con estrellas
def bullet_eight(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('stars.bmp')

    gl_clear_color(1, 1, 1)
    get_color()

    gl_view_port(0, 0, width-1, width-1)
    for x in range(width):
        for y in range(height):
            estrella = random.random()
            if estrella > 0.988:
                tamanio = random.random()
                if tamanio < 0.33:
                    gl_vertex(x, y)
                elif 0.33 <= tamanio < 0.66:
                    gl_vertex(x, y)

                else:
                    gl_vertex(x, y)

    gl_finish()
    return


def cuadrado(x, y, width, height, size):
    x = denormalize(x, width)
    y = denormalize(y, height)
    if y < 0.95:
        for i in range(size):
            line(x, y, x, y + 0.05, width, height)
            x = x+0.01
    return


# por crear una escena de 80 x 96 pixeles o 160 x 192 pixeles representando un frame de un juego de Atari. Sólo pueden
# usar los colores NTSC de
def bullet_nine(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('tempest.bmp')
    gl_view_port(0, 0, width-1, width-1)

    gl_clear_color(0, 0, 1)

    #Cuadro Principal
    line(-0.75, 0.5, 0.75, 0.5, width, height)
    line(-0.75, 0.5, -0.75, -0.8, width, height)
    line(-0.75, -0.8, 0.75, -0.8, width, height)
    line(0.75, -0.8, 0.75, 0.5, width, height)

    #Segnudo Cuadro
    line(-0.125, -0.5, 0.125, -0.5, width, height)
    line(-0.125, -0.5, -0.125, -0.3, width, height)
    line(-0.125, -0.3, 0.125, -0.3, width, height)
    line(0.125, -0.3, 0.125, -0.5, width, height)

    #16 lineas
    line(-0.75, 0.5, -0.125, -0.3, width, height)
    line(-0.75, -0.8, -0.125, -0.5, width, height)
    line(0.75, -0.8, 0.125, -0.5, width, height)

    line(0, 0.5, 0, -0.3, width, height)
    line(0.75, -0.15, 0.125, -0.4, width, height)
    line(0, -0.5, 0, -0.8, width, height)
    line(-0.75, -0.15, -0.125, -0.4, width, height)

    line(-0.375, 0.5, -0.0625, -0.3, width, height)
    line(0.375, 0.5, 0.0625, -0.3, width, height)
    line(0.75, -0.475, 0.125, -0.45, width, height)
    line(0.375, -0.8, 0.0625, -0.5, width, height)
    line(-0.375, -0.8, -0.0625, -0.5, width, height)
    line(-0.75, -0.475, -0.125, -0.45, width, height)
    line(-0.75, 0.175, -0.125, -0.35, width, height)

    gl_clear_color(0.898, 0.745, 0)
    line(0.75, 0.175, 0.125, -0.35, width, height) #amarillo
    line(0.75, 0.5, 0.125, -0.3, width, height) ##amarillo

    #Numeros
    gl_clear_color(0.1412, 0.9059, 0.0667)
    #Unos (cuatro unos)
    line(-0.45, 0.9, -0.45, 0.7, width, height)
    line(0.27, 0.9, 0.27, 0.96, width, height)
    line(0.17, 0.9, 0.17, 0.96, width, height)
    line(0.37, 0.9, 0.37, 0.96, width, height)

    #Cinco
    line(-0.13, 0.9, -0.23, 0.9, width, height)
    line(-0.13, 0.8, -0.23, 0.8, width, height)
    line(-0.13, 0.7, -0.23, 0.7, width, height)
    line(-0.13, 0.81, -0.13, 0.7, width, height)
    line(-0.23, 0.9, -0.23, 0.8, width, height)

    #Seis
    line(-0.26, 0.7, -0.26, 0.81, width, height)
    line(-0.36, 0.7, -0.26, 0.7, width, height)
    line(-0.36, 0.8, -0.26, 0.8, width, height)
    line(-0.36, 0.7, -0.36, 0.91, width, height)

    #Ceros (tres ceros)
    line(0, 0.9, 0, 0.7, width, height)
    line(0, 0.7, -0.1, 0.7, width, height)
    line(-0.1, 0.7, -0.1, 0.9, width, height)
    line(0, 0.9, -0.1, 0.9, width, height)
    x = normalize(0, width)
    y = normalize(0.9, height)
    gl_vertex(x, y)

    line(0.2, 0.95, 0.25, 0.95, width, height)
    line(0.25, 0.95, 0.25, 0.90, width, height)
    line(0.25, 0.90, 0.2, 0.90, width, height)
    line(0.2, 0.90, 0.2, 0.95, width, height)
    x = normalize(0.25, width)
    y = normalize(0.95, height)
    gl_vertex(x, y)

    line(0.3, 0.95, 0.35, 0.95, width, height)
    line(0.35, 0.95, 0.35, 0.90, width, height)
    line(0.35, 0.90, 0.3, 0.90, width, height)
    line(0.3, 0.90, 0.3, 0.95, width, height)
    x = normalize(0.35, width)
    y = normalize(0.95, height)
    gl_vertex(x, y)

    #Letra E
    line(0.5, 0.9, 0.5, 0.95, width, height)
    line(0.5, 0.9, 0.55, 0.9, width, height)
    line(0.5, 0.95, 0.55, 0.95, width, height)
    line(0.5, 0.925, 0.53, 0.925, width, height)

    #Letra J
    line(0.56, 0.925, 0.58, 0.9, width, height)
    line(0.58, 0.9, 0.6, 0.9, width, height)
    line(0.6, 0.9, 0.6, 0.96, width, height)

    #Letra D
    line(0.62, 0.9, 0.62, 0.95, width, height)
    line(0.62, 0.9, 0.64, 0.9, width, height)
    line(0.62, 0.95, 0.64, 0.95, width, height)
    line(0.64, 0.95, 0.65, 0.930, width, height)
    line(0.64, 0.9, 0.65, 0.920, width, height)
    line(0.65, 0.930, 0.65, 0.920, width, height)

    #Nave Grande

    #Nave pequeña 1

    #Nave Pequeña 2



    gl_finish()
    return


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
    for x in range(x, x1):
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
    for y in range(y, y1):
        gl_vertex(x, y)
        if D > 0:
            x = x + xi
            D = D - 2 * dy
        D = D + 2 * dx
    return


#bullet_one(600, 800)
#bullet_two(600, 800)
#bullet_three(1000, 1000)
#bullet_four(600, 800)
#bullet_five(600, 800)
#bullet_six(600, 800)
#bullet_seven(600, 800)
#bullet_eight(600, 800)
bullet_nine(160, 192)
