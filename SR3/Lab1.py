from GL_Studio import *


#Se usara un lienzo de 800 x 800
def line_product(startx, starty, endx, endy, width, height):
    startx = denormalize(startx, width)
    endx = denormalize(endx, width)
    starty = denormalize(starty, height)
    endy = denormalize(endy, height)

    print("Startx: " +str(startx)+ ", Starty: " +str(starty)+ ", Endx: " +str(endx)+ ", Endy: " + str(endy))
    gl_line(startx, starty, endx, endy)

    return


def draw_simulator(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Lampara.bmp')
    gl_view_port(0, 0, width-1, width-1)

    #poligono1
    line_product(165, 380, 185, 360, width, height)
    line_product(185, 360, 180, 330, width, height)
    line_product(180, 330, 207, 345, width, height)
    line_product(207, 345, 233, 330, width, height)
    line_product(233, 330, 230, 360, width, height)
    line_product(230, 360, 250, 380, width, height)
    line_product(250, 380, 220, 385, width, height)
    line_product(220, 385, 205, 410, width, height)
    line_product(205, 410, 193, 383, width, height)
    line_product(193, 383, 165, 380, width, height)

    #poligono2
    line_product(321, 335, 288, 286, width, height)
    line_product(288, 286, 339, 251, width, height)
    line_product(339, 251, 374, 302, width, height)
    line_product(374, 302, 321, 335, width, height)

    #poligono 3
    line_product(377, 249, 411, 197, width, height)
    line_product(411, 197, 436, 249, width, height)
    line_product(436, 249, 377, 249, width, height)

    #poligono 4
    line_product(413, 177, 448, 159, width, height)
    line_product(448, 159, 502, 88, width, height)
    line_product(502, 88, 553, 53, width, height)
    line_product(553, 53, 535, 36, width, height)
    line_product(535, 36, 676, 37, width, height)
    line_product(676, 37, 660, 52, width, height)
    line_product(660, 52, 750, 145, width, height)
    line_product(750, 145, 761, 179, width, height)
    line_product(761, 179, 672, 192, width, height)
    line_product(672, 192, 659, 214, width, height)
    line_product(659, 214, 615, 214, width, height)
    line_product(615, 214, 632, 230, width, height)
    line_product(632, 230, 580, 230, width, height)
    line_product(580, 230, 597, 215, width, height)
    line_product(597, 215, 552, 214, width, height)
    line_product(552, 214, 517, 144, width, height)
    line_product(517, 144, 466, 180, width, height)
    line_product(466, 180, 413, 177, width, height)

    #poligono 5
    line_product(682, 175, 708, 120, width, height)
    line_product(708, 120, 735, 148, width, height)
    line_product(735, 148, 739, 170, width, height)
    line_product(739, 170, 682, 175, width, height)

    gl_finish()
    return


draw_simulator(800, 500)