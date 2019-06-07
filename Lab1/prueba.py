
import struct
from random import randint
from collections import namedtuple
import obj


def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    return bytes([b, g, r])


v2 = namedtuple('Vertex2', ['x', 'y'])
v3 = namedtuple('Vertex3', ['x', 'y', 'z'])




class Bitmap(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.clear()

    def clear(self):
        self.framebuffer = [
            [
                color(0, 0, 0)
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # File Header 14
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header 40
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

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

    def glVertex(self, x, y):

        xw = (self.xnd) + ((self.vWidth) / 2) + x
        yw = (self.ynd) + ((self.vHeight) / 2) + y

        self.xw = xw

        puntoX = int((xw + (self.vWidth / 2 * x)))
        puntoY = int((yw + (self.vHeight / 2 * y)))

        self.puntoX = puntoX
        self.puntoY = puntoY

        self.point(puntoX, puntoY)

    def glCreateWindow(self, x, y):
        # Crea una ventana de ancho x y de alto y
        self.x = x
        self.y = y

    def glViewPort(self, xnd, ynd, vWidth, vHeight):
        # Se toma el espacio del dispositivo x,y
        self.xnd = xnd
        self.ynd = ynd
        self.vWidth = vWidth
        self.vHeight = vHeight

    def glColor(self, r, g, b):
        self.rVertex = round(255 * r)
        self.gVertex = round(255 * g)
        self.bVertex = round(255 * b)

    def glFinish(self, name):
        self.write(name + ".bmp")

    def point(self, x, y):
        self.framebuffer[y][x] = color(self.rVertex, self.gVertex, self.bVertex)

    def glClear(self, red, green, blue):
        self.framebuffer = [
            [
                color(red, green, blue)
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        try:
            self.rColor = round(255 * r)
            self.gColor = round(255 * g)
            self.bColor = round(255 * b)
            self.glClear(self.rColor, self.gColor, self.bColor)

        except ValueError:
            print("No se aceptan valores mayores a 1 o menores a 0, vuelva a ingresarlos")

    def randomPoint(self, x, y):
        # Coordenadas del punto en X y Y
        xp = randint(0, x)
        yp = randint(0, y)
        self.framebuffer[yp][xp] = color(255, 255, 255)

    def polygon(self, x1, y1):
        self.point(x1, y1)

    def convertidor(self, x, y, x_2, y_2, width, height):
        xN = ((x - (width / 2)) / (width / 2))
        yN = ((y - (height / 2)) / (height / 2))
        xM = ((x_2 - (width / 2)) / (width / 2))
        yM = ((y_2 - (height / 2)) / (height / 2))

        return xN, yN, xM, yM

    def desconvertidor(self, x3, y3, x_4, y_4, width, height):
        xN = (x3 * (width / 2) + (width / 2))
        yN = (y3 * (height / 2) + (height / 2))
        xM = (x_4 * (width / 2) + (width / 2))
        yM = (y_4 * (height / 2) + (height / 2))

        return xN, yN, xM, yM

    def glLine(self, x1, y1, x2, y2):
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        try:
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)

            steep = dy > dx

            if steep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2

            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            dy = abs(y2 - y1)
            dx = abs(x2 - x1)

            offset = 0 * 2 * dx
            threshold = 0.5 * 2 * dx

            y = y1
            while x1 <= (x2 + 1):
                if steep:
                    self.point(y, x1)
                else:
                    self.point(x1, y)
                offset += dy

                if offset >= threshold:
                    y += 1 if y1 < y2 else -1
                    threshold += 1 * dx
                x1 = x1 + 1

        except ValueError:
            print("No se aceptan valores mayores a 1 o menores a -1, vuelva a ingresarlos")

    def rellenar(self, xMin, xMax, yMin, yMax):

        for y in range(yMin, yMax):

            contador = 0
            xin = 0
            xfin = 0
            for x in range(xMin, xMax + 1):

                if (self.framebuffer[y][x] == color(self.rVertex, self.gVertex, self.bVertex) and contador == 0):
                    self.point(x, y)
                    xin = x
                    x += 1
                    contador += 1

                if (self.framebuffer[y][x] == color(self.rVertex, self.gVertex, self.bVertex) and contador == 1):
                    self.point(x, y)
                    xfin = x
                    contador += 1

                # if(self.framebuffer[y][x] == color(255,255,255) and self.framebuffer[y][x+1] == color(255,255,255)):
                #    contador =1

                if (self.framebuffer[y][x] == color(self.rVertex, self.gVertex, self.bVertex) and self.framebuffer[y][
                    x - 1] == color(self.rVertex, self.gVertex, self.bVertex) and contador >= 1):
                    contador = 1
                    xin = x

                if ((xin != xMin and xin != 0) and (xfin != xMax and xfin != 0) and contador == 2):
                    self.glLine(xin, y, xfin, y)

    def rellenoInv(self, xMin, xMax, yMin, yMax):

        for y in range(yMin, yMax):

            contador = 0
            xin = 0
            xfin = 0
            for x in range(xMin, xMax + 1):

                if (self.framebuffer[y][x] == color(0, 0, 0) and contador == 0):
                    self.point(x, y)
                    xin = x
                    x += 1
                    contador += 1

                if (self.framebuffer[y][x] == color(0, 0, 0) and contador == 1):
                    self.point(x, y)
                    xfin = x
                    contador += 1

                if ((xin != xMin and xin != 0) and (xfin != xMax and xfin != 0) and contador == 2):
                    self.glLine(xin, y, xfin, y)

    def rellenoInvTri(self, xMin, xMax, yMin, yMax):

        for y in range(yMin, yMax):

            contador = 0
            xin = 0
            xfin = 0
            for x in range(xMin, xMax + 1):

                if (self.framebuffer[y][x] == color(0, 0, 0) and contador == 0):
                    self.point(x, y)
                    xin = x
                    x += 1
                    contador += 1

                if (self.framebuffer[y][x] == color(0, 0, 0) and contador == 1):
                    self.point(x, y)
                    xfin = x
                    contador += 1

                # if(self.framebuffer[y][x] == color(255,255,255) and self.framebuffer[y][x+1] == color(255,255,255)):
                #    contador =1

                if (self.framebuffer[y][x] == color(0, 0, 0) and self.framebuffer[y][x - 1] == color(0, 0, 0)):
                    contador = 1
                    xin = x

                if ((xin != xMin and xin != 0) and (xfin != xMax and xfin != 0) and contador == 2):
                    self.glLine(xin, y, xfin, y)

    def paintTriangle(self, A, B, C):
        if (A.y > B.y):
            A, B = B, A
        if (A.y > C.y):
            A, C = C, A
        if (B.y > C.y):
            B, C = C, B

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y

        mi_ac = dx_ac / dy_ac

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y

        mi_ab = dx_ab / dy_ab

        for y in range(A.y, B.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(A.x - mi_ab * (A.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)

        dx_bc = C.x - B.x
        dy_bc = C.y - B.y

        mi_bc = dx_bc / dy_bc

        for y in range(B.y, C.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(B.x - mi_bc * (B.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)

    def glTriangle(self, a, b, c):
        # ordenar vertices por altura
        if (a.y > b.y):
            a, b = b, a
        if (a.y > c.y):
            a, c = c, a
        if (b.y > c.y):
            b, c = c, b

        # pendientes de a c
        dx_ac = c.x - a.x
        dy_ac = c.y - a.y
        if (dy_ac == 0):
            mi_ac = 0
        else:
            mi_ac = dx_ac / dy_ac

        # pendientes de a b
        dx_ab = b.x - a.x
        dy_ab = b.y - a.y
        if (dy_ab == 0):
            mi_ab = 0
        else:
            mi_ab = dx_ab / dy_ab

        # pendientes de b c
        dx_bc = c.x - b.x
        dy_bc = c.y - b.y
        if (dy_bc == 0):
            mi_bc = 0
        else:
            mi_bc = dx_bc / dy_bc

        for y in range(a.y, b.y + 1):
            xi = round(a.x - mi_ac * (a.y - y))
            xf = round(a.x - mi_ab * (a.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)

        for y in range(b.y, c.y + 1):
            xi = round(a.x - mi_ac * (a.y - y))
            xf = round(b.x - mi_bc * (b.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)

    # Vectores
    # def sum(v0, v1):
    #    V2=(v0.x + v1.x,v0.y + v1.y,v0.z + v1.z)

    # def sub(v0, v1):

    # def mul(v0, v1):

    # def dot(v0, v1):


ancho = 800
alto = 500

r = Bitmap(ancho, alto)

r.glViewPort(0, 0, 600, 500)

# Poligono1
r.glColor(0, 0, 1)
r.point(165, 380)
r.point(185, 360)
r.point(180, 330)
r.point(207, 345)
r.point(233, 330)
r.point(230, 360)
r.point(250, 380)
r.point(220, 385)
r.point(205, 410)
r.point(193, 383)

# contorno
r.glLine(165, 380, 185, 360)
r.glLine(185, 360, 180, 330)
r.glLine(180, 330, 207, 345)
r.glLine(207, 345, 233, 330)
r.glLine(233, 330, 230, 360)
r.glLine(230, 360, 250, 380)
r.glLine(250, 380, 220, 385)
r.glLine(220, 385, 205, 410)
r.glLine(205, 410, 193, 383)
r.glLine(165, 380, 193, 383)

r.rellenar(165, 250, 331, 410)

r.glColor(0, 0, 0)
r.glLine(180, 330, 233, 330)
r.glLine(180, 330, 207, 345)
r.glLine(233, 330, 207, 345)

r.rellenoInvTri(181, 233, 330, 345)

# Poligono4
r.glColor(1, 1, 0)
r.point(413, 177)
r.point(448, 159)
r.point(502, 88)
r.point(553, 53)
r.point(535, 36)
r.point(676, 37)
r.point(660, 52)
r.point(750, 145)
r.point(761, 179)
r.point(672, 192)
r.point(659, 214)
r.point(615, 214)
r.point(632, 230)
r.point(580, 230)
r.point(597, 215)
r.point(552, 214)
r.point(517, 144)
r.point(466, 180)

# contorno
r.glLine(413, 177, 448, 159)
r.glLine(448, 159, 502, 88)
r.glLine(502, 88, 553, 53)
r.glLine(553, 53, 535, 36)
r.glLine(535, 36, 676, 37)
r.glLine(676, 37, 660, 52)
r.glLine(660, 52, 750, 145)
r.glLine(750, 145, 761, 179)
r.glLine(761, 179, 672, 192)
r.glLine(672, 192, 659, 214)
r.glLine(659, 214, 615, 214)
r.glLine(615, 214, 632, 230)
r.glLine(632, 230, 580, 230)
r.glLine(580, 230, 597, 215)
r.glLine(597, 215, 552, 214)
r.glLine(552, 214, 517, 144)
r.glLine(517, 144, 466, 180)
r.glLine(466, 180, 413, 177)

# pintar
r.rellenar(413, 761, 36, 230)

# cubrir un espacio en negro
r.glColor(0, 0, 0)
r.glLine(517, 144, 466, 180)
r.glLine(517, 144, 534, 180)
r.glLine(466, 180, 534, 180)

r.rellenoInvTri(466, 534, 145, 180)

# Poligono5
r.point(682, 175)
r.point(708, 120)
r.point(735, 148)
r.point(739, 170)

r.glLine(682, 175, 708, 120)
r.glLine(708, 120, 735, 148)
r.glLine(735, 148, 739, 170)
r.glLine(739, 170, 682, 175)

r.rellenoInv(682, 739, 122, 175)

# Poligono2
r.glColor(0, 1, 1)
r.point(321, 335)
r.point(288, 286)
r.point(339, 251)
r.point(374, 302)

# contorno
r.glLine(321, 335, 288, 286)
r.glLine(288, 286, 339, 251)
r.glLine(339, 251, 374, 302)
r.glLine(374, 302, 321, 335)

# pintar
r.rellenar(288, 374, 251, 335)

# Poligono3
r.glColor(0, 1, 0)
r.point(377, 249)
r.point(411, 197)
r.point(436, 249)

# contorno
r.glLine(377, 249, 411, 197)
r.glLine(411, 197, 436, 249)
r.glLine(436, 249, 377, 249)

# pintar
r.rellenar(377, 436, 197, 249)

r.glFinish("Lab1")