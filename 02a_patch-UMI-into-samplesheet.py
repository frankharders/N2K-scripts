#!/usr/bin/env python3
"""
Script: patch2UMI-csv.py

Description:
    This script adds fixed text lines to a SampleSheet.csv file immediately after the line that starts with "OverrideCycles".
    The fixed text to be inserted is:

        CreateFastqForIndexReads,1
        TrimUMI,0

    The insertion is case sensitive.

    Additionally, the script logs both general and error messages (including username, hostname, date, and time)
    and checks if the output file already exists. If so, it requires the --force option to overwrite it.
    Both log files (general and error) are stored in the same directory as the output file.

Usage:
    Make the script executable and run it with the following parameters:

        python patch2UMI-csv.py -i <input_file> -o <output_file> [--force]

Parameters:
    -i, --input   : Path to the original SampleSheet.csv file.
    -o, --output  : Path to the output file (modified SampleSheet.csv).
    -f, --force   : Overwrite the output file if it already exists.

Log Files:
    - General log: insert_after_overridecycles.log (stored in the output file's directory)
    - Error log:   insert_after_overridecycles.err (stored in the output file's directory)

Example:
    python patch2UMI-csv.py -i /path/to/SampleSheet.csv \
    -o /path/to/new_SampleSheet.csv --force

Notes:
    - The script searches for the first line that starts exactly with "OverrideCycles" (case sensitive, ignoring leading whitespace).
    - If this line is not found, the script exits with an error message and logs the error.
    - The fixed text lines are inserted preserving newline characters.
"""

import argparse
import os
import sys
import logging
import socket
import getpass
import io  # For compatibility with Python 2 and 3

# Global logger; configuration will be set up in main()
logger = logging.getLogger(__name__)

# Custom filter to add username and hostname to log records
class ContextFilter(logging.Filter):
    def filter(self, record):
        record.username = getpass.getuser()
        record.hostname = socket.gethostname()
        return True

# Fixed text lines to be inserted after "OverrideCycles"
if sys.version_info[0] < 3:
    FIXED_INSERT_LINES = [unicode("CreateFastqForIndexReads,1", "utf-8"),
                          unicode("TrimUMI,0", "utf-8")]
else:
    FIXED_INSERT_LINES = ["CreateFastqForIndexReads,1", "TrimUMI,0"]

def insert_text_after_overridecycles(input_file, output_file):
    """
    Reads the input CSV file, searches for the line starting with 'OverrideCycles', and inserts the fixed text lines immediately after it.
    The modified content is written to the specified output file.

    Args:
        input_file (str): Path to the original SampleSheet.csv file.
        output_file (str): Path where the modified file should be saved.

    Raises:
        SystemExit: If the input file does not exist, cannot be read, or if the 'OverrideCycles' line is not found.
    """
    logger.info("Starting to process input file: {}".format(input_file))

    try:
        with io.open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        logger.info("Successfully read {} lines from {}".format(len(lines), input_file))
    except Exception as e:
        error_msg = "Error reading '{}': {}".format(input_file, e)
        logger.error(error_msg)
        sys.exit(error_msg)

    output_lines = []
    inserted = False

    # Process the file line by line
    for line in lines:
        output_lines.append(line)
        # Check if this line starts with "OverrideCycles" (ignoring leading whitespace)
        if not inserted and line.lstrip().startswith("OverrideCycles"):
            logger.info("Found line starting with 'OverrideCycles'. Inserting fixed text lines.")
            for text in FIXED_INSERT_LINES:
                if not text.endswith("\n"):
                    text += "\n"
                output_lines.append(text)
                logger.debug("Inserted line: {}".format(text.strip()))
            inserted = True

    if not inserted:
        error_msg = "Error: No line starting with 'OverrideCycles' found in the input file."
        logger.error(error_msg)
        sys.exit(error_msg)

    try:
        with io.open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(output_lines)
        logger.info("Insertion complete. Modified file saved as: {}".format(output_file))
        print("Insertion complete. Modified file saved as: {}".format(output_file))
    except Exception as e:
        error_msg = "Error writing to '{}': {}".format(output_file, e)
        logger.error(error_msg)
        sys.exit(error_msg)

def main():
    parser = argparse.ArgumentParser(
        description="Insert fixed text lines into a SampleSheet.csv file immediately after the line starting with 'OverrideCycles'."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the original SampleSheet.csv file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file (modified SampleSheet.csv).")
    parser.add_argument("-f", "--force", action="store_true", default=False,
                        help="Force overwrite of the output file if it already exists.")
    opts = parser.parse_args()

    # Check if the input file exists; if not, print error message and usage instructions
    if not os.path.isfile(opts.input):
        print("Error: Input file '{}' does not exist.".format(opts.input))
        parser.print_usage()
        sys.exit(1)

    # Check if the output file already exists and the force option is not specified
    if os.path.isfile(opts.output) and not opts.force:
        print("Output file '{}' already exists. Use the --force option to overwrite it.".format(opts.output))
        parser.print_usage()
        sys.exit(1)

    # Determine the output directory to store the log files
    output_dir = os.path.dirname(os.path.abspath(opts.output))
    if not output_dir:
        output_dir = "."

    # Set up logging handlers to store logs in the output directory
    log_file = os.path.join(output_dir, "insert_after_overridecycles.log")
    err_log_file = os.path.join(output_dir, "insert_after_overridecycles.err")

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(username)s@%(hostname)s - %(levelname)s - %(message)s')

    info_handler = logging.FileHandler(log_file)
    info_handler.setLevel(logging.DEBUG)
    info_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(err_log_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Clear any existing handlers
    logger.handlers = []
    # Add custom context filter
    context_filter = ContextFilter()
    info_handler.addFilter(context_filter)
    error_handler.addFilter(context_filter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    logger.info("Script started")
    insert_text_after_overridecycles(opts.input, opts.output)
    logger.info("Script completed successfully")

if __name__ == '__main__':
    main()
