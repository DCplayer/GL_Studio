from GL_Studio import *
import random



# por renderizar una imagen negra con un punto blanco en una ubicación random dentro de la imagen.
def bullet_one():

    gl_create_window(600, 800)
    filename('Punto_Random.bmp')

    gl_view_port(0, 0, 600, 800)
    thisy = random.uniform(-1, 1)
    thisx = random.uniform(-1, 1)
    realx = normalize(thisx, 600)
    realy = normalize(thisy, 800)
    gl_vertex(realx, realy)
    gl_finish()

# por renderizar una imagen negra con un punto blanco en cada esquina.
def bullet_two(x):
    pass


# por renderizar un cubo de 100 pixeles en el centro de su imagen.
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

