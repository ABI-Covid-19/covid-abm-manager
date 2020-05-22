import abc


class AbstractStorePlanner(metaclass=abc.ABCMeta):
    # __metaclass__ = abc.ABCMeta

    """
    Abstract class for store design and generation.
    """

    @abc.abstractmethod
    def create_entry(self):
        """
        Designing the floor plan for the entry gate.
        :return:
        """
        pass

    @abc.abstractmethod
    def create_produce_dept(self):
        """
        Designing the floor plan for the produce department.
        :return:
        """
        pass

    def create_grocery_dept(self):
        """
        Designing the floor plan for the grocery department
        :return:
        """
        pass

    def create_frozen_dept(self):
        """
        Designing the floor plan for the frozen department
        :return:
        """
        pass

    def create_liquor_dept(self):
        """
        Designing the floor plan for the liquor department
        :return:
        """
        pass

    def create_checkout_dept(self):
        """
        Designing the floor plan for the checkout department
        :return:
        """
        pass

    def create_other_depts(self):
        """
        Designing the floor plan for the rest of the store
        :return:
        """
        pass

