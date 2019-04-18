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
    gl_line(-0.1, 0.1, 0.1, 0.1)
    gl_line(0.1, 0.1, 0.1, -0.1)
    gl_line(0.1, -0.1, -0.1, -0.1)
    gl_line(-0.1, -0.1, -0.1, 0.1)

    #Segundo Cuadro
    gl_line(-0.05, 0.15, 0.15, 0.15)
    gl_line(0.15, 0.15, 0.15, -0.05)
    gl_line(0.15, -0.05, -0.05, -0.05)
    gl_line(-0.05, -0.05, -0.05, 0.15)

    #Conexiones
    gl_line(-0.1, 0.1, -0.05, 0.15)
    gl_line(0.1, 0.1, 0.15, 0.15)
    gl_line(0.1, -0.1, 0.15, -0.05)
    gl_line(-0.1, -0.1, -0.05, -0.05)
    gl_finish()
    return


# por renderizar líneas blancas en toda la orilla de su imagen (4 lineas)
def bullet_four(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Bordes.bmp')

    gl_view_port(0, 0, width-1, width-1)

    gl_line(-1, 1, 1, 1)
    gl_line(1, 1, 1, -1)
    gl_line(1, -1, -1, -1)
    gl_line(-1, -1, -1, 1)

    gl_finish()
    return


# por renderizar una línea blanca en diagonal por el centro de su imagen.
def bullet_five(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Diagonal.bmp')

    gl_view_port(0, 0, width-1, width-1)
    gl_line(-1, -1, 1, 1)
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
                gl_color(pintura[0], pintura[1], pintura[2])
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

    gl_color(1, 1, 1)
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
            gl_line(x, y, x, y + 0.05)
            x = x+0.01
    return


# por crear una escena de 80 x 96 pixeles o 160 x 192 pixeles representando un frame de un juego de Atari. Sólo pueden
# usar los colores NTSC de
def bullet_nine(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('tempest.bmp')
    gl_view_port(0, 0, width-1, width-1)

    gl_color(0, 0, 1)

    #Cuadro Principal
    gl_line(-0.75, 0.5, 0.75, 0.5)
    gl_line(-0.75, 0.5, -0.75, -0.8)
    gl_line(-0.75, -0.8, 0.75, -0.8)
    gl_line(0.75, -0.8, 0.75, 0.5)

    #Segnudo Cuadro
    gl_line(-0.125, -0.5, 0.125, -0.5)
    gl_line(-0.125, -0.5, -0.125, -0.3)
    gl_line(-0.125, -0.3, 0.125, -0.3)
    gl_line(0.125, -0.3, 0.125, -0.5)

    #16 lineas
    gl_line(-0.75, 0.5, -0.125, -0.3)
    gl_line(-0.75, -0.8, -0.125, -0.5)
    gl_line(0.75, -0.8, 0.125, -0.5)

    gl_line(0, 0.5, 0, -0.3)
    gl_line(0.75, -0.15, 0.125, -0.4)
    gl_line(0, -0.5, 0, -0.8)
    gl_line(-0.75, -0.15, -0.125, -0.4)

    gl_line(-0.375, 0.5, -0.0625, -0.3)
    gl_line(0.375, 0.5, 0.0625, -0.3)
    gl_line(0.75, -0.475, 0.125, -0.45)
    gl_line(0.375, -0.8, 0.0625, -0.5)
    gl_line(-0.375, -0.8, -0.0625, -0.5)
    gl_line(-0.75, -0.475, -0.125, -0.45)
    gl_line(-0.75, 0.175, -0.125, -0.35)

    gl_color(0.898, 0.745, 0)
    gl_line(0.75, 0.175, 0.125, -0.35) #amarillo
    gl_line(0.75, 0.5, 0.125, -0.3) ##amarillo

    #Numeros
    gl_color(0.1412, 0.9059, 0.0667)
    #Unos (cuatro unos)
    gl_line(-0.45, 0.9, -0.45, 0.7)
    gl_line(0.27, 0.9, 0.27, 0.96)
    gl_line(0.17, 0.9, 0.17, 0.96)
    gl_line(0.37, 0.9, 0.37, 0.96)

    #Cinco
    gl_line(-0.13, 0.9, -0.23, 0.9)
    gl_line(-0.13, 0.8, -0.23, 0.8)
    gl_line(-0.13, 0.7, -0.23, 0.7)
    gl_line(-0.13, 0.81, -0.13, 0.7)
    gl_line(-0.23, 0.9, -0.23, 0.8)

    #Seis
    gl_line(-0.26, 0.7, -0.26, 0.81)
    gl_line(-0.36, 0.7, -0.26, 0.7)
    gl_line(-0.36, 0.8, -0.26, 0.8)
    gl_line(-0.36, 0.7, -0.36, 0.91)

    #Ceros (tres ceros)
    gl_line(0, 0.9, 0, 0.7)
    gl_line(0, 0.7, -0.1, 0.7)
    gl_line(-0.1, 0.7, -0.1, 0.9)
    gl_line(0, 0.9, -0.1, 0.9)
    x = normalize(0, width)
    y = normalize(0.9, height)
    gl_vertex(x, y)

    gl_line(0.2, 0.95, 0.25, 0.95)
    gl_line(0.25, 0.95, 0.25, 0.90)
    gl_line(0.25, 0.90, 0.2, 0.90)
    gl_line(0.2, 0.90, 0.2, 0.95)
    x = normalize(0.25, width)
    y = normalize(0.95, height)
    gl_vertex(x, y)

    gl_line(0.3, 0.95, 0.35, 0.95)
    gl_line(0.35, 0.95, 0.35, 0.90)
    gl_line(0.35, 0.90, 0.3, 0.90)
    gl_line(0.3, 0.90, 0.3, 0.95)
    x = normalize(0.35, width)
    y = normalize(0.95, height)
    gl_vertex(x, y)

    #Letra E
    gl_line(0.5, 0.9, 0.5, 0.95)
    gl_line(0.5, 0.9, 0.55, 0.9)
    gl_line(0.5, 0.95, 0.55, 0.95)
    gl_line(0.5, 0.925, 0.53, 0.925)

    #Letra J
    gl_line(0.56, 0.925, 0.58, 0.9)
    gl_line(0.58, 0.9, 0.6, 0.9)
    gl_line(0.6, 0.9, 0.6, 0.96)

    #Letra D
    gl_line(0.62, 0.9, 0.62, 0.95)
    gl_line(0.62, 0.9, 0.64, 0.9)
    gl_line(0.62, 0.95, 0.64, 0.95)
    gl_line(0.64, 0.95, 0.65, 0.930)
    gl_line(0.64, 0.9, 0.65, 0.920)
    gl_line(0.65, 0.930, 0.65, 0.920)

    #Nave Grande
    gl_color(1, 1, 0)
    gl_line(0.375, 0.5, 0.65625, 0.55)
    gl_line(0.65625, 0.55, 0.75, 0.5)
    gl_line(0.375, 0.5, 0.4875, 0.45)
    gl_line(0.4875, 0.45, 0.4, 0.5)
    gl_line(0.4, 0.5, 0.70, 0.51)
    gl_line(0.70, 0.51, 0.5625, 0.45)
    gl_line(0.5625, 0.45, 0.75, 0.5)

    #Nave pequeña 1
    gl_line(-0.5, 0.6, -0.60, 0.65)
    gl_line(-0.6, 0.65, -0.7, 0.6)
    gl_line(-0.7, 0.6, -0.64, 0.55)
    gl_line(-0.640, 0.55, -0.67, 0.6)
    gl_line(-0.69, 0.6, -0.53, 0.6)
    gl_line(-0.51, 0.6, -0.56, 0.55)
    gl_line(-0.56, 0.55, -0.5, 0.6)

    #Nave Pequeña 2
    gl_line(-0.75, 0.6, -0.85, 0.65)
    gl_line(-0.85, 0.65, -0.95, 0.6)
    gl_line(-0.95, 0.6, -0.89, 0.55)
    gl_line(-0.89, 0.55, -0.92, 0.6)
    gl_line(-0.92, 0.6, -0.80, 0.6)
    gl_line(-0.78, 0.6, -0.83, 0.55)
    gl_line(-0.83, 0.55, -0.75, 0.6)

    #Lineas rojas
    gl_color(1, 0, 0)
    gl_line(-0.0625, -0.5, 0.0625, -0.5)

    gl_finish()
    return




bullet_one(600, 800)
bullet_two(600, 800)
bullet_three(1000, 1000)
bullet_four(600, 800)
bullet_five(600, 800)
bullet_six(600, 800)
bullet_seven(600, 800)
bullet_eight(600, 800)
bullet_nine(160, 192)
