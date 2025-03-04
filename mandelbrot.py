import moderngl
import numpy as np

class MandelbrotRenderer:
    def __init__(self, ctx, width, height):
        self.ctx = ctx
        self.width = width
        self.height = height

        # Crear buffer de vértices para la pantalla completa
        self.quad_buffer = self.ctx.buffer(np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0, -1.0, 1.0, 0.0,
             1.0,  1.0, 1.0, 1.0
        ], dtype='f4'))

        # Shader de fragmento para Mandelbrot con múltiples colores según iteración
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            in vec2 in_texcoord;
            out vec2 uv;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                uv = in_texcoord;
            }
            """,
            fragment_shader="""
            #version 330
            uniform float zoom;
            uniform vec2 center;
            uniform int max_iter;
            uniform vec3 color1;
            uniform vec3 color2;
            uniform vec3 color3;
            uniform vec3 color4;
            uniform vec3 color5;
            in vec2 uv;
            out vec4 fragColor;

            void main() {
                vec2 c = (uv - vec2(0.5)) * zoom + center;
                vec2 z = vec2(0.0, 0.0);
                int iter;
                for (iter = 0; iter < max_iter; iter++) {
                    if (length(z) > 2.0) break;
                    z = vec2(z.x * z.x - z.y * z.y + c.x, 2.0 * z.x * z.y + c.y);
                }
                float color_factor = float(iter) / float(max_iter);

                // Colores diferentes dependiendo de la iteración
                if (iter < max_iter / 5) {
                    fragColor = vec4(color1 * color_factor, 1.0);
                } else if (iter < 2 * max_iter / 5) {
                    fragColor = vec4(color2 * color_factor, 1.0);
                } else if (iter < 3 * max_iter / 5) {
                    fragColor = vec4(color3 * color_factor, 1.0);
                } else if (iter < 4 * max_iter / 5) {
                    fragColor = vec4(color4 * color_factor, 1.0);
                } else {
                    fragColor = vec4(color5 * color_factor, 1.0);
                }
            }
            """
        )

        self.vao = self.ctx.vertex_array(
            self.prog, [(self.quad_buffer, "2f 2f", "in_vert", "in_texcoord")]
        )

    def render(self, zoom, center, max_iter, color1, color2, color3, color4, color5):
        self.prog["zoom"].value = zoom
        self.prog["center"].value = center
        self.prog["max_iter"].value = max_iter
        self.prog["color1"].value = color1
        self.prog["color2"].value = color2
        self.prog["color3"].value = color3
        self.prog["color4"].value = color4
        self.prog["color5"].value = color5
        self.vao.render(moderngl.TRIANGLES)
