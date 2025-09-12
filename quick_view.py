import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def get_points(file_name: str) -> pd.DataFrame:
    
    data_path = f'DATA/{file_name}.txt'
    
    # header=26 and 7 spaces
    return pd.read_table(data_path, header=26, sep='      ', names=['2theta', 'intensity'], engine='python')

if __name__ == "__main__":

    # Get the points from the txt file
    file_name = sys.argv[1]
    data = get_points(file_name)

    # Plot the data
    x_axis = data['2theta']
    y_axis = data['intensity']
    plt.scatter(x_axis, y_axis, label='Data', s=0.5, color='black')

    # Plot info
    plt.xlabel("$2\\theta$ (degrees)", fontsize=14)
    plt.ylabel("Intensity (cps)", fontsize=14)
    plt.legend(fontsize=14)
    plt.title(f'XRD Analysis - Sample {file_name}', fontsize=16)
    # plt.grid(True)
    plt.xticks(np.arange(0, max(x_axis) + min(x_axis), 10))
    plt.ylim(0, max(y_axis) * 1.05)

 
    # Show the data
    plt.show()

