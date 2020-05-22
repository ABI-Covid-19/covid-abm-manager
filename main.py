from src.model.supermarket import SupermarketModel


def run_model(model, steps=300):
    for _ in range(steps):
        model.step()


def run_batch():
    # TODO: Need to write a func to run the model multiple times with a set of fixed params and a set of variable params
    pass


# TODO: Use argparse for user input arguments.


if __name__ == '__main__':
    n_customers = 10
    n_infected = 5
    social_distance_prob = 0.90
    time_steps = 2880  # 12 hours (every time step is 15 seconds; i.e. 4*60*12)

    supermarket_model = SupermarketModel(number_of_customers=n_customers,
                                         number_of_infected=n_infected,
                                         size='small',
                                         social_distance_prob=social_distance_prob)

    run_model(supermarket_model, steps=time_steps)
    model_results = supermarket_model.get_simulation_result()
    model_results.to_csv('supermarket_abm_simulation.csv')
