import struct


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
    return  width

def filename(name):
    global bitmap
    bitmap.filename = name


def normalize(x, dimension):
    return round((x+1) * dimension * 0.5)


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
    COLOR = color(red, green, blue)


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


def gl_finish():
    global bitmap
    bitmap.write()


class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixel = []
        self.color = color(255, 255, 255)
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
        except IndexError:
            if x != 0:
                x = x-1
            if y != 0:
                y = y-1
            self.pixel[y][x] = self.color

    def clear(self):
        self.pixel = [
            [COLOR for x in range(self.width)]
            for y in range(self.height)
        ]
