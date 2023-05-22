import numpy as np
import tensorflow as tf
import six


def propose_action(self, user_action=None):
    if (user_action != None):
        (loc_x, loc_y) = self.loc
        act = ControllableWalker.move_map[user_action]
        new_dir = ((act[0] + loc_x), (act[1] + loc_y))
        this_action = Move(my_agent=self, my_map=self.parent_map, new_loc=new_dir)
        return this_action
    else:
        if (self.inventory != []):
            this_action = Eat(self, self.parent_map)
            return this_action
        picked = False
        if ('Apple' in self.parent_map.map_dict[self.loc]):
            if (self.parent_map.map_dict[self.loc]['Apple'] != []):
                apple_to_pick = self.parent_map.map_dict[self.loc]['Apple'][0]
                this_action = PickDrop(self, self.parent_map, apple_to_pick)
                picked = True
                return this_action
        if (picked == False):
            (loc_x, loc_y) = self.loc
            r = np.random.randint(4)
            new_dir = ((ControllableWalker.rand_dir[r][0] + loc_x), (ControllableWalker.rand_dir[r][1] + loc_y))
            this_action = Move(my_agent=self, my_map=self.parent_map, new_loc=new_dir)
            return this_action
