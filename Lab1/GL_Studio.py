import struct
import numpy


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

    def write(self):
        f = open(self.filename, 'bw')

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
