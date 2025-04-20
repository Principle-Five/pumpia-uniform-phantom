# Introduction
This repository contains code to analyse a uniform phantom using the [PumpIA](https://github.com/Principle-Five/pumpia) framework.
It uses the subtraction SNR method and therefore expects a repeat image, however the uniformity module will run with a single image.

It is currently not validated and is provided as is, see the license for more information.

The collection contains the following tests:
- SNR
- Uniformity

# Usage

Users should make themselves familiar with the [PumpIA user interface](https://principle-five.github.io/pumpia/usage/user_interface.html)

To run the collection:
1. Clone the repository
2. Install the requirements using the command `pip install -r requirements.txt` when in the repository directory
3. Run the `run_uniform_rpt_collection.py` script

To use the collection:
1. Load the folder with the relevant images
2. Drag and drop the series containing the relevant images into the viewer of the `Main` tab
3. Generate the ROIs and run analysis
4. Correct the context if required (see below)
    - Re-run generating ROIs
5. Move any ROIs as required, this should be done through their relevant modules.
    - Re-run analysis
6. Copy the results in the relevant format. Horizontal is tab separated, vertical is new line separated.

## Correcting Context

The context used for this collection is the Auto Phantom Context Manager provided with PumpIA, see the [relevant documentation](https://principle-five.github.io/pumpia/usage/user_interface.html) for this.
