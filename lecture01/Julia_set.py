# ------ initialize Taichi ------
import taichi as ti

ti.init(ti.gpu)

# ------ Data ------
n = 320
pixels = ti.Vector.field(3, ti.f32, (n * 2, n))
# pixels = ti.field(dtype=float, shape=(n * 2, n))

# ------ Computation ------
@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

@ti.kernel
def paint(t: float):
    for i, j in pixels: # Parallized over all pixels
        c = ti.Vector([-0.8, ti.cos(t) * 0.2])
        z = ti.Vector([i / n - 1, j / n - 0.5]) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(complex_sqr(z)) + c
            iterations += 1
        pixels[i, j][0] = 0.3 
        pixels[i, j][1] = iterations * 0.02
        pixels[i, j][2] = 1 - iterations * 0.02

# ------ Visualization ------
gui = ti.GUI("Julia Set", res=(n * 2, n))

for i in range(1000000):
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()