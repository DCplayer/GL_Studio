import struct
import numpy
from SR4 import obj

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

def length(v0):
    return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return [0, 0, 0]

    return [v0[0] / v0length,
            v0[1] / v0length,
            v0[2] / v0length]

def bbox(*vertices):
    xs = [ vertex[0] for vertex in vertices ]
    ys = [ vertex[1] for vertex in vertices ]
    xs.sort()
    ys.sort()

    return [[xs[0], ys[0]], [xs[-1], ys[-1]]]

def barycentric(A, B, C, P):
  bary = numpy.cross(
    [C[0] - A[0], B[0] - A[0], A[0] - P[0]],
    [C[1] - A[1], B[1] - A[1], A[1] - P[1]]
  )

  if abs(bary[2]) < 1:
    return -1, -1, -1   # this triangle is degenerate, return anything outside

  return (
    1 - (bary[0] + bary[1]) / bary[2],
    bary[1] / bary[2],
    bary[0] / bary[2]
  )



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


def gl_load_wf(filename, texture, translate, scale):
    bitmap.load(filename, translate=translate, scale=scale, texture=texture)

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

    def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
        # returns a vertex 3, translated and transformed
        return [
            round((vertex[0] + translate[0]) * scale[0]),
            round((vertex[1] + translate[1]) * scale[1]),
            round((vertex[2] + translate[2]) * scale[2])
        ]

    def triangle(self, A, B, C, color=None, texture=None, texture_coords=(), intensity=1):
        bbox_min, bbox_max = bbox(A, B, C)

        for x in range(bbox_min[0], bbox_max[0] + 1):
            for y in range(bbox_min[1], bbox_max[1] + 1):
                w, v, u = barycentric(A, B, C, [x, y])
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue

                if texture:
                    tA, tB, tC = texture_coords
                    tx = tA[0] * w + tB[0] * v + tC[0] * u
                    ty = tA[1] * w + tB[1] * v + tC[1] * u

                    color = texture.get_color(tx, ty, intensity)

                z = A.z * w + B.z * v + C.z * u

                if x < 0 or y < 0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.point(x, y, color)
                    self.zbuffer[x][y] = z

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), texture=None):
        model = obj.Obj(filename)
        light = [0, 0, 1]

        for face in model.vfaces:
            vcount = len(face)

            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                a = self.transform(model.vertices[f1], translate, scale)
                b = self.transform(model.vertices[f2], translate, scale)
                c = self.transform(model.vertices[f3], translate, scale)

                normal = norm(numpy.cross(numpy.subtract(b, a), numpy.subtract(c, a)))
                intensity = numpy.dot(normal, light)

                if not texture:
                    grey = round(255 * intensity)
                    if grey < 0:
                        continue
                    self.triangle(a, b, c, color=color(grey, grey, grey))
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    tA = []
                    tB = []
                    tC = []
                    tA = model.tvertices[t1]
                    tB = model.tvertices[t2]
                    tC = model.tvertices[t3]

                    self.triangle(a, b, c, texture=texture, texture_coords=(tA, tB, tC), intensity=intensity)


gl_create_window(1000, 1000)
gl_clear()
filename('Skull.bmp')
gl_view_port(0, 0, 999, 999)
textura = obj.Texture('12140_Skull_v3_L2.bmp')

gl_load_wf('12140_Skull_v3_L2.obj', textura , (0, 0, 0), (10, 10, 10))
gl_finish()
