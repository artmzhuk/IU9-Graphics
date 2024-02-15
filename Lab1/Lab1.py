import glfw
from OpenGL.GL import *

yCoef = 1.0
xCoef = 1.0
size = 1.0


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


def display(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex2f(xCoef * size * -0.7, yCoef * size * -1.0)
    glVertex2f(xCoef * size * -1.0, yCoef * size * 0.3)
    glVertex2f(xCoef * size * 0.0, yCoef * size * 1.0)
    glVertex2f(xCoef * size * 1.0, yCoef * size * 0.3)
    glVertex2f(xCoef * size * 0.7, yCoef * size * -1.0)
    glColor3f(0.78, 0.13, 0.13)

    glEnd()
    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global yCoef
    global xCoef
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            xCoef += 0.1
        if key == 263:  # glfw.KEY_LEFT
            xCoef -= 0.1
        if key == glfw.KEY_UP:
            yCoef += 0.1
        if key == glfw.KEY_DOWN:
            yCoef -= 0.1


def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10


if __name__ == '__main__':
    main()
