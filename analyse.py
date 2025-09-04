import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import sys
import os

def main():
    # Get arguments from command line
    file_name = sys.argv[1]
    print(sys.argv)

    # Get the points and model parameters from the data (file_name.txt and file_name_results.txt)
    points = get_points(file_name)
    params = get_parameters(file_name)

    # Create a new folder for storing all of the data
    os.makedirs(f'RESULTS/{file_name}_analysis', exist_ok=True)
    points.to_csv(f'RESULTS/{file_name}_analysis/points.csv', index=False)
    params.to_json(f'RESULTS/{file_name}_analysis/params.json', index=False)

    # Run some analysis to generate graphs and possibly other useful data
    simple_plot(file_name, points)


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

    num_peaks1 = results_single_line.at[0, 'num_peaks1']
    num_peaks2 = results_single_line.at[0, 'num_peaks2']
    
    backgound_parameters = {
            'background': results_single_line.at[0, 'background'],
            'n1': results_single_line.at[0, 'n_knots[0]'],
            'n2': results_single_line.at[0, 'n_knots[1]'],
            'n3': results_single_line.at[0, 'n_knots[2]'],
            'n4': results_single_line.at[0, 'n_knots[3]']
    }
    
    narrow_parameters = {
            'num_peaks': num_peaks1,
            'centers': [results_single_line.at[0, f'center1[{i}]'] for i in range(int(num_peaks1))],
            'widths': [results_single_line.at[0, f'width1[{i}]'] for i in range(int(num_peaks1))],
            'areas': [np.exp(results_single_line.at[0, f'log_amplitude1[{i}]']) for i in range(int(num_peaks1))]
    }

    wide_parameters = {
            'num_peaks': num_peaks2,
            'centers': [results_single_line.at[0, f'center2[{i}]'] for i in range(int(num_peaks2))],
            'widths': [results_single_line.at[0, f'width2[{i}]'] for i in range(int(num_peaks2))],
            'areas': [np.exp(results_single_line.at[0, f'log_amplitude2[{i}]']) for i in range(int(num_peaks2))]
    }

    # Save the parameters to a nested dictionary 
    dict_parameters = {'bg_params': backgound_parameters, 'narrow_params': narrow_parameters, 'wide_params': wide_parameters} 
    df = pd.DataFrame(dict_parameters)

    return df 


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
 
    plt.savefig(f'RESULTS/{file_name}_analysis/simple_plot', format='png')



if __name__ == "__main__":
    print('Run correctly!')
    main()


