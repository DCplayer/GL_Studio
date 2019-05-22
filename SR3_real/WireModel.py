from GL_Studio import *


def load_wireframe(width, height):
    gl_create_window(width, height)
    gl_clear()
    filename('Lampara.bmp')
    gl_view_port(0, 0, width - 1, width - 1)

    gl_load_wf('tea.obj', 1500, 1100, 0, 250, 250, 1, 1, width, height)
    gl_finish()

load_wireframe(3000, 3000)