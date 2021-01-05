import csv

def write_csv(filename, header, data):
    """Write the provided data to the CSV file.

    :param str filename: The name of the file to which the data should be written
    :param list header: The header for the columns in csv file
    :param list data: The list of list mapping the values to the columns
    """
    try:
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(data)
    except (IOError, OSError) as csv_file_error:
        print("Unable to write the contents to csv file. Exception: {}".format(csv_file_error))

if __name__ == '__main__':
    header = ['name', 'age', 'gender']
    data = [['Richard', 32, 'M'], ['Mumzil', 21, 'F'], ['Melinda', 25, 'F']]
    filename = 'sample_output.csv'
    write_csv(filename, header, data)
