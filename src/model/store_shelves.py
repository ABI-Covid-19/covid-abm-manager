from .agent import Agent

import numpy as np


class StoreShelfInstance(type):

    def __instancecheck__(self, other):
        if other == StoreShelf:
            return True
        else:
            return False


class StoreShelf(Agent, metaclass=StoreShelfInstance):

    def __init__(self, unique_id, model, pos):
        super(StoreShelf, self).__init__(unique_id, model)
        self.model = model
        self.model_space = self.model.space
        self.pos = np.array(pos)

    def get_shelves(self):
        shelf_agents = np.zeros((self.model.width, self.model.height))
        for cell in self.model_space.coord_iter():
            cell_content, x, y = cell
            if len(cell_content) > 0:
                content = cell_content.pop()
                if isinstance(content, self):
                    shelf_agents[x][y] = 100
        return shelf_agents
