import struct
from random import randint as random


def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    return bytes([b, g, r])


class GL_Studio:
    def __init__(self):
        pass

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

    def gl_color(self):
        pass

    def gl_finish(self):
        pass


class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

