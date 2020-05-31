from src.api import SimpleAPI


def run_batch():
    # TODO: Need to write a func to run the model multiple times with a set of fixed params and a set of variable params
    pass


# TODO: Use argparse for user input arguments.


def _model_parameters():
    params = {
        'model': 'supermarket',
        'number': 20,
        'infected': 1,
        'prob': 0.7,
        'size': 'small',
        'time': 300
    }
    return params


if __name__ == '__main__':
    sapi = SimpleAPI()

    """ option 1:
    pass a dictionary of the model parameters
    """
    sapi.set_model_descriptions(_model_parameters())
    sapi.run_model()
    # result = sapi.get_model_results()
    # sapi.save_model_results("supermarket_simulation_results.csv")

    """ option 2:
    explicitly set the model parameters with individual api methods
    """
    sapi.set_model('supermarket')
    sapi.set_number_of_agents(10)
    sapi.set_number_of_infected(2)
    sapi.set_social_distance_prob(0.7)
    sapi.set_store_size('small')
    sapi.set_time_steps(300)
    sapi.run_model()
    # result = sapi.get_model_results()
    # sapi.save_model_results("supermarket_simulation_results.csv")
