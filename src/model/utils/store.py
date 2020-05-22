from abc import ABC

from .abstract_store import AbstractStorePlanner
import numpy as np


class Store(AbstractStorePlanner, ABC):
    """
    Class to handle low level parameters of the store. This class designs a generic supermarket layout of New World.
    """

    def __init__(self, model_description):
        self._model_description = model_description
        self._blocked_cells = list()

    def __update_description(self, description):
        self._model_description[description[0]] = description[1]

    def create_entry(self):
        """
        Designing the floor plan for the entry gate.
        :return:
        """
        ratio = 0.01 * self._model_description["area"]
        entry_list = []
        number_of_columns = number_of_rows = int(np.ceil(np.sqrt(ratio)))
        for col in range(0, number_of_columns):
            for row in range(0, number_of_rows):
                entry_list.append((row, col))
        self.__update_description(["entry_cells", entry_list])
        return entry_list

    def create_produce_dept(self):
        free_space_before_produce = int(np.ceil(0.004 * self._model_description["area"]))

        #  create the first aisle
        aisle_cells = []
        begin_aisle = max(c[1] for c in self._model_description["entry_cells"]) + free_space_before_produce + 1
        end_aisle = self._model_description["height"]
        for cell in range(begin_aisle, end_aisle - 1):
            aisle_cells.append((0, cell))
        self.__update_description(["produce_aisle_cells", aisle_cells])

        size = free_space_before_produce if free_space_before_produce % 2 != 0 else free_space_before_produce + 1
        width, height = int(np.ceil(np.sqrt(size))), int(np.floor(np.sqrt(size)))

        if self._model_description["width"] * self._model_description["height"] >= 2000:  # for super-sized stores
            free_space_between_cells = 3
        else:
            free_space_between_cells = 2

        #  create the first three island
        begin_cell_width = max(c[0] for c in self._model_description["entry_cells"]) + 1
        begin_cell_height = begin_aisle
        island_one_cells = self.__create_produce_islands(begin_cell_width, width, begin_cell_height, height)
        self.__update_description(["produce_island_1_cells", island_one_cells])

        begin_cell_width = max(c[0] for c in self._model_description["entry_cells"]) + 1
        begin_cell_height = max(c[1] for c in island_one_cells) + free_space_between_cells + 1
        island_two_cells = self.__create_produce_islands(begin_cell_width, width, begin_cell_height, height)
        self.__update_description(["produce_island_2_cells", island_two_cells])

        begin_cell_width = max(c[0] for c in self._model_description["entry_cells"]) + 1
        begin_cell_height = max(c[1] for c in island_two_cells) + free_space_between_cells + 1
        island_three_cells = self.__create_produce_islands(begin_cell_width, width, begin_cell_height, height)
        self.__update_description(["produce_island_3_cells", island_three_cells])

        #  create the last island
        begin_cell_width = max(c[0] for c in self._model_description["entry_cells"]) + 1
        begin_cell_height = max(c[1] for c in island_three_cells) + free_space_between_cells + 1
        if begin_cell_height + height + 1 == self._model_description["height"] or \
                begin_cell_height + height + 1 == self._model_description["height"] - 1:
            begin_cell_height = begin_cell_height - 2
        island_four_cells = self.__create_produce_islands(begin_cell_width, width, begin_cell_height, height)
        self.__update_description(["produce_island_4_cells", island_four_cells])

        produce_list = aisle_cells + island_one_cells + island_two_cells + island_three_cells + island_four_cells
        self.__update_description(["produce_cells", produce_list])
        return produce_list

    @staticmethod
    def __create_produce_islands(begin_w, w, begin_h, h):
        island_cells = list()
        for col in range(begin_h, begin_h + h):
            for row in range(begin_w, begin_w + w):
                island_cells.append((row, col))
        return island_cells

    def create_grocery_dept(self):
        if self._model_description["width"] * self._model_description["height"] >= 2000:  # for super-sized stores
            number_of_aisles = int(np.ceil(0.0045 * self._model_description["area"]))
            free_space_between_cells = 3
        else:
            number_of_aisles = int(np.ceil(0.009 * self._model_description["area"]))
            free_space_between_cells = 2

        self.__update_description(["number_of_grocery_aisles", number_of_aisles])

        begin_cell_width = max(c[0] for c in self._model_description["produce_cells"]) + free_space_between_cells + 1
        begin_cell_height = min(c[1] for c in self._model_description["produce_cells"]) - free_space_between_cells
        end_cell_height = int(max(c[1] for c in self._model_description["produce_cells"]) - 1)
        aisle_shape = (2, end_cell_height - begin_cell_height)

        grocery_cells_0 = []
        for col in range(begin_cell_height, begin_cell_height + aisle_shape[1]):
            for row in range(begin_cell_width, begin_cell_width + aisle_shape[0]):
                grocery_cells_0.append((row, col))
        self.__update_description(["grocery_cells_0", grocery_cells_0])

        grocery_cells = grocery_cells_0

        for current_aisle in range(1, number_of_aisles):
            previous_aisle = current_aisle - 1
            begin_cell_width = max(
                self._model_description["grocery_cells_{}".format(previous_aisle)])[0] + free_space_between_cells
            grocery_cells_i = []
            for col in range(begin_cell_height, begin_cell_height + aisle_shape[1]):
                for row in range(begin_cell_width, begin_cell_width + aisle_shape[0]):
                    grocery_cells_i.append((row, col))
            self.__update_description(["grocery_cells_{}".format(current_aisle), grocery_cells_i])
            grocery_cells += grocery_cells_i

        self.__update_description(["grocery_cells_all", grocery_cells])
        return grocery_cells

    def create_frozen_dept(self):
        if self._model_description["width"] * self._model_description["height"] >= 2000:  # for super-sized stores
            number_of_rows = 2
            free_space_between_cells = 3
        else:
            number_of_rows = 1
            free_space_between_cells = 2

        begin_cell_width = max(c[0] for c in self._model_description["grocery_cells_0"]) + free_space_between_cells
        begin_cell_height = min(c[1] for c in self._model_description["grocery_cells_0"])
        end_cell_height = max(c[1] for c in self._model_description["grocery_cells_0"]) + 1
        aisle_shape = (number_of_rows, end_cell_height - begin_cell_height)

        fridge_cells = []
        for col in range(begin_cell_height, begin_cell_height + aisle_shape[1]):
            for row in range(begin_cell_width, begin_cell_width + aisle_shape[0]):
                fridge_cells.append((row, col))
        self.__update_description(["fridge_cells", fridge_cells])

        begin_cell_height = min(c[1] for c in self._model_description["grocery_cells_0"])
        end_cell_height = max(c[1] for c in self._model_description["produce_aisle_cells"]) + 1

        aisle_cells = []
        for cell in range(begin_cell_height, end_cell_height):
            aisle_cells.append((self._model_description["width"] - 1, cell))
        self.__update_description(["aisle_cells", aisle_cells])

        frozen_cells = fridge_cells + aisle_cells
        self.__update_description(["frozen_cells", frozen_cells])

        return frozen_cells

    def create_liquor_dept(self):
        liquor_cells = []
        end_cell_height = min(c[1] for c in self._model_description["frozen_cells"]) - 1
        aisle_cells = []
        for cell in range(1, end_cell_height):
            aisle_cells.append((self._model_description["width"] - 1, cell))
        self.__update_description(["liquor_aisle_0", aisle_cells])
        liquor_cells += aisle_cells
        begin_cell_width = max(c[0] for c in self._model_description["grocery_cells_all"])
        aisle_cells = []
        for cell in range(begin_cell_width, self._model_description["width"] - 1):
            aisle_cells.append((cell, 0))
        self.__update_description(["liquor_aisle_1", aisle_cells])
        liquor_cells += aisle_cells

        return liquor_cells

    def create_checkout_dept(self):
        number_of_checkouts = self._model_description["number_of_grocery_aisles"] - 1

        begin_cell_height = min(c[1] for c in self._model_description["entry_cells"]) + 1
        end_cell_height = begin_cell_height + 2
        checkout_cells = []
        for checkout in range(0, number_of_checkouts):
            begin_cell_width = min(c[0] for c in self._model_description["grocery_cells_{}".format(checkout)])
            end_cell_width = begin_cell_width + 2

            checkout_cells_i = []
            for col in range(begin_cell_height, end_cell_height):
                for row in range(begin_cell_width, end_cell_width):
                    checkout_cells_i.append((row, col))
            self.__update_description(["checkout_cells_{}".format(checkout), checkout_cells_i])
            checkout_cells += checkout_cells_i
        last_checkout_cell = (min(checkout_cells)[0], min(checkout_cells[1]) - 1)
        checkout_cells.append((last_checkout_cell[0], last_checkout_cell[1]))
        return checkout_cells

    def create_other_depts(self):
        begin_cell_width = min(c[0] for c in self._model_description["produce_cells"]) + 1
        end_cell_width = self._model_description["width"] - 2
        other_cells = []
        for cell in range(begin_cell_width, end_cell_width + 1):
            other_cells.append((cell, self._model_description["height"] - 1))

        return other_cells

    def get_final_description(self):
        return self._model_description

    def generate_store(self):
        #  create entry cells
        entry_cell = self.create_entry()
        # self._occupied = self._occupied + entry_cell

        #  create produce department cells
        produce_cells = self.create_produce_dept()
        self._blocked_cells = self._blocked_cells + produce_cells

        #  create grocery department cells
        grocery_cells = self.create_grocery_dept()
        self._blocked_cells = self._blocked_cells + grocery_cells

        #  create frozen department cells
        frozen_cells = self.create_frozen_dept()
        self._blocked_cells = self._blocked_cells + frozen_cells

        #  create liquor department cells
        liquor_cells = self.create_liquor_dept()
        self._blocked_cells = self._blocked_cells + liquor_cells

        #  create checkout department cells
        checkout_cells = self.create_checkout_dept()
        self._blocked_cells = self._blocked_cells + checkout_cells

        #  create other department cells
        other_cells = self.create_other_depts()
        self._blocked_cells = self._blocked_cells + other_cells

        # extra corner cells
        self._blocked_cells.append((0, self._model_description["height"] - 1))
        self._blocked_cells.append((self._model_description["width"] - 1, self._model_description["height"] - 1))
        self._blocked_cells.append((self._model_description["width"] - 1, 0))

        return self._blocked_cells
