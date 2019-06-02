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

    def load(self, filename):
        model = obj.Obj(filename)

        vertices = []
        t_vertices = []
        n_vertices = []

        for face in model.vfaces:
            vcount = len(face)
            if vcount == 3:
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

                t_vertices.append(glm.vec2(*model.tvertices[f1t]))
                t_vertices.append(glm.vec2(*model.tvertices[f2t]))
                t_vertices.append(glm.vec2(*model.tvertices[f3t]))

                n_vertices.append((glm.vec3(*model.normals[f1n])))
                n_vertices.append((glm.vec3(*model.normals[f2n])))
                n_vertices.append((glm.vec3(*model.normals[f3n])))

        self.vertices = iter(self.transform(vertices))
        self.t_vertices = iter(t_vertices)
        self.normals = iter(n_vertices)


    def transform(self, vertices):
        newvertex = []

        # i = glm.mat4(1)
        # translate = glm.translate(i, glm.vec3(0, 0, 100))
        # rotate = glm.rotate(i, glm.radians(360), glm.vec3(0, 1, 0))
        # scale = glm.scale(i, glm.vec3(100, 100, 100))
        # model = translate * rotate * scale
        #
        # view = glm.lookAt(glm.vec3(0, 0, 200), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        #
        # projection = glm.mat4(
        #     1, 0, 0, 0,
        #     0, 1, 0, 0,
        #     0, 0, 1, -0.001,
        #     0, 0, 0, 1
        # )
        #
        #
        # viewport = glm.mat4(
        #     1, 0, 0, 0,
        #     0, 1, 0, 0,
        #     0, 0, 1, 0,
        #     self.surface.get_width()/2, self.surface.get_height()/2, 128, 1
        # )
        #
        #
        # matrix = viewport * projection * view * model

        for vertex in vertices:
            vertex = glm.vec4(*vertex, 1)
            # vertex = vertex * 100 + 400
#            transformed_vertex = matrix * vertex
            transformed_vertex = (vertex * 100) + 400
            print(transformed_vertex)

            # newvertex.append(
            #     glm.vec3(
            #         transformed_vertex.x / transformed_vertex.w,
            #         transformed_vertex.y / transformed_vertex.w,
            #         transformed_vertex.z / transformed_vertex.w
            #     )
            # )
            newvertex.append(
                glm.vec3(
                    transformed_vertex.x,
                    transformed_vertex.y,
                    transformed_vertex.z
                )
            )
        return newvertex

    def draw(self):
        try:
            while True:
                self.triangle()
        except StopIteration:
            print('Done.')

    def triangle(self):
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

                        c  = (random.randint(0, 255),random.randint(0, 255), random.randint(0, 255) )
                        # c = self.shader(
                        #     (A, B, C),
                        #     (x, y),
                        #     (w, v, u),
                        #     c,
                        #     (0, 0, 1),
                        #     (na, nb, nc)
                        # )

                        self.point(x, y, c)
                except:
                    pass

    def shader(self, trian, p, bari, c, light, normals):

        nA, nB, nC = normals
        w, v, u =  bari

        nx = nA.x * w + nB.x * v + nC.x * u
        ny = nA.y * w + nB.y * v + nC.y * u
        nz = nA.z * w + nB.z * v + nC.z * u

        normal = (nx, ny, nz)

        intensity = glm.dot(normal, light)

        r = min(max(c[0] * intensity, 0), 255)
        g = min(max(c[1] * intensity, 0), 255)
        b = min(max(c[2] * intensity, 0), 255)
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
s = pygame.display.set_mode((1000, 1000), pygame.DOUBLEBUF|pygame.HWACCEL) #, pygame.FULLSCREEN)

r = Render(s)
r.load('./Cubo.obj')
r.current_texture = pygame.image.load('./cueva.bmp')

r.draw()

pygame.display.flip()

import time
time.sleep(15)
