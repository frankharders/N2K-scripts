#!/bin/bash
#
# run_dragen.sh
#
# Description:
#   This script runs the Dragen command with the following fixed options:
#
#     --bcl-conversion-only true
#     --bcl-input-directory <BCL_INPUT_DIR>
#     --sample-sheet <SAMPLE_SHEET>
#     --output-directory <OUTPUT_DIR>
#     --force (if specified)
#
#   The script accepts command-line options:
#     -b   BCL input directory
#     -s   Sample sheet file
#     -o   Output directory (where the log file will also be stored)
#     -f   Optional flag to force overwrite (adds the "--force" option)
#
#   The script creates a log file named "dragen_run.log" in the output directory
#   and logs the user, hostname, date, time, the command that was run, and all output/errors.
#
# Usage:
#   ./run_dragen.sh -b <BCL_INPUT_DIR> -s <SAMPLE_SHEET> -o <OUTPUT_DIR> [-f]
#

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print usage instructions and exit
usage() {
    echo "Usage: $0 -b <BCL_INPUT_DIR> -s <SAMPLE_SHEET> -o <OUTPUT_DIR> [-f]"
    exit 1
}

# Parse command-line options
FORCE_FLAG=""
while getopts "b:s:o:f" opt; do
    case $opt in
        b)
            BCL_INPUT_DIR="$OPTARG"
            ;;
        s)
            SAMPLE_SHEET="$OPTARG"
            ;;
        o)
            OUTPUT_DIR="$OPTARG"
            ;;
        f)
            FORCE_FLAG="--force"
            ;;
        *)
            usage
            ;;
    esac
done

# Check for required parameters
if [[ -z "$BCL_INPUT_DIR" || -z "$SAMPLE_SHEET" || -z "$OUTPUT_DIR" ]]; then
    echo "Error: Missing required parameters."
    usage
fi

# Create output directory if it does not exist
mkdir -p "$OUTPUT_DIR"

# Define log file (stored in the output directory)
LOGFILE="$OUTPUT_DIR/dragen_run.log"

# Write header information to the log file
{
    echo "==============================="
    echo "Dragen Run Log"
    echo "Date: $(date)"
    echo "User: $(whoami)"
    echo "Hostname: $(hostname)"
    echo "-------------------------------"
    echo "Running command:"
    echo "dragen --bcl-conversion-only true --bcl-input-directory \"$BCL_INPUT_DIR\" --sample-sheet \"$SAMPLE_SHEET\" --output-directory \"$OUTPUT_DIR\" $FORCE_FLAG"
    echo "==============================="
} >> "$LOGFILE"

# Run the Dragen command and log both standard output and errors
dragen --bcl-conversion-only true \
       --bcl-input-directory "$BCL_INPUT_DIR" \
       --sample-sheet "$SAMPLE_SHEET" \
       --output-directory "$OUTPUT_DIR" $FORCE_FLAG 2>&1 | tee -a "$LOGFILE"

# Log the completion time
echo "===============================" >> "$LOGFILE"
echo "Dragen run completed on $(date)" >> "$LOGFILE"

