import pygame, branch, math, copy, random


def setup(self):
    ' Setting up the display and storing our initial root branch '
    self.display.fill(bg_colour)
    pygame.display.set_caption('Fractal Tree Generator')
    for i in range(forest_size):
        branch_size = random.randint(min_branch_size, max_branch_size)
        x = random.randint(0, self.dimensions[0])
        a = branch.Vector(x, self.dimensions[1])
        b = branch.Vector(x, (self.dimensions[1] - branch_size))
        root = branch.Branch(a, b)
        self.tree.append(root)
        self.forest.append(self.tree)
    self.run()
