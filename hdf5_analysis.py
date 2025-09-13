import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import sys

x_ray_sources = {
        'Cu': 1.54,
        'Mo': 0.71,
        'Cr': 2.29,
        'Co': 1.79,
}

def main(file_name):
    
    # Get the points and model parameters from the data (file_name.txt and file_name_results.txt)
    points = get_points(file_name)
    bg_params, narrow_params, wide_params = get_parameters(file_name)

    # Run some analysis to generate graphs and possibly other useful data
    # simple_plot(file_name, points)

    # Save everything into an hdf5 file
    with pd.HDFStore(f'HDF5_files/{file_name}.h5', 'w') as store:
        store['Points'] = points
        store['BG_Parameters'] = bg_params 
        store['NA_Parameters'] = narrow_params
        store['WI_Parameters'] = wide_params


def get_points(file_name: str) -> pd.DataFrame:
    
    data_path = f'DATA/{file_name}.txt'
    results_path = f'RESULTS/{file_name}_results.txt'

    data = pd.read_table(data_path, header=26, sep='       ', names=['2theta', 'intensity'], engine='python')
    size = len(data)

    with open(results_path, 'r') as file:
        content = file.read()[3:] # The indexing is here to disconsider the '#  ' at the beggining of posterior_sample.txt
        lines = content.splitlines()

        listColumnNames = lines[0].split(sep=', ')
        listNumbers = [float(n) for n in lines[-1].split()]


    my_dict = dict(zip(listColumnNames, listNumbers))
    results_single_line = pd.DataFrame(my_dict, [0])

    # Finally put the info inside posterior_sample.txt into our dataFrame
    data['q'] = [(4 * np.pi * np.sin(np.radians(a)/2)/(x_ray_sources['Cu'])) for a in data['2theta']]
    data['bg'] = [results_single_line.at[0, f'bg[{i}]'] for i in range(size)]
    data['wide'] = [results_single_line.at[0, f'wide[{i}]'] for i in range(size)]
    data['narrow'] = [results_single_line.at[0, f'narrow[{i}]'] for i in range(size)]
    data['model_curve'] = [results_single_line.at[0, f'model_curve[{i}]'] for i in range(size)]

    # Return our dataFrame
    return data


def get_parameters(file_name: str) -> pd.DataFrame:
    
    results_path = f'RESULTS/{file_name}_results.txt'

    # Load the content into the results file
    with open(results_path, 'r') as file:
      content = file.read()[3:] # The indexing is here to disconsider the '#  ' at the beggining of posterior_sample.txt
      lines = content.splitlines()

      listColumnNames = lines[0].split(sep=', ')
      listNumbers = [float(n) for n in lines[-1].split()]

    my_dict = dict(zip(listColumnNames, listNumbers))
    results_single_line = pd.DataFrame(my_dict, [0]) # That's a table with a single line, and each column is a parameter inside the original posterior_sample.txt

    num_peaks1 = results_single_line.at[0, 'num_peaks1'] # for narrow parameters
    num_peaks2 = results_single_line.at[0, 'num_peaks2'] # for wide parameters
    
    background_parameters = pd.DataFrame({
            'background': [results_single_line.at[0, 'background']],
            'n1': [results_single_line.at[0, 'n_knots[0]']],
            'n2': [results_single_line.at[0, 'n_knots[1]']],
            'n3': [results_single_line.at[0, 'n_knots[2]']],
            'n4': [results_single_line.at[0, 'n_knots[3]']]
    })
    
    narrow_parameters = pd.DataFrame({
            'centers': [results_single_line.at[0, f'center1[{i}]'] for i in range(int(num_peaks1))],
            'widths': [results_single_line.at[0, f'width1[{i}]'] for i in range(int(num_peaks1))],
            'areas': [np.exp(results_single_line.at[0, f'log_amplitude1[{i}]']) for i in range(int(num_peaks1))]
    })

    wide_parameters = pd.DataFrame({
            'centers': [results_single_line.at[0, f'center2[{i}]'] for i in range(int(num_peaks2))],
            'widths': [results_single_line.at[0, f'width2[{i}]'] for i in range(int(num_peaks2))],
            'areas': [np.exp(results_single_line.at[0, f'log_amplitude2[{i}]']) for i in range(int(num_peaks2))]
    })

     

    return background_parameters, narrow_parameters, wide_parameters 


def simple_plot(file_name: str, data: pd.DataFrame):
    x_axis = data['2theta']
    y_axis = data['intensity']
    wide = data['wide']
    narrow = data['narrow']
    bg = data['bg']
    model = data['model_curve']

    plt.scatter(x_axis, y_axis, s=1.0, c='black', label='Data')
    plt.plot(x_axis, wide, linewidth=2, color='blue', label='Amorphous')
    plt.plot(x_axis, narrow, linewidth=2, color='red', label='Crystalline')
    plt.plot(x_axis, bg, linewidth=2, color='yellow', label='Background')
    plt.plot(x_axis, model, linewidth=2, color='green', label='Model Curve')

    plt.title(f"XRD Analysis - Sample {file_name}")
    plt.xlabel("$2\\theta$ (degrees)", fontsize=14)
    plt.ylabel("intensity (cps)", fontsize=14)
    plt.legend(fontsize=14)
    plt.xlim(0, 85)
    plt.ylim(0, max(y_axis) * 1.05)
 
    plt.savefig('simple_plot', format='png')

if __name__ == "__main__":
    print('Run correctly!')
    
    # Get arguments from command line
    file_names = sys.argv[1:]
    
    for name in file_names:
        main(name)


