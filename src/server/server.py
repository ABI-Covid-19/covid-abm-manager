from model.supermarket import SupermarketModel
from model.shopper import Shopper
from visualisation.continuous_module import Canvas

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, PieChartModule

COLORS = dict(Healthy="#46FF33", Risky="#00FFFF", Exposed="#9932CC", Infected="#FF3C33")
model_params = {"number_of_customers": UserSettableParameter("slider",
                                                             "Number of customers",
                                                             75, 1, 250,
                                                             description="Initial Number of People"),

                "number_of_infected": UserSettableParameter("slider",
                                                            "Number of symptomatic individuals",
                                                            1, 0, 100,
                                                            description="Number of symptomatic individuals"),
                "size": UserSettableParameter("choice",
                                              "Store size",
                                              "small",
                                              choices=["small", "medium", "large"],
                                              description="Options are currently small, medium, or large"),

                "social_distance_prob": UserSettableParameter("slider",
                                                              "prob",
                                                              70, 0, 100,
                                                              description="Probability of individuals practicing"
                                                                          "social distancing"),
                }


def shopper_portrayal(agent):
    """
    Get the shoppers' information for real-time visualisation.

    :param agent:
    :return:
    """

    if agent is None:
        return

    portrayal = {}

    #  update portrayal characteristics for each Shopper object
    if isinstance(agent, Shopper):
        if agent.pos is None:
            return None
        (position_x, position_y) = agent.pos
        portrayal["x"] = position_x
        portrayal["y"] = position_y
        portrayal["Shape"] = "circle"
        portrayal["r"] = 3
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = COLORS[agent.state.value]

    return portrayal


supermarket_canvas = Canvas(shopper_portrayal, 500, 500)

line_chart = ChartModule(
    [
        {"Label": "Healthy", "Color": COLORS["Healthy"]},
        {"Label": "Risky", "Color": COLORS["Risky"]},
        {"Label": "Exposed", "Color": COLORS["Exposed"]},
        {"Label": "Infected", "Color": COLORS["Infected"]},
    ]
)

pie_chart = PieChartModule(
    [
        {"Label": "Healthy", "Color": COLORS["Healthy"]},
        {"Label": "Risky", "Color": COLORS["Risky"]},
        {"Label": "Exposed", "Color": COLORS["Exposed"]},
        {"Label": "Infected", "Color": COLORS["Infected"]},
    ]
)

server = ModularServer(SupermarketModel, [supermarket_canvas, line_chart, pie_chart], "ABI-COVID-19-ABM", model_params)
