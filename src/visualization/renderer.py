from pathlib import Path
import numpy as np
import moderngl_window as mglw
from moderngl_window.scene.camera import OrbitCamera

class Window(mglw.WindowConfig):
    title = "Concorde Simulation"
    gl_version = (3, 3)
    window_size = (1920, 1080)
    resizable = True

    # Assets folder config.
    resource_dir = (Path(__file__).parent.parent.parent / "assets").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cielo.
        self.sky_prog = self.ctx.program(

        vertex_shader="""
            #version 330
            in vec2 in_position;
            out vec2 uv;
            void main() 
            {
                uv = in_position * 0.5 + 0.5; // All the screen space.
                gl_Position = vec4(in_position, 0.0, 1.0);
            }
        """,

        fragment_shader="""
            #version 330
            uniform float time;
            uniform float aspect;
            in vec2 uv;
            out vec4 color;

            float hash(vec2 p) 
            {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }

            // Noise.
            float noise(vec2 p) 
            {
                vec2 i = floor(p);
                vec2 f = fract(p);

                f = f * f * (3.0 - 2.0 * f);   
                
                float a = hash(i);
                float b = hash(i + vec2(1.0, 0.0));
                float c = hash(i + vec2(0.0, 1.0));
                float d = hash(i + vec2(1.0, 1.0));
                
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }

            
            float fbm(vec2 p) 
            {                      
                float v = 0.0;
                float amp = 0.5;

                for (int i = 0; i < 5; i++) 
                {
                    v += amp * noise(p);
                    p *= 2.0;
                    amp *= 0.5;
                }

                return v;
            }

            // Main.
            void main() {
                vec3 horizon = vec3(0.75, 0.88, 1.0);
                vec3 zenith  = vec3(0.15, 0.40, 0.80);
                vec3 sky = mix(horizon, zenith, uv.y);

                vec2 p = vec2(uv.x * aspect, uv.y) * 3.0 + vec2(time * 0.05, 0.0);
                float clouds = smoothstep(0.5, 0.8, fbm(p));

                color = vec4(mix(sky, vec3(1.0), clouds), 1.0);
            }
        """,
    )

        quad = np.array([-1, -1,  1, -1,  -1, 1,  1, 1], dtype="f4")
        self.sky_vbo = self.ctx.buffer(quad)
        self.sky_vao = self.ctx.vertex_array(
            self.sky_prog, [(self.sky_vbo, "2f", "in_position")]
        )

        # Concorde loader and camera configuration.
        self.scene = self.load_scene("concorde/scene.gltf")

        # Create an orbital camera.
        self.camera = OrbitCamera(aspect_ratio=self.wnd.aspect_ratio)

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.0, 0.0, 0.0)

        # 1. Sky (with depth)
        self.ctx.disable(self.ctx.DEPTH_TEST)
        self.sky_prog["time"].value = time
        self.sky_prog["aspect"].value = self.wnd.aspect_ratio
        self.sky_vao.render(mode=self.ctx.TRIANGLE_STRIP)

        # 2. Plane (no depth)
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )

    def on_resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def on_mouse_drag_event(self, x, y, dx, dy):
        self.camera.rot_state(dx, dy)

    def on_mouse_scroll_event(self, x_offset, y_offset):
        self.camera.zoom_state(y_offset)

class Render():
    def run(self):
        mglw.run_window_config(Window)