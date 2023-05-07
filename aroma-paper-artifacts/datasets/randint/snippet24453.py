import pygame, branch, math, copy, random


def run(self):
    ' Main program loop '
    layer = 0
    while self.running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.running = False
            for tree in self.forest:
                if (layer < top_layer):
                    for i in range(len(tree)):
                        if (not tree[i].finished):
                            tree.append(tree[i].branch_off((math.pi / random.randint(4, ((top_layer - layer) + 8))), branch_reduction))
                            tree.append(tree[i].branch_off(((- math.pi) / random.randint(4, ((top_layer - layer) + 8))), branch_reduction))
                            tree[i].finished = True
                    layer += 1
                if (layer == top_layer):
                    for i in range(len(tree)):
                        if (not tree[i].finished):
                            if show_leaves:
                                self.leaves.append(copy.copy(tree[i].end))
                self.draw()
