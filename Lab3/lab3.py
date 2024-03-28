#!/usr/bin/env python3

import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt, asin, pi

xR, yR = 0.1, 0.1
delta = 0.2
h = 0.8
alpha, beta = 0, 0
fill = True


def main():
    if not glfw.init():
        return
    window = glfw.create_window(1280, 720, "LAB_3", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def display(window):
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)

    glRotate(alpha, 0, 0, 1)
    glRotate(beta, 0, 1, 0)

    global h, xR, yR

    def tilted_prism():
        sides = 3
        segment_angle = 2.0 * pi / sides

        glBegin(GL_QUADS)
        for i in range(sides):
            x1 = xR * cos(i * segment_angle)
            y1 = yR * sin(i * segment_angle)
            x2 = xR * cos((i + 1) * segment_angle)
            y2 = yR * sin((i + 1) * segment_angle)

            glColor3f(0.0, 1.0, 0.0)
            glVertex3f(x1, y1, 0.0)
            glVertex3f(x2, y2, 0.0)

            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(x2+delta, y2+delta, h)
            glVertex3f(x1+delta, y1+delta, h)

            glVertex3f(x1, y1, 0.0)
            glVertex3f(x2, y2, 0.0)
            glVertex3f(x2+delta, y2+delta, h)
            glVertex3f(x1+delta, y1+delta, h)

            glVertex3f(delta, delta, h)
            glVertex3f(delta, delta, h)
            glVertex3f(x1+delta, y1+delta, h)
            glVertex3f(x2+delta , y2+delta, h)

        glEnd()
    tilted_prism()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global xR, yR, h, alpha, beta, delta
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            xR += 0.1
        elif key == glfw.KEY_S:
            xR -= 0.1
        elif key == glfw.KEY_A:
            yR += 0.1
        elif key == glfw.KEY_D:
            yR -= 0.1
        elif key == glfw.KEY_Z:
            h += 0.1
        elif key == glfw.KEY_X:
            h -= 0.1
        elif key == glfw.KEY_UP:
            alpha -= 5
        elif key == glfw.KEY_DOWN:
            alpha += 5
        elif key == glfw.KEY_LEFT:
            beta -= 5
        elif key == glfw.KEY_RIGHT:
            beta += 5
        elif key == glfw.KEY_C:
            delta += 0.1
        elif key == glfw.KEY_V:
            delta -= 0.1
        elif key == glfw.KEY_Q:
            global fill
            fill = not fill
            if fill:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


if __name__ == "__main__":
    main()
