from OpenGL.GL import *
import glfw
import glm
import random
from helpers.models import *
from helpers.models.cuboid import Cuboid
from helpers.shaders import DemoShaders

y_speed = 0.0
x_speed = 0.0
pos_x = 0.0
pos_y = 0.0
pos_z = 0.0
bubble_positions = []
bubble_lifetime = 4.0
bubble_speed = 1.2
bubble_growth_duration = 0.6
animation_speed = 1.0

def key_callback(window, key, scancode, action, mods):
    global y_speed, x_speed, pos_x, pos_y, pos_z, animation_speed
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            y_speed = -3.14
        elif key == glfw.KEY_RIGHT:
            y_speed = 3.14
        elif key == glfw.KEY_UP:
            x_speed = -3.14
        elif key == glfw.KEY_DOWN:
            x_speed = 3.14
        elif key == glfw.KEY_W:
            pos_z -= 0.1
        elif key == glfw.KEY_S:
            pos_z += 0.1
        elif key == glfw.KEY_A:
            pos_x -= 0.1
        elif key == glfw.KEY_D:
            pos_x += 0.1
        elif key == glfw.KEY_Z:
            pos_y += 0.1
        elif key == glfw.KEY_X:
            pos_y -= 0.1
        elif key in range(glfw.KEY_1, glfw.KEY_9 + 1):
            animation_speed = key - glfw.KEY_0

    if action == glfw.RELEASE:
        if key in [glfw.KEY_LEFT, glfw.KEY_RIGHT]:
            y_speed = 0
        if key in [glfw.KEY_UP, glfw.KEY_DOWN]:
            x_speed = 0

def init_opengl_program(window):
    glClearColor(0, 0, 0, 1)
    DemoShaders.initShaders("helpers/shaders/")
    glfw.set_key_callback(window, key_callback)

def draw_scene(window, angle_x, angle_y, time_elapsed):
    global bubble_positions
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    V = glm.lookAt(glm.vec3(pos_x, pos_y + 5, pos_z + 10),
                   glm.vec3(pos_x, pos_y, pos_z),
                   glm.vec3(0.0, 1.0, 0.0))
    ratio = glfw.get_framebuffer_size(window)[0] / glfw.get_framebuffer_size(window)[1]

    P = glm.perspective(glm.radians(50.0), ratio, 0.1, 100.0)

    DemoShaders.spConstant.use()
    glUniformMatrix4fv(DemoShaders.spConstant.u("P"), 1, GL_FALSE, glm.value_ptr(P))
    glUniformMatrix4fv(DemoShaders.spConstant.u("V"), 1, GL_FALSE, glm.value_ptr(V))

    M = glm.rotate(angle_y, glm.vec3(0, 1, 0)) * glm.rotate(angle_x, glm.vec3(1, 0, 0))

    table_top = Cuboid(width=5, height=1, depth=3)
    M_top = glm.translate(M, glm.vec3(0, 0.5, 0))
    glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, glm.value_ptr(M_top))
    table_top.drawWire()

    teapot = Teapot()
    M_teapot = glm.translate(M, glm.vec3(0, 1.4, 0))
    glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, glm.value_ptr(M_teapot))
    teapot.drawWire()

    for x, y, z in [(-2.25, -2, -1.25),
                    (2.25, -2, -1.25),
                    (2.25, -2, 1.25),
                    (-2.25, -2, 1.25)]:
        leg = Cuboid(width=0.5, height=4, depth=0.5)
        M_leg = glm.translate(M, glm.vec3(x, y, z))
        glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, glm.value_ptr(M_leg))
        leg.drawWire()

    if random.random() < 0.1:
        bubble_positions.append([0.9, 1.9, 0, 0, 1])

    new_bubble_positions = []
    for bubble in bubble_positions:
        if bubble[3] < bubble_growth_duration:
            bubble[4] = (bubble[3] / bubble_growth_duration)
        else:
            bubble[1] += bubble_speed * time_elapsed

        bubble[3] += time_elapsed
        if bubble[3] < bubble_lifetime:
            new_bubble_positions.append(bubble)
            bubble_model = Sphere(0.08 * bubble[4])
            M_bubble = glm.translate(M, glm.vec3(bubble[0], bubble[1], bubble[2]))
            glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, glm.value_ptr(M_bubble))
            bubble_model.drawWire()
    bubble_positions = new_bubble_positions

    glfw.swap_buffers(window)

def free_opengl_program(window):
    pass

def main():
    glfw.init()
    window = glfw.create_window(1200, 1000, "Zadanie 1", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    init_opengl_program(window)
    time = glfw.get_time()
    angle_x = 0.0
    angle_y = 0.0

    while not glfw.window_should_close(window):
        new_time = glfw.get_time()
        time_elapsed = (new_time - time) * animation_speed
        time = new_time
        angle_x += x_speed * time_elapsed
        angle_y += y_speed * time_elapsed
        draw_scene(window, angle_x, angle_y, time_elapsed)
        glfw.poll_events()

    free_opengl_program(window)
    glfw.terminate()

if __name__ == "__main__":
    main()