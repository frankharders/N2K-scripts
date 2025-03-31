import os
import shutil
import socket
import sys
import getpass
import readline
import glob
from datetime import datetime

# Function to auto-complete paths
def complete_path(text, state):
    line = readline.get_line_buffer().split()
    return [x for x in glob.glob(os.path.expanduser(text) + '*')][state]

# Register the completer function
readline.set_completer(complete_path)
readline.parse_and_bind("tab: complete")

# Ask for user input for the working directory with autofill
working_directory = raw_input("Enter the working directory: ")

# Change to the working directory
os.chdir(working_directory)

# Get the hostname
hostname = socket.gethostname()

# Get the IPv4 address of the hostname
ip_address = socket.gethostbyname_ex(hostname)[2][0]

# Get the Python version
python_version = sys.version

# Get the username
user = getpass.getuser()

# Print the hostname, IP address, Python version, and username
print("Hostname: {}".format(hostname))
print("IP Address: {}".format(ip_address))
print("Python Version: {}".format(python_version))
print("User: {}".format(user))

# Log all necessary information in a log file with date and time
log_file = "script_log.txt"
with open(log_file, 'a') as log:
    log.write("Date and Time: {}\n".format(datetime.now()))
    log.write("Hostname: {}\n".format(hostname))
    log.write("IP Address: {}\n".format(ip_address))
    log.write("Python Version: {}\n".format(python_version))
    log.write("User: {}\n".format(user))
    log.write("\n\n")

# Define the base directory
base_dir = 'Analysis/'

# Get the list of folders in the base directory
folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

# Sort folders by modification time and choose the latest one
latest_folder = max(folders, key=lambda x: os.path.getmtime(os.path.join(base_dir, x)))

# Define the path to the SampleSheet.csv file in the latest folder and one level deeper in data
sample_sheet_path = os.path.join(base_dir, latest_folder, 'Data', 'SampleSheet.csv')

# Read the content of the SampleSheet.csv file
with open(sample_sheet_path, 'r') as file:
    lines = file.readlines()

# Find the start of the [Cloud_Data] section
start_index = None
for i, line in enumerate(lines):
    if line.strip() == '[Cloud_Data]':
        start_index = i + 1
        break

# Extract the [Cloud_Data] section
if start_index is not None:
    cloud_data_lines = lines[start_index:]

    # Process the [Cloud_Data] section as a table
    header = cloud_data_lines[0].strip().split(',')
    data_lines = [line.strip().split(',') for line in cloud_data_lines[1:] if line.strip()]

    # Create a set of unique project names from column 2
    unique_projects = set(data_line[1] for data_line in data_lines if len(data_line) > 1)

    # Create directories for each unique project in the current directory
    for project_name in unique_projects:
        project_dir = os.path.join(os.getcwd(), project_name)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Copy SampleSheet.csv to each project directory
        shutil.copy(sample_sheet_path, project_dir)

        # Print the project directory (for verification)
        print('Project Directory: {}'.format(project_dir))

    print("Unique directories have been created for each project.")

    # Define the base directory for fastq files
    fastq_base_dir = os.path.join(base_dir, latest_folder, 'Data', 'fastq')

    if os.path.exists(fastq_base_dir):
        for data_line in data_lines:
            sample_name = data_line[0]
            project_name = data_line[1]

            # List all fastq files in the fastq_base_dir with the specified syntax
            fastq_files = [f for f in os.listdir(fastq_base_dir) if f.startswith(sample_name) and ('_R1' in f or '_R2' in f) and f.endswith('.fastq.gz')]

            # Copy fastq files to the corresponding project directory
            for fastq_file in fastq_files:
                src_path = os.path.join(fastq_base_dir, fastq_file)
                dest_path = os.path.join(os.getcwd(), project_name, fastq_file)
                shutil.copy(src_path, dest_path)

                # Print the copy operation (for verification)
                print('Copied {} to {}'.format(fastq_file, dest_path))
    else:
        print('The directory {} does not exist.'.format(fastq_base_dir))
else:
    print('The [Cloud_Data] section was not found in the SampleSheet.csv file.')

# Documentation:
"""
This script performs several tasks:

1. Auto-complete paths using tab completion.
2. Ask for user input to specify a working directory.
3. Change to the specified working directory.
4. Retrieve and print system information including hostname, IPv4 address, Python version, and username.
5. Log all necessary information including date and time, hostname, IPv4 address, Python version, username into a log file.
6. Define a base directory and get a list of folders within it.
7. Sort folders by modification time and select the latest one.
8. Define a path to a SampleSheet.csv file within the latest folder.
9. Read and process the content of SampleSheet.csv to extract a specific section ([Cloud_Data]).
10. Create unique directories based on project names found within the [Cloud_Data] section.
11. Copy SampleSheet.csv to each constructed project directory.
12. Define a base directory for fastq files and copy relevant files to corresponding project directories.

The script is designed to automate tasks related to organizing project directories and copying relevant files while logging important system information.
"""
