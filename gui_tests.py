# -*- coding: utf-8 -*-
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy

def main():
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    steps = numpy.linspace(0.0, 1.0, 8)
    a = 1.0
    background_color = [1., 1., 1., 1]

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

        imgui.begin("Example: tooltip")
        if(imgui.button("Click me!")):
            a = a / 1.2
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.text("This button is clickable.")
            imgui.text("This button has full window tooltip.")
            texture_id = imgui.get_io().fonts.texture_id
            imgui.image(texture_id, 512, 64, border_color=(1, 0, 0, 1))
            imgui.end_tooltip()
        if(imgui.button("reset")):
            a = 1
        imgui.text("text")
        imgui.begin_child("text")
        for r in steps:
            for  g in steps:
                for b in steps:
                    # for a in steps:
                    imgui.text_colored(f"color {r:.{2}f} {g:.{2}f} {b:.{2}f} {a:.{2}f}", r, g, b, a)
                    if imgui.is_item_hovered():
                        imgui.begin_tooltip()
                        imgui.color_button(r, g, b, a)
                        imgui.same_line()
                        imgui.text("This button is colored.")
                        imgui.end_tooltip()
                    
                    # context menu label must differ or everything is dumpred into the same context menu
                    # this way information cn be accumulated into a context menu or popup window though
                    if imgui.begin_popup_context_item(f"Item Context Menu {r:.{2}f} {g:.{2}f} {b:.{2}f} {a:.{2}f}", mouse_button=0):
                        if(imgui.color_button(r, g, b, a)):
                            background_color = [r, g, b, a]
                        imgui.same_line()
                        imgui.text("<- Click.")
                        # imgui.selectable("Set to Zero")
                        imgui.end_popup()

                    imgui.same_line()
                    imgui.text_colored(f"{r:.{2}f}", 1, 0, 0, 1)
                    imgui.same_line()
                    imgui.text_colored(f"{g:.{2}f}", 0, 1, 0, 1)
                    imgui.same_line()
                    imgui.text_colored(f"{b:.{2}f}", 0, 0, 1, 1)
                    
        imgui.end_child()
        imgui.end()

        imgui.begin("Example: Log")
        if(imgui.button("Click me!")):
            log.append(f"line {len(log)}")
        cbx_clicked, log_cbx_state = imgui.checkbox("Toggle Me!", log_cbx_state)
        imgui.text("Checkbox 2 return value: {}".format(log_cbx_state))
        if(log_cbx_state):
            log.append(f"line {len(log)}")

        imgui.begin_child("log")
        for i, line in enumerate(log):
            imgui.text(line)
        imgui.end_child()
        imgui.end()

        imgui.begin("Example: checkboxes for flags", flags=flags)

        clicked, flags = imgui.checkbox_flags(
            "No resize", flags, imgui.WINDOW_NO_RESIZE
        )
        clicked, flags = imgui.checkbox_flags(
            "No move", flags, imgui.WINDOW_NO_MOVE
        )
        clicked, flags = imgui.checkbox_flags(
            "No collapse", flags, imgui.WINDOW_NO_COLLAPSE
        )
        # note: it also allows to use multiple flags at once
        clicked, flags = imgui.checkbox_flags(
            "No resize & no move", flags,
            imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE
        )
        imgui.text("Current flags value: {0:b}".format(flags))
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
