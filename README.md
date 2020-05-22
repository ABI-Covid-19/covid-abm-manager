COVID-ABM-MANAGER
=================

A framework to manage various agent-based model simulations within a given spatial environment.

Required dependencies: 

- mesa
- pandas
- numpy
- dataclass

Optional dependencies:

- tornado (for web-based real-time visualisation of the model simulation)
- imageio & matplotlib (for off-line visualisation and animation generation)

To install all the dependencies, run: 

` pip install -r requirements.txt `

##### To run and visualise a simulation, you can simply run the following:

` python run_server.py `

This should open up a browser and show the simulation environment. You can tweak with the input parameters and 
start the simulation. You can stop, change the parameters, and reset the simulation at any time. 

If the browser does not automatically pop up, go to http://127.0.0.1:8521 page.

##### To run a simulation offline and save the data for later analysis:
 
 Change the input parameters inside the `main.py` file and run the file by simply:
 
 ` python main.py`
 
 At the end of the simulation, a `.csv` file should be saved which has all the data from the simulation. You can 
 then plot and analyze as you wish. However, there is also a simple script called `generate_animation.py` in the 
 `scripts` directory.
 
 ##### Current developments:
 ###### General:
 - Ability to pass arguments using `argparse`.
 
 ###### Model specific:
- Add environmental transmission e.g. surface touching.
- Add other environments e.g. school, workplace, restaurants etc.

###### Integration:
- Connect the [covid-transport-manager](https://github.com/ABI-Covid-19/covid-transport-manager) for an integrative 
modeling of the people flow in a city.
- Connect Unity Simulation and ML-Agents (e.g. 
[here](https://github.com/Unity-Technologies/unitysimulation-coronavirus-example)) for a nice environment settings
 and a more realistic navigation.
