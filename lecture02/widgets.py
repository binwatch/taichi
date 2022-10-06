import taichi as ti

class Scrollbar:
    def __init__(self, initial_scale) -> None:
        self.scale = initial_scale
        self.width = 0.3
        height = 0.03
        self.radius = self.width * 40 
        self.topleft = [0.03, 0.03]
        self.bottomright = [self.topleft[0]+self.width, self.topleft[1]+height]
        self.pos = [self.topleft[0] + self.scale * self.bottomright[0], (self.topleft[1] + self.bottomright[1])/2]

    def display(self, gui):
        gui.rect(self.topleft, self.bottomright, 3, 0x4169E1)
        gui.circle(self.pos, 0x3CB371, self.radius)

    def update(self, cursor_pos):
        if self.insideBar(cursor_pos):
            new_scale = (cursor_pos[0] - self.topleft[0])/self.width
            self.setScale(new_scale)
            self.updatePos()
            return new_scale
        return -1
    
    def insideBar(self, position):
        if position[0] < self.topleft[0] or position[0] > self.bottomright[0]:
            return False
        if position[1] < self.topleft[1] or position[1] > self.bottomright[1]:
            return False
        return True
    
    def getScale(self):
        return self.scale
    
    def setScale(self, value):
        self.scale = value

    def updatePos(self):
        self.pos[0] = self.topleft[0] + self.scale * self.bottomright[0]