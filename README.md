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
2. Use an environment manager to install the requirements from `requirements.txt` or install the requirements using the command `pip install -r requirements.txt` when in the repository directory
3. Run the `run_uniform_rpt_collection.py` script

OR

install from [PyPI](https://pypi.org/project/pumpia-uniform-phantom/) using pip:

    pip install pumpia-uniform-phantom

And run using the commands `pumpia-uniform-phantom` (making sure you are in the right environment if used for the pip install).

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

# Modules
## Subtraction SNR

Calculates SNR based on the subtraction method.
The ROI size is determined from the size input as a percentage of the phantom height and width.
The ROI is always centred on the phantom.
The following corrections can be applied:
- Bandwidth
- Pixel Size (includes slice width)
- Number of Averages
- Number of Phase Encode Steps

A button for showing the subtraction image is included.

## Uniformity

This is calculated using the integral uniformity method.
The size of the ROI is determined in the same way as the SNR module.

There is the option of applying a low pass kernel convolution to the image prior to calculation, this is defaulted to on.
The kernel is defined by

|    |    |    |
|----|----|----|
|1/16|2/16|1/16|
|2/16|4/16|2/16|
|1/16|2/16|1/16|
