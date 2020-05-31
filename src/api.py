from src.model.supermarket import SupermarketModel


class ModelDescription:

    def __init__(self):
        self.__model__ = dict(supermarket=SupermarketModel)
        self.__description = {}
        self._model = None
        self._model_results = None

    def update_description(self, key, value):
        self.__description[key] = value

    def update_from_json(self, description):
        self.__description = description

    def run_model(self):
        model = self.__model__[self.__description['model']]
        self._model = model(self.__description['number'],
                            self.__description['infected'],
                            self.__description['prob'],
                            self.__description['size'])
        self.__run()

    def __run(self):
        for _ in range(self.__description['time']):
            self._model.step()

    def get_results(self):
        self._model_results = self._model.get_simulation_result()
        return self._model_results

    def save_results(self, path_to_file):
        self._model_results.to_csv(path_to_file)


class SimpleAPI:

    def __init__(self):
        self._model_description = ModelDescription()

    def set_model_descriptions(self, description):
        self._model_description.update_from_json(description)

    def set_model(self, model='supermarket'):
        self._model_description.update_description('model', model)

    def set_number_of_agents(self, num=20):
        self._model_description.update_description('number', num)

    def set_number_of_infected(self, num=1):
        self._model_description.update_description('infected', num)

    def set_social_distance_prob(self, prob=0.7):
        self._model_description.update_description('prob', prob)

    def set_store_size(self, size='small'):
        self._model_description.update_description('size', size)

    def set_time_steps(self, time=2880):
        """
        Set time-step. Every time step is 15 seconds.

        :param time: default is 12 hours.
        :return:
        """
        self._model_description.update_description('time', time)

    def run_model(self):
        self._model_description.run_model()

    def get_model_results(self):
        return self._model_description.get_results()

    def save_model_results(self, path_to_file):
        self._model_description.save_results(path_to_file)
