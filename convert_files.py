import pandas as pd 
import numpy as np 



def convert_results_to_csv(file_name):
    
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

    # Save the data to a CSV file
    data_output_path = f'RESULTS/{file_name}_results.csv'
    data.to_csv(data_output_path, index=False)



def convert_parameters_to_json(file_name):
    pass










