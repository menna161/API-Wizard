import numpy as np
import tensorflow as tf
import six


def __init__(self, size=20, map_config={}):
    'Maps contain data structures storing game states.  The primary data\n    structures used here are the map_dict and the object_list.  map_dict\n    contains dictionaries indexed by index-within-the-world.  So,\n    map_dict[(i,j)] returns a dictionary of lists of Objects on the cell at\n    (i,j).  Object lists are indexed within map_dict by their class name, which\n    is always defined as a human-readable string, and referenced by\n    Object.c_name.\n    object_list is a global dictionary of lists of objects in the game.  This\n    makes it easy to loop over all Agent object without having to look at every\n    location on the map.  Care must be taken to update both of these data\n    structures whenever transformations are applied.'
    self.size = size
    self.map_dict = {}
    self.object_list = {}
    self.fields = {}
    self.fields['Temperature'] = Temperature(self, 'Temperature', np.array(np.ones((self.size, self.size))))
    for i in range(size):
        for j in range(size):
            self.map_dict[(i, j)] = {}
    already_placed = []
    for (_, obj_data) in six.iteritems(map_config):
        (obj_fn, num_objects) = obj_data
        for this_obj in range(num_objects):
            unique = False
            while (not unique):
                rand_x = (np.random.randint((size - 2)) + 1)
                rand_y = (np.random.randint((size - 2)) + 1)
                if ((rand_x, rand_y) not in already_placed):
                    unique = True
                    already_placed.append((rand_x, rand_y))
            obj_name = obj_fn.c_name
            new_obj = obj_fn(my_map=self, loc=(rand_x, rand_y), name=(obj_name + str(this_obj)))
            if (obj_name not in self.map_dict[(rand_x, rand_y)]):
                self.map_dict[(rand_x, rand_y)][obj_name] = []
            if (obj_name not in self.object_list):
                self.object_list[obj_name] = []
            self.map_dict[(rand_x, rand_y)][obj_name].append(new_obj)
            self.object_list[obj_name].append(new_obj)
    wall_str = Wall.c_name
    for i in range(size):
        for j in range(size):
            if ((i == 0) or (i == (size - 1)) or (j == 0) or (j == (size - 1))):
                if (wall_str not in self.map_dict[(i, j)]):
                    self.map_dict[(i, j)][wall_str] = []
                if (wall_str not in self.object_list):
                    self.object_list[wall_str] = []
                this_wall = Wall(my_map=self, loc=(i, j), name=((wall_str + str(i)) + str(j)), char='#')
                self.map_dict[(i, j)][wall_str].append(this_wall)
                self.object_list[wall_str].append(this_wall)
    pass
