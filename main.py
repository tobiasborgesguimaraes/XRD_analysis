import numpy as np
import pandas as pd 
import sys 
import yaml
import shutil
import subprocess
import os

# This file should be executed along with the name of the file to be analysed, so to do it with the 'easy_data.txt' file, run 'uv run main.py easy_data', or 'python main.py easy_data'

args = sys.argv
if len(args) != 2:
    raise "This file should be called with a single argument (the name of the file to be analysed)"
else:
    file_name = args[1]



# Copy the data file to the amorph directory

shutil.copy2(f'DATA/{file_name}.txt', 'amorph/src')



# Edit the config.yaml file so that amorph can analyse the correct file

config_path = 'amorph/src/config.yaml'
with open(config_path, 'r') as f:
    # Load config.yaml file
    config = yaml.safe_load(f)

    # Apply the changes to the file
    config['data_file'] = f'{file_name}.txt'

with open(config_path, 'w') as f:
    # Save the changes to config.yaml
    yaml.dump(config, f)



# Run AMORPH.exe

exe_path = 'amorph//src//AMORPH.exe'
process = subprocess.Popen([exe_path])
process.wait()



# Save results file to the RESULTS directory




# Convert the results files to csv and json



# Run the analysis on the results file






