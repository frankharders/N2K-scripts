# Data Processing & Dragen Automation Scripts

This repository includes three scripts designed to automate common data processing workflows related to SampleSheets and Dragen pipeline execution. Each script has a specific purpose, described in detail below with clear usage examples.

---

## 1. `01_split-into-project-folders.py`

**Purpose:**
- Splits a SampleSheet into project-specific folders.
- Creates directories based on project names extracted from the `[Cloud_Data]` section.
- Copies the corresponding `SampleSheet.csv` and FASTQ files into each project-specific directory.

### Usage:

```bash
python 01_split-into-project-folders.py
```

- The script prompts you to enter the working directory.
- Creates `script_log.txt` in the working directory with execution details (hostname, IP, Python version, user).

---

## 2. `02a_patch-UMI-into-samplesheet.py`

**Purpose:**
- Inserts fixed UMI-related lines into a SampleSheet immediately after the line beginning with `OverrideCycles`:
  ```
  CreateFastqForIndexReads,1
  TrimUMI,0
  ```
- Case-sensitive insertion.
- Logs execution details and errors.

### Usage:

```bash
python 02a_patch-UMI-into-samplesheet.py -i <input_file> -o <output_file> [--force]
```

**Example:**

```bash
python 02a_patch-UMI-into-samplesheet.py \
  -i /path/to/SampleSheet.csv \
  -o /path/to/SampleSheet.FH.csv \
  --force
```

- Logs:
  - General log: `insert_after_overridecycles.log`
  - Error log: `insert_after_overridecycles.err`

---

## 3. `02b_create.UMI.output.sh`

**Purpose:**
- Runs the Dragen command with specified parameters for BCL conversion.
- Handles command-line options and creates a detailed log file in the specified output directory.

### Usage:

```bash
./02b_create.UMI.output.sh -b <BCL_INPUT_DIR> -s <SAMPLE_SHEET> -o <OUTPUT_DIR> [-f]
```

**Example:**

```bash
./02b_create.UMI.output.sh \
  -b 250324_VH02146_11_AAGNTTGM5/ \
  -s 250324_VH02146_11_AAGNTTGM5/SampleSheet.FH.csv \
  -o 250324_VH02146_11_AAGNTTGM5/Analysis/final2 \
  -f
```

- Log file:
  - Created in the output directory: `dragen_run.log`
  - Contains execution details (user, hostname, command executed, date/time, and any errors).

---

## Prerequisites

- **Python:**
  - Script 1 (`01_split-into-project-folders.py`) is Python 2 compatible (adaptable to Python 3).
  - Script 2 (`02a_patch-UMI-into-samplesheet.py`) requires Python 3.

- **Bash:**
  - Script 3 (`02b_create.UMI.output.sh`) requires a Unix-like environment.

- **Dragen:**
  - Must be installed and accessible via command line.

---

## Logging

Each script provides extensive logging:

- **Script 1:** Logs details in `script_log.txt`.
- **Script 2:** Generates two logs (`insert_after_overridecycles.log`, `insert_after_overridecycles.err`).
- **Script 3:** Logs command execution details to `dragen_run.log`.

---

## Additional Notes

- Ensure dependencies (Python versions, Dragen) are correctly installed.
- Adjust file paths as needed.
- Logs ensure full transparency and traceability.

---

## License

Specify your license here (e.g., MIT License).

---

## Contact

For questions or issues, please contact [Frank Harders] at [frank.harders@wur.nl].

