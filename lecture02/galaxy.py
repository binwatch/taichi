import taichi as ti
from celestial_objects import SuperStar, Star, Planet
from widgets import Scrollbar

if __name__ == "__main__":

    ti.init(arch=ti.cuda)

    # control
    paused = False
    export_images = False

    # parameters of stars
    initial_scale = 0.1
    stars_max_mass = 5000
    stars_initial_mass = initial_scale * stars_max_mass

    # superstars
    superstars = SuperStar(N=1, mass=10000)
    superstars.initialize(0.5, 0.5, 0.1, 0)

    # stars and planets
    stars = Star(N=3, mass=stars_initial_mass)
    stars.initialize(0.5, 0.5, 0.2, 10)
    planets = Planet(N=1000, mass=1)
    planets.initialize(0.5, 0.5, 0.4, 10)
    
    # scrollbar to control the mass of stars
    scrollbars = Scrollbar(initial_scale)

    # GUI
    my_gui = ti.GUI("Galaxy", (800, 800))
    h = 5e-5    # time-step size
    i = 0
    while my_gui.running:
        for e in my_gui.get_events(ti.GUI.PRESS):
            if e.key == ti.GUI.ESCAPE:
                exit()
            elif e.key == ti.GUI.SPACE:
                paused = not paused
            elif e.key == 'r':
                stars.initialize(0.5, 0.5, 0.2, 10)
                planets.initialize(0.5, 0.5, 0.4, 10)
                i = 0
            elif e.key == 'i':
                export_images = not export_images
            elif e.key == ti.GUI.LMB:
                cursor_pos = my_gui.get_cursor_pos()
                new_scale = scrollbars.update(cursor_pos)
                if new_scale >= 0:
                    new_mass = new_scale * stars_max_mass
                    stars.setMass(new_mass)
        if not paused:
            superstars.computeForce()
            stars.computeForce(superstars)
            planets.computeForce(stars, superstars)
            for celestial_obj in (stars, planets, superstars):
                celestial_obj.update(h)
            i += 1

        superstars.display(my_gui, radius=20, color=0xFF4500)
        stars.display(my_gui, radius=10, color=0xFFD500)
        planets.display(my_gui)
        scrollbars.display(my_gui)

        if export_images:
            my_gui.show(f"frames/galaxy_{i:05}.png")
        else:
            my_gui.show()