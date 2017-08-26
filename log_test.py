# -*- coding: utf-8 -*-
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

import random
import string
import numpy

def main():
    imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 0)
    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
    imgui.push_style_var(imgui.STYLE_CHILD_WINDOW_ROUNDING, 0)
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    steps = numpy.linspace(0.0, 1.0, 8)
    background_color = [.3, .3, .3, 1]
    color_select = (0.5, 0.5, 0.5)
    text_count = 3

    # imgui_io: imgui.core._IO = imgui.get_io()
    # font_extra = imgui_io.fonts.add_font_from_file_ttf(
    #     "Roboto-Regular.ttf", 30, imgui_io.fonts.get_glyph_ranges_japanese()
    # )
    # imgui_io.fonts._require_pointer()

    log = []
    log_cbx_state = False
    flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_test_window()

        imgui.begin("Example: Log")
        clicked, color_select = imgui.color_edit3("color", *color_select)

        if(imgui.button("random color")):
            r = random.uniform(0.3, 1.0)
            g = random.uniform(0.3, 1.0)
            b = random.uniform(0.3, 1.0)
            color_select = (r, g, b)
        if(imgui.button("random text")):
            text_item = []
            for i in range(text_count):
                r = random.uniform(0.3, 1.0)
                g = random.uniform(0.3, 1.0)
                b = random.uniform(0.3, 1.0)
                color_select = (r, g, b)
                text = "".join( [random.choice(string.ascii_letters[:26]) for i in range(5)] )
                text_item.append({"color": (r, g, b), "content": f"text {i} {text}"})
            log.append(text_item)
        if(imgui.button("Click me!")):
            log.append(f"line {len(log)}")
        if(imgui.button("Click me! 2")):
            log.append({"color": color_select, "content": f"line {len(log)}"})
        cbx_clicked, log_cbx_state = imgui.checkbox("Toggle Me!", log_cbx_state)
        imgui.text("Checkbox 2 return value: {}".format(log_cbx_state))
        if(log_cbx_state):
            log.append(f"line {len(log)}")

        imgui.begin_child("log")
        for i, line in enumerate(log):
            if isinstance(line, dict):
                line: dict = line
                # with imgui.font(font_extra):
                if "color" in line and "content" in line:
                    imgui.text_colored(line["content"], *line["color"])
            elif isinstance(line, str):
                imgui.text(line)
            elif isinstance(line, list):
                for item in line:
                    if isinstance(item, dict):
                        item: dict = item
                        # with imgui.font(font_extra):
                        if "color" in item and "content" in item:
                            color = item["color"]
                            imgui.text_colored(item["content"], *color)
                            if(imgui.is_item_hovered()):
                                imgui.begin_tooltip()
                                imgui.color_button(*color)
                                imgui.same_line()
                                imgui.text("This button is colored.")
                                imgui.end_tooltip()
                    elif isinstance(item, str):
                        imgui.text(item)
                    imgui.same_line()
                imgui.new_line()
            else:
                print(type(line))
        imgui.end_child()
        imgui.end()

        # gl.glClearColor(.5, .5, .5, 1)
        gl.glClearColor(*background_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        glfw.swap_buffers(window)

    impl.shutdown()
    imgui.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "ExMachina Tests"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window

if __name__ == "__main__":
    main()
