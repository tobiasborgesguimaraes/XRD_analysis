import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


def get_points(file_name: str) -> pd.DataFrame:
    
    data_path = f'DATA/{file_name}.txt'

    return pd.read_table(data_path, header=26, sep='       ', names=['2theta', 'intensity'], engine='python')


def quick_view(file_name: str, data: pd.DataFrame):
    
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
    plt.xlim(0, 85)
    plt.ylim(0, max(y_axis) * 1.05)

    # Show the data
    plt.show()


def model_plot(file_name: str, data: pd.DataFrame):
    
    # Get the points from the df
    x_axis = data['2theta']
    y_axis = data['intensity']
    bg = data['bg']
    wide = data['wide']
    narrow = data['narrow']
    model = data['model_curve']

    # Plot the data
    plt.scatter(x_axis, y_axis, label='Data', s=0.5, color='black')
    plt.plot(x_axis, bg, label='Background', linewidth=2, color='orange')
    plt.plot(x_axis, wide, label='Amorphous', linewidth=2, color='blue')
    plt.plot(x_axis, narrow, label='Crystalline', linewidth=2, color='red')
    plt.plot(x_axis, model, label='Model Curve', linewidth=2, color='green')
     

    # Plot info
    plt.xlabel("$2\\theta$ (degrees)", fontsize=14)
    plt.ylabel("Intensity (cps)", fontsize=14)
    plt.legend(fontsize=14)
    plt.title(f'XRD Analysis - Sample {file_name}', fontsize=16)
    # plt.grid(True)
    plt.xlim(0, 85)
    plt.ylim(0, max(y_axis) * 1.05)

    # Show the data
    plt.show()






if __name__ == "__main__":
    print('Running correctly')
    
    # Get the points from the txt file
    file_name = sys.argv[1]

    # Read hdf5 file
    hdf_file = pd.read_hdf(f'HDF5_files/{file_name}.h5', key='Points')
    print(hdf_file)

    quick_view(file_name, hdf_file)
    model_plot(file_name, hdf_file)






