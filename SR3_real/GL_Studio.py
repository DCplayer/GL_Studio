import struct
import numpy
from SR3_real import  obj

def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    return bytes([b, g, r])


bitmap = None
pos_x = None
pos_y = None
height = None
width = None
COLOR = color(0, 0, 0)


def getwidth():
    return width


def filename(name):
    global bitmap
    bitmap.filename = name


def normalize(x, dimension):
    return round((x+1) * dimension * 0.5)


def denormalize(x, dimension):
    return (float(x)/float(dimension*0.5)) -1


def gl_init():
    pass


def gl_create_window(w, h):
    global bitmap
    bitmap = Render(w, h)
    pass


def gl_view_port(x, y, param_width, param_height):
    global pos_x
    pos_x = x

    global pos_y
    pos_y = y

    global width
    width = param_width

    global height
    height = param_height


def gl_clear():
    global bitmap
    bitmap.clear()


def gl_clear_color(r, g, b):
    red = round(r * 255)
    green = round(g * 255)
    blue = round(b * 255)
    global COLOR
    bitmap.bk_color = color(red, green, blue)


def gl_vertex(x, y):
    real_x = x + pos_x
    real_y = y + pos_y
    bitmap.point(real_x, real_y)


def gl_color(r, g, b):
    red = round(r*255)
    green = round(g*255)
    blue = round(b*255)
    global bitmap
    bitmap.color = color(red, green, blue)


def get_color():
    print(COLOR)


def gl_finish():
    global bitmap
    bitmap.write()


def gl_line(startx, starty, endx, endy):
    bitmap.line(startx, starty, endx, endy, bitmap.width, bitmap.height)


def gl_load_wf(file, xT, yT, zT, xS, yS, zS, n, width, height):
    bitmap.load(file, xT, yT, zT, xS, yS, zS, n, width, height)

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixel = []
        self.array = numpy.array(self.pixel)
        self.color = color(255, 255, 255)
        self.bk_color = color(0, 0, 0)
        self.clear()
        self.filename = 'out.bmp'

    def write(self, filename):
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for i in range(self.height):
            for j in range(self.width):
                f.write(self.pixel[i][j])

        f.close()

    def point(self, x, y):
        if x < 0 or y < 0:
            return
        print("X: "+ str(x)+ ", Y: " + str(y))
        try:
            self.pixel[y][x] = self.color
            #print("X: " + str(x) + " Y: " + str(y))
        except IndexError:
            if x >= width:
                x = x-1
            if y >= height:
                y = y-1
            self.pixel[y][x] = self.color
            #print("X: " + str(x) + " Y: " + str(y))

    def clear(self):
        self.pixel = [
            [self.bk_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def lineLow(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        D = 2 * dy - dx
        y = y0

        x = x0
        for x in range(x, x1):
            gl_vertex(x, y)
            if D > 0:
                y = y + yi
                D = D - 2 * dx
            D = D + 2 * dy
        return

    def lineHigh(self, x0, y0, x1, y1):
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

    # por renderizar un cubo de 100 pixeles en el centro de su imagen.
    # Basandose en el pseudocodigo del algoritmo de bresenham.
    # https://es.wikipedia.org/wiki/Algoritmo_de_Bresenham
    def line(self, startx, starty, endx, endy, width, height):

        startx = normalize(startx, width)
        starty = normalize(starty, height)
        endx = normalize(endx, width)
        endy = normalize(endy, height)

        if abs(endy - starty) < abs(endx - startx):
            if startx > endx:
                self.lineLow(endx, endy, startx, starty)
            else:
                self.lineLow(startx, starty, endx, endy)
        else:
            if starty > endy:
                self.lineHigh(endx, endy, startx, starty)
            else:
                self.lineHigh(startx, starty, endx, endy)
        return

    def load(self, file, xtrans, ytrans, ztrans, xscale, yscale, zscale, norm, width, height):
        x = obj.Obj(file)

        for face in x.caras:
            cara1 = int(face[0])
            cara2 = int(face[1])
            cara3 = int(face[2])

            vertexSet = [x.vertex[cara1 - 1], x.vertex[cara2 - 1], x.vertex[cara3 - 1]]

            for i in range(len(vertexSet)):
                print(vertexSet)
                if i == 2:
                    x1 = (float(vertexSet[i][0]) * xscale) + xtrans
                    y1 = (float(vertexSet[i][1]) * yscale) + ytrans

                    x2 = (float(vertexSet[0][0]) * xscale) + xtrans
                    y2 = (float(vertexSet[0][1]) * yscale) + ytrans
                    if norm:
                        x1 = denormalize(x1, width)
                        x2 = denormalize(x2, width)
                        y1 = denormalize(y1, height)
                        y2 = denormalize(y2, height)
                        gl_line(x1, y1, x2, y2)
                    else:
                        gl_line(x1, y1, x2, y2)


                else:
                    x1 = (float(vertexSet[i][0]) * xscale) + xtrans
                    y1 = (float(vertexSet[i][1]) * yscale) + ytrans

                    x2 = (float(vertexSet[i + 1][0]) * xscale) + xtrans
                    y2 = (float(vertexSet[i + 1][1]) * yscale) + ytrans
                    if norm:
                        x1 = denormalize(x1, width)
                        x2 = denormalize(x2, width)
                        y1 = denormalize(y1, height)
                        y2 = denormalize(y2, height)
                        gl_line(x1, y1, x2, y2)
                    else:
                        x1 = normalize(x1, width)
                        x2 = normalize(x2, width)
                        y1 = normalize(y1, height)
                        y2 = normalize(y2, height)
                        gl_line(x1, y1, x2, y2)
