import numpy as np
import moderngl_window as mglw

class Window(mglw.WindowConfig):
    title = "Concorde Simulation"
    gl_version = (3, 3)
    window_size = (1920, 1080)
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_position;
                void main() {
                    gl_Position = vec4(in_position, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                out vec4 color;
                void main() {
                    color = vec4(1.0, 0.5, 0.0, 1.0);
                }
            """,
        )

        vertices = np.array([
            -0.5, -0.5,
             0.5, -0.5,
             0.0,  0.5,
        ], dtype="f4")

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(
            self.prog, [(self.vbo, "2f", "in_position")]
        )

    def on_render(self, time: float, frametime: float):
        self.ctx.clear(0.1, 0.2, 0.3)
        self.vao.render()

class Render():
    def run(self):
        mglw.run_window_config(Window)