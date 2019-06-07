from GL_Studio import *


def poligono(vertices, color):
    actual_color = make_color(color[0], color[1], color[2])
    print(vertices)
    print(len(vertices)-1)
    for i in range(len(vertices)-1):
        print("FROM: ", vertices[i][0], vertices[i][1], " TO: ", vertices[i + 1][0], vertices[i + 1][1])
        gl_line(vertices[i][0], vertices[i][1], vertices[i + 1][0], vertices[i + 1][1])
        get_color()
    gl_line(vertices[0][0], vertices[0][1], vertices[-1][0], vertices[-1][1])

width = 800
height = 800

gl_create_window(width, height)
gl_clear()
filename('Lampara.bmp')
gl_view_port(0, 0, width - 1, width - 1)


#Poligono 1
vertices = [[165, 380],
            [185, 360],
            [180, 330],
            [207, 345],
            [233, 330],
            [230, 360],
            [250, 380],
            [220, 385],
            [205, 410],
            [193, 383]]

poligono(vertices, (1, 1, 1))
xmin, xmax= sorted([i[0] for i in vertices])[0], sorted([i[0] for i in vertices])[-1]
ymin, ymax = sorted([i[1] for i in vertices])[0], sorted([i[1] for i in vertices])[-1]
gl_fill(xmin, xmax, ymin, ymax, 1)

#Poligono 2
vertices = [[321, 335],
            [288, 286],
            [339, 251],
            [374, 302]
            ]
poligono(vertices, (1, 1, 1))
xmin, xmax= sorted([i[0] for i in vertices])[0], sorted([i[0] for i in vertices])[-1]
ymin, ymax = sorted([i[1] for i in vertices])[0], sorted([i[1] for i in vertices])[-1]
gl_fill(xmin, xmax, ymin, ymax, 1)


#Poligono 3
vertices = [[377, 249],
            [411, 197],
            [436, 249]]
poligono(vertices, (1, 1, 1))
xmin, xmax= sorted([i[0] for i in vertices])[0], sorted([i[0] for i in vertices])[-1]
ymin, ymax = sorted([i[1] for i in vertices])[0], sorted([i[1] for i in vertices])[-1]
gl_fill(xmin, xmax, ymin, ymax, 1)


#Poligono 4
vertices = [[413, 177],
            [448, 159],
            [502, 88],
            [553, 53],
            [535, 36],
            [676, 37],
            [660, 52],
            [750, 145],
            [761, 179],
            [672, 192],
            [659, 214],
            [615, 214],
            [632, 230],
            [580, 230],
            [597, 215],
            [552, 214],
            [517, 144],
            [466, 180]
            ]
poligono(vertices, (1, 1, 1))
xmin, xmax= sorted([i[0] for i in vertices])[0], sorted([i[0] for i in vertices])[-1]
ymin, ymax = sorted([i[1] for i in vertices])[0], sorted([i[1] for i in vertices])[-1]
gl_fill(xmin, xmax, ymin, ymax, 1)

#Poligono 5
vertices = [[682, 175],
            [708, 120],
            [735, 148],
            [739, 170]
            ]
poligono(vertices, (1, 1, 1))
xmin, xmax= sorted([i[0] for i in vertices])[0], sorted([i[0] for i in vertices])[-1]
ymin, ymax = sorted([i[1] for i in vertices])[0], sorted([i[1] for i in vertices])[-1]
gl_fill(xmin, xmax, ymin, ymax, 2)


gl_finish()