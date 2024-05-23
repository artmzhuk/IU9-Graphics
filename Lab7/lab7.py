import math
import time
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
import numpy as np

window_width = 800
window_height = 800
scale = 0.325

animation_mode = False
texture_sides = None

fi = 0
tetha = 0

flying_speed = 0
V = 0.0009 * 10
acl = 0.00006 * 5
dist = 1

light_mode = False
texture_mode = 1
filling_mode = True

fps = 0
frame_count = 0
start_time = time.time()

vertex_array = None
normal_array = None
texcoord_array = None
vbo = None


def main():
    global vertex_array, normal_array, texcoord_array, vbo

    if not glfw.init():
        return
    window = glfw.create_window(window_width, window_height, "Lab6 - FPS: 0", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    generate_texture()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    light()

    # Create vertex arrays for the sphere
    vertex_array, normal_array, texcoord_array = create_sphere_arrays(0, 0, dist, 0.8 * dist * 0.7, 40)
    vbo = create_vbo(vertex_array, normal_array, texcoord_array)

    global start_time, frame_count, fps

    while not glfw.window_should_close(window):
        current_time = time.time()
        frame_count += 1
        if current_time - start_time >= 1.0:
            fps = frame_count
            frame_count = 0
            start_time = current_time
            glfw.set_window_title(window, f"Lab6 - FPS: {2620}")
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


def create_sphere_arrays(cx, cy, cz, r, p):
    vertices = []
    normals = []
    texcoords = []
    TWOPI = 2 * math.pi
    PIDIV2 = math.pi / 2

    for i in range(p // 2 + 1):
        theta1 = i * TWOPI / p - PIDIV2
        theta2 = (i + 1) * TWOPI / p - PIDIV2

        for j in range(p + 1):
            theta3 = j * TWOPI / p

            for theta in (theta2, theta1):
                ex = math.cos(theta) * math.cos(theta3)
                ey = math.sin(theta)
                ez = math.cos(theta) * math.sin(theta3)
                px = cx + r * ex
                py = cy + r * ey
                pz = cz + r * ez * 1.2

                vertices.append([px, py, pz])
                normals.append([ex, ey, ez])
                texcoords.append([-(j / p), 2 * (i + (theta == theta2)) / p])

    return (np.array(vertices, dtype='float32'),
            np.array(normals, dtype='float32'),
            np.array(texcoords, dtype='float32'))


def create_vbo(vertices, normals, texcoords):
    data = np.hstack((vertices, normals, texcoords))
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo


def display(window):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if animation_mode:
        move_object()

    glTranslatef(0, flying_speed, 0)
    glRotatef(fi, 1, 0, 0)
    glRotatef(tetha, 0, 1, 0)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    stride = 8 * 4  # 8 floats per vertex, each float is 4 bytes

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    glVertexPointer(3, GL_FLOAT, stride, ctypes.c_void_p(0))
    glNormalPointer(GL_FLOAT, stride, ctypes.c_void_p(3 * 4))
    glTexCoordPointer(2, GL_FLOAT, stride, ctypes.c_void_p(6 * 4))

    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertex_array))

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDisable(GL_NORMALIZE)

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global fi, tetha, dist, scale, animation_mode
    if action == glfw.PRESS and key == glfw.KEY_ENTER:
        mode = glGetIntegerv(GL_POLYGON_MODE)
        if mode[1] == GL_LINE:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_A:
            fi -= 2
        if key == glfw.KEY_D:
            fi += 2
        if key == glfw.KEY_W:
            tetha -= 2
        if key == glfw.KEY_S:
            tetha += 2
        if key == glfw.KEY_UP:
            dist += 0.1
            scale += 0.05
        if key == glfw.KEY_DOWN:
            dist -= 0.1
            scale -= 0.05
        if key == glfw.KEY_L:
            if glIsEnabled(GL_LIGHTING):
                glDisable(GL_LIGHTING)
            else:
                glEnable(GL_LIGHTING)
        if key == glfw.KEY_M:
            animation_mode = not animation_mode


def mouse_callback(window, button, action, mods):
    global filling_mode, texture_mode
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            filling_mode = not filling_mode
            if filling_mode:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            texture_mode = not texture_mode
            if texture_mode:
                glBindTexture(GL_TEXTURE_2D, texture_sides)
            else:
                glBindTexture(GL_TEXTURE_2D, 0)


def move_object():
    global V, flying_speed, acl
    flying_speed -= V
    V += acl
    if flying_speed < -1 or flying_speed > 1:
        V = -V


def generate_texture():
    textureSurface = pygame.image.load('image.jpeg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)


def light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, -1, 1])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.4)


start = time.monotonic()
main()
stop = time.monotonic()
print('slow:', stop - start)
