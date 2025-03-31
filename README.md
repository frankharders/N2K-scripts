# Data Processing & Dragen Automation Tools

This repository contains a collection of scripts designed to automate data processing tasks and to streamline the execution of the Dragen pipeline. The tools included are used for splitting project folders, patching sample sheets with UMI-related information, and wrapping the Dragen command with detailed logging.

## Repository Contents

- **01_split-into-project-folders.py**  
  This script:
  - Prompts the user for a working directory (with auto-completion support).
  - Changes to the specified working directory.
  - Retrieves system information (hostname, IP address, Python version, and username) and logs it.
  - Finds the latest project folder in the `Analysis/` directory.
  - Reads a `SampleSheet.csv` file from the latest folder (inside a `Data` subdirectory).
  - Extracts the `[Cloud_Data]` section, creates unique project directories based on project names, and copies the `SampleSheet.csv` and related FASTQ files into these directories.

- **02a_patch-UMI-into-samplesheet.py**  
  This script:
  - Reads an input `SampleSheet.csv` file.
  - Searches for the first line that starts with `OverrideCycles` (case sensitive).
  - Inserts two fixed text lines immediately after that line:
    ```
    CreateFastqForIndexReads,1
    TrimUMI,0
    ```
  - Writes the modified content to a specified output file.
  - Logs all operations and errors in two log files (general and error logs) that are stored in the same directory as the output file.

- **02b_create.UMI.output.sh**  
  This Bash script:
  - Wraps the Dragen command with fixed options for BCL conversion.
  - Accepts command-line options for:
    - **BCL input directory** (`-b`)
    - **Sample sheet file** (`-s`)
    - **Output directory** (`-o`)
    - **Force flag** (`-f`) – to force overwriting if necessary.
  - Creates a log file (`dragen_run.log`) in the output directory that records the user, hostname, date, time, the exact command executed, and any errors.

## Requirements

- **Python:**  
  - `01_split-into-project-folders.py` can run on Python 2 (with `raw_input`) or can be adapted for Python 3.
  - `02a_patch-UMI-into-samplesheet.py` is written for Python 3.
- **Bash:**  
  - `02b_create.UMI.output.sh` is a Bash script and requires a Unix-like environment.
- **Dragen:**  
  - The Dragen tool must be installed and available in your PATH for the Bash wrapper to execute the command successfully.

## Usage

### 1. Splitting Project Folders

Run the script to organize files based on project names:

```bash
python 01_split-into-project-folders.py



- **02a_patch-UMI-into-samplesheet.py** 



python 02a_patch-UMI-into-samplesheet.py -i <input_file> -o <output_file> --force


python 02a_patch-UMI-into-samplesheet.py -i /path/to/SampleSheet.csv -o /path/to/SampleSheet.FH.csv --force

./02b_create.UMI.output.sh -b <BCL_INPUT_DIR> -s <SAMPLE_SHEET> -o <OUTPUT_DIR> [-f]


./02b_create.UMI.output.sh -b 250324_VH02146_11_AAGNTTGM5/ \
-s 250324_VH02146_11_AAGNTTGM5/SampleSheet.FH.csv \
-o 250324_VH02146_11_AAGNTTGM5/Analysis/final2 -f



