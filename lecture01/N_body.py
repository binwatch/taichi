# ------ initialize Taichi ------
import taichi as ti

ti.init(ti.gpu)

# ------ Data ------
# global control
paused = ti.field(ti.i32, ())

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1
# G = 6.67408e-11
PI = 3.141592653

# number of planets
N = 1000
# unit mass
m = 5
# galaxy size
galaxy_size = 0.4
# planet radius (for rendering)
planet_radius = 2
# init vel
init_vel = 120

# time-step size
h = 1e-5
# substepping
substepping = 10

# pos, vel and force of the planets
# Nx2 vectors
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
force = ti.Vector.field(2, ti.f32, N)
pos_backup = ti.Vector.field(2, ti.f32, N)

# black hole
blackhole_pos = ti.Vector.field(2, ti.f32, ())
# M >= c^2|r|/G for a black hole, try larger mass
M = 3e6 

# ------ Computation ------
@ti.kernel
def initialize():
    center = ti.Vector([0.5, 0.5])
    blackhole_pos[None] = ti.Vector([-1.0, -1.0])
    for i in range(N):
        theta = ti.random() * 2 * PI
        r = (ti.sqrt(ti.random()) * 0.7 + 0.3) * galaxy_size
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center + offset
        vel[i] = [-offset.y, offset.x]
        vel[i] *= init_vel

#@ti.kernel
@ti.func
def compute_force():
    # clear force
    for i in range(N):
        force[i] = ti.Vector([0.0, 0.0])

    # compute gravitational force
    for i in range(N):
        p = pos[i]
        for j in range(N):
            if i != j:
                diff = p - pos[j]
                r = diff.norm(1e-5)

                # gravitational force -(GMm/r^2) * diff/r
                f = -G * m * m * (1.0/r)**3 * diff

                # assign to each particle
                force[i] += f
        # if balck hole exists
        if blackhole_pos[None][0] > 0.0:
            diff = p - blackhole_pos[None]
            r = diff.norm(1e-5)

            # gravitational force -(GMm/r^2) * diff/r
            f = -G * M * m * (1.0/r)**3 * diff

            # assign to each particle
            force[i] += f

@ti.kernel
def update():
    dt = h/substepping
    dt_half = dt/2
    #for i in range(N):
        # symplectic euler
        # vel[i] += dt*force[i]/m
        # pos[i] += dt*vel[i]
    # midpoint method
    for i in range(N):
        pos_backup[i] = pos[i]
    compute_force()
    for i in range(N):
        vel[i] += dt_half*force[i]/m
        pos[i] += dt_half*vel[i]
    compute_force()
    for i in range(N):
        vel[i] += dt_half*force[i]/m
        pos_backup[i] += dt*vel[i]
        pos[i] = pos_backup[i]
    blackhole_pos[None] = ti.Vector([-1.0, -1.0])
  
# ------ Visualization ------
gui = ti.GUI('N-body problem', (512, 512))

initialize()
while gui.running:

    for i in range(substepping):
        if gui.get_event(ti.GUI.PRESS, ti.GUI.LMB):
            blackhole_pos[None] = gui.get_cursor_pos()
        update()

    gui.clear(0x112F41)
    gui.circles(pos.to_numpy(), color=0xffffff, radius=planet_radius)
    gui.show()
