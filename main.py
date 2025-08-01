import numpy as np 
import pandas as pd 
import sys 
import os
import yaml


args = sys.argv
print(args)
if len(args) != 2:
    raise "This file should be called with a single argument (the name of the file to be analysed)"
else:
    file_name = args[1]


# copy the data file to the amorph directory
os.system(f"cp DATA/{file_name}.txt amorph/src")




config_path = 'amorph/src/config.yaml'
with open(config_path, 'r') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
    
    config['data_file'] = f'{file_name}.txt'
with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)










