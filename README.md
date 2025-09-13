# XRD_analysis

## Description

This repository was made as a complement for the [amorph](https://bitbucket.org/eggplantbren/amorph) repository (A program build for analysing X-Ray Diffraction in amorphous materials). It takes the `posterior_sample.txt` that [amorph](https://bitbucket.org/eggplantbren/amorph) generates, and build an HDF5 file for easier access to the data.   

The python environment is managed with `uv` and the code also includes a `graphs.py` file to generate graphs with the HDF5 output. **The usability and features are still being worked on**.

## How to use the program

After cloning the repository, you can either move all the files to the `src` folder in the `amorph` directory, or use them in different folders. If you're going for the first option, remember to change the path inside `config.yaml` to include the `DATA` directory.

After analysing your XRD file (stored as `{file_name}.txt`) with [amorph](https://bitbucket.org/eggplantbren/amorph). Copy the `posterior_sample.txt` file to the `RESULTS` directory and named it `{file_name}_results.txt`. After doing that you can run `uv run hdf5/_analysis.py {file_name}` to create the HDF5. It also works with a list of file names.

Then, by using `uv run graphs.py {file_name}` you'll get a view of the amorph's ouput. As well as the graphs being saved in the `GRAPHS` directory. 













