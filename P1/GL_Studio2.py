import glm
import pygame
import os
import pywavefront
import random
import obj

class Render(object):
    def __init__(self, surface):
        self.surface = surface
        self.vertices = []
        self.normals = []
        self.t_vertices = []
        self.zbuffer = [
            [-999 for x in range(self.surface.get_width())]
            for y in range(self.surface.get_height())
        ]

    def point(self, x, y, c):
        self.surface.set_at((int(x), int(y)), c)

    def load(self, filename, trans, rot, scale, whereami, lookat):
        model = obj.Obj(filename)

        vertices = []
        t_vertices = []
        n_vertices = []

        for face in model.vfaces:
            vcount = len(face)
            if vcount >= 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                f1t = face[0][1] - 1
                f2t = face[1][1] - 1
                f3t = face[2][1] - 1

                f1n = face[0][2] - 1
                f2n = face[1][2] - 1
                f3n = face[2][2] - 1

                vertices.append(model.vertices[f1])
                vertices.append(model.vertices[f2])
                vertices.append(model.vertices[f3])

                try:
                    t_vertices.append(glm.vec2(*model.tvertices[f1t]))
                    t_vertices.append(glm.vec2(*model.tvertices[f2t]))
                    t_vertices.append(glm.vec2(*model.tvertices[f3t]))
                except TypeError:
                    t_vertices.append(glm.vec3(*model.tvertices[f1t]))
                    t_vertices.append(glm.vec3(*model.tvertices[f2t]))
                    t_vertices.append(glm.vec3(*model.tvertices[f3t]))

                n_vertices.append((glm.vec3(*model.normals[f1n])))
                n_vertices.append((glm.vec3(*model.normals[f2n])))
                n_vertices.append((glm.vec3(*model.normals[f3n])))

        self.vertices = iter(self.transform(vertices, trans, rot, scale, whereami, lookat))
        self.t_vertices = iter(t_vertices)
        self.normals = iter(n_vertices)


    #all menos los verices son VEC3
    def transform(self, vertices, trans, rot, scale, whereami, lookat):
        newvertex = []

        i = glm.mat4(1)
        translate = glm.translate(i, trans)
        rotate = glm.rotate(i, glm.radians(0), glm.vec3(1, 0, 0))
        if rot.x != 0:
            rotate = glm.rotate(rotate, glm.radians(rot.x), glm.vec3(1, 0, 0))
        if rot.y != 0:
            rotate = glm.rotate(rotate, glm.radians(rot.y), glm.vec3(0, 1, 0))
        if rot.z != 0:
            rotate = glm.rotate(rotate, glm.radians(rot.z), glm.vec3(0, 0, 1))

        scale = glm.scale(i, scale)
        model = translate * rotate * scale
        #Donde estoy, donde apunta la camara y Que es arriba
        view = glm.lookAt(whereami, lookat, glm.vec3(0, 1, 0))

        projection = glm.mat4(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, -0.001,
            0, 0, 0, 1
        )


        viewport = glm.mat4(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            self.surface.get_width()/2, self.surface.get_height()/2, 128, 1
        )


        matrix = viewport * projection * view * model

        for vertex in vertices:
            vertex = glm.vec4(*vertex, 1)
            # vertex = vertex * 100 + 400
            transformed_vertex = matrix * vertex
            newvertex.append(
                glm.vec3(
                    transformed_vertex.x / transformed_vertex.w,
                    transformed_vertex.y / transformed_vertex.w,
                    transformed_vertex.z / transformed_vertex.w
                )
            )
            # print(newvertex)
        return newvertex

    def draw(self, light):
        try:
            while True:
                self.triangle(light)
        except StopIteration:
            print('Done.')

    def triangle(self, light):
        A = next(self.vertices)
        B = next(self.vertices)
        C = next(self.vertices)

        At = next(self.t_vertices)
        Bt = next(self.t_vertices)
        Ct = next(self.t_vertices)

        na = next(self.normals)
        nb = next(self.normals)
        nc = next(self.normals)

        c = (255, 0, 0)

        xs = sorted([A.x, B.x, C.x])
        ys = sorted([A.y, B.y, C.y])

        xmin = int(xs[0])
        xmax = int(xs[-1]) + 1
        ymin = int(ys[0])
        ymax = int(ys[-1]) + 1


        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                w, v, u = self.barycentric(A, B, C, (x,y))
                if w < 0 or v < 0 or u < 0:
                    continue

                z = A.z * w + B.z * v + C.z * u
                try:
                    if self.zbuffer[x][y] < z:
                        self.zbuffer[x][y] = z

                        if self.current_texture:
                            tx = At.x * w + Bt.x * v + Ct.x * u
                            ty = At.y * w + Bt.y * v + Ct.y * u
                            tx = int(tx * (self.current_texture.get_width() - 1))
                            ty = int(ty * (self.current_texture.get_height() - 1))
                            c = self.current_texture.get_at((tx, ty))

                        color = self.shader(
                            (A, B, C),
                            (x, y),
                            (w, v, u),
                            c,
                            (0, 0, 1),
                            (na, nb, nc),
                            light
                        )

                        self.point(x, y, color)
                except:
                    pass

    def shader(self, trian, p, bari, c, light, normals, lettherebelight):

        nA, nB, nC = normals
        w, v, u =  bari

        nx = nA.x * w + nB.x * v + nC.x * u
        ny = nA.y * w + nB.y * v + nC.y * u
        nz = nA.z * w + nB.z * v + nC.z * u

        normal = (nx, ny, nz)
        intensity = 1
        if lettherebelight:
            intensity = glm.dot(normal, light)

        r = min(max(c[0] * intensity, 0), 255)
        g = min(max(c[1] * intensity, 0), 255)
        b = min(max(c[2] * intensity, 0), 255)
        c = glm.vec3(r, g, b)
        return c


    def barycentric(self, A, B, C, P):
        bary = glm.cross(
            [C[0] - A[0], B[0] - A[0], A[0] - P[0]],
            [C[1] - A[1], B[1] - A[1], A[1] - P[1]]
        )
        if abs(bary[2]) < 1:
            return -1, -1, -1  # this triangle is degenerate, return anything outside

        return (
            1 - (bary[0] + bary[1]) / bary[2],
            bary[1] / bary[2],
            bary[0] / bary[2]
        )

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
s = pygame.display.set_mode((1400, 1400), pygame.DOUBLEBUF|pygame.HWACCEL) #, pygame.FULLSCREEN)

fondo = Render(s)
#trans, rot, scale, whereami, lookat
fondo.load('./cueva/Cubo.obj', glm.vec3(3500, -1000, 6000), glm.vec3(0, 0, 90), glm.vec3(4000, 4000, 4000), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
fondo.current_texture = pygame.image.load('./cueva/cueva.bmp')
fondo.draw(False)

# Ogro lejano
#trans, rot, scale, whereami, lookat
fondo.load('./Ogro/Ogro.obj', glm.vec3(200, -50, 900), glm.vec3(180, -25, 0), glm.vec3(100, 100, 100), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
fondo.current_texture = pygame.image.load('./Ogro/SkinColorMostro_COLOR.bmp')
fondo.draw(True)


# Ogro Cercano
#trans, rot, scale, whereami, lookat
fondo.load('./Ogro/Ogro.obj', glm.vec3(-400, 300, -300), glm.vec3(180, 175, 0), glm.vec3(100, 100, 100), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
fondo.current_texture = pygame.image.load('./Ogro/SkinColorMostro_COLOR.bmp')
fondo.draw(True)


# gatoReal
#trans, rot, scale, whereami, lookat
fondo.load('./Cat/cat.obj', glm.vec3(300, 50, 850), glm.vec3(180, 210, 0), glm.vec3(100, 100, 100), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
fondo.current_texture = pygame.image.load('./Cat/ColorCat.bmp')
fondo.draw(True)


# Perro
#trans, rot, scale, whereami, lookat
fondo.load('./Dog/Dog.obj', glm.vec3(-100, 200, -150), glm.vec3(180, 170, 0), glm.vec3(100, 100, 100), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
fondo.current_texture = pygame.image.load('./Dog/Dog.bmp')
fondo.draw(True)


#Deagle
#trans, rot, scale, whereami, lookat
fondo.load('./DesertEagle/deagle.obj', glm.vec3(-300, 200, 100), glm.vec3(180, 170, 0), glm.vec3(100, 100, 100), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
# fondo.current_texture = pygame.image.load('./Dog/Dog.bmp')
fondo.draw(True)


# #Deagle
# #trans, rot, scale, whereami, lookat
# fondo.load('./DesertEagle/deagle.obj', glm.vec3(-100, 200, -3000), glm.vec3(180, 170, 0), glm.vec3(10, 10, 10), glm.vec3(0, 0, -200), glm.vec3(0, 0, 0))
# # fondo.current_texture = pygame.image.load('./Dog/Dog.bmp')
# fondo.draw(True)


pygame.display.flip()

import time
time.sleep(20)
