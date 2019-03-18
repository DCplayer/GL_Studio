import struct
from random import randint as random
import numpy as np


def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    return bytes([b, g, r])


class GL_Studio:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = np.zeros((height, width))
        print(self.pixels)

    def gl_init(self):
        pass

    def gl_create_window(self):
        pass

    def gl_view_port(self):
        pass

    def gl_clear(self):
        pass

    def gl_clear_color(self):
        pass

    def gl_vertex(self):
        pass

    def gl_color(self):
        pass

    def gl_finish(self):
        pass


class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.studio = GL_Studio()

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
                f.write(self.studio.pixels[i][j])

        f.close()

        def point(self, color, x, y):
            self.studio.pixels[x][y] = color
