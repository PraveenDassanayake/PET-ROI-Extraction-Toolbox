# PET ROI Extraction Toolbox

A user-friendly Python GUI toolbox integrated with MATLAB SPM12 for atlas-based ROI extraction from preprocessed PET SUV brain images.

This toolbox allows users to load multiple PET images, apply a brain atlas in MNI space, optionally apply a gray matter mask, and extract mean PET values for each region of interest (ROI). The output is saved as a subject-by-ROI CSV table that can be used for downstream statistical analysis, visualization, or correlation with biological and clinical variables.

---

## Overview

Quantitative PET brain analysis often requires extracting regional values from anatomical or functional brain atlases. This process can be repetitive, time-consuming, and prone to manual errors when performed subject-by-subject.

The PET ROI Extraction Toolbox simplifies this workflow by providing a graphical interface where users can:

* Load multiple preprocessed PET SUV images
* Load a brain atlas in MNI space
* Optionally load a gray matter mask
* Select specific ROI numbers or automatically detect all atlas labels
* Extract mean PET values per ROI
* Export results as a CSV table
* Preview results inside the GUI

The toolbox is designed for researchers who want to perform standardized ROI-based PET quantification without manually editing scripts for each subject or atlas.

---

## Features

* Python-based graphical user interface
* MATLAB SPM12 backend for NIfTI image handling
* Multiple-subject PET image loading
* Custom atlas support
* Automatic ROI label detection from atlas
* Optional gray matter mask application
* Manual ROI selection using comma-separated labels
* Subject-wise ROI mean extraction
* CSV export
* Results preview inside the GUI
* Progress and status updates during processing

---

## Workflow

```text
Preprocessed PET SUV images
        +
Atlas in MNI space
        +
Optional gray matter mask
        ↓
ROI extraction using MATLAB/SPM12
        ↓
Subject-by-ROI CSV output
```

---

## Input Requirements

### PET Images

PET images should be:

* Preprocessed
* Normalized to MNI space
* In NIfTI or Analyze format (`.nii` or `.img`)
* Named consistently, for example:

```text
subject_1.nii
subject_2.nii
subject_3.nii
```

The toolbox is designed for PET SUV images that have already gone through preprocessing steps such as realignment, coregistration, normalization, and smoothing.

---

### Atlas

The atlas should be:

* In MNI space
* A numerical label atlas
* In NIfTI or Analyze format (`.nii` or `.img`)
* Structured using integer ROI labels

Example atlas label structure:

```text
ROI 0 = background
ROI 1 = region 1
ROI 2 = region 2
ROI 3 = region 3
...
```

The toolbox automatically ignores ROI label `0`, since this is usually used as the background label. If the ROI selection field is left blank, all non-zero ROI labels are automatically detected from the atlas.

---

### Optional Gray Matter Mask

A gray matter mask can be provided if the user wants ROI values extracted only from gray matter voxels.

The mask must:

* Be in the same space as the PET images and atlas
* Have matching image dimensions
* Be in NIfTI or Analyze format (`.nii` or `.img`)

If no gray matter mask is selected, the toolbox extracts ROI values directly from the PET image using only the atlas labels.

---

## Output

The toolbox generates a CSV file where:

* Rows represent subjects
* Columns represent ROIs
* Values represent the mean PET signal/SUV within each ROI

Example output table:

```text
Subject,ROI_1,ROI_2,ROI_3
subject_1,1.24,0.98,1.12
subject_2,1.31,1.04,1.18
subject_3,1.19,0.91,1.06
```

The CSV output can be used for:

* Statistical analysis
* Group comparisons
* Data visualization
* Correlation with biological or clinical variables
* Machine learning or downstream quantitative analysis

---

## Repository Structure

```text
PET-ROI-Extraction-Toolbox/
│
├── pet_roi_gui.py          # Python GUI
├── pet_roi_extract.m       # MATLAB/SPM12 ROI extraction backend
├── logo.png                # Optional toolbox logo
├── README.md
├── requirements.txt
└── images/
    └── gui_screenshot.png
```

---

## Requirements

### Software

* Python 3.9–3.12
* MATLAB
* MATLAB Engine for Python
* SPM12
* Anaconda or another Python environment manager is recommended

### Python Packages

* pandas
* Pillow
* matlabengine

Install the required Python packages using:

```bash
pip install pandas pillow matlabengine
```

If using conda:

```bash
conda install pandas pillow -y
pip install matlabengine
```

You can also install packages from a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## MATLAB/SPM12 Setup

Before running the toolbox, make sure SPM12 works inside MATLAB.

In MATLAB:

```matlab
addpath('C:\spm12')
savepath
spm
```

If the SPM12 GUI opens, the setup is working.

---

## How to Run

### Option 1: Run from Anaconda Prompt

1. Open Anaconda Prompt.

2. Activate your Python environment:

```bash
conda activate spyder_spm
```

3. Navigate to the toolbox folder:

```bash
cd "C:\Users\YourName\Documents\PET-ROI-Extraction-Toolbox"
```

4. Run the GUI:

```bash
python pet_roi_gui.py
```

### Option 2: Run from Spyder

1. Open Spyder using the same Python environment where MATLAB Engine is installed.
2. Open `pet_roi_gui.py`.
3. Run the script.

---

## How to Use the GUI

1. Click **Load PET Images** and select one or more preprocessed PET SUV images.
2. Select an atlas in MNI space.
3. Optionally select a gray matter mask.
4. Choose an output CSV path.
5. Enter ROI numbers separated by commas, or leave blank to auto-detect all atlas labels.
6. Click **Run ROI Extraction**.
7. The output table will be displayed in the preview panel and saved as a CSV file.

---

## ROI Selection

Users can choose between automatic ROI detection and manual ROI selection.

### Auto-detect all ROIs

Leave the ROI field blank.

The toolbox will automatically detect all non-zero ROI labels from the atlas.

### Select specific ROIs

Enter ROI numbers separated by commas:

```text
1,2,3,4,5
```

Only the selected ROIs will be extracted.

---

## Example Use Case

This toolbox can be used to extract regional PET SUV values from preprocessed brain PET images using atlases such as:

* AAL atlas
* Harvard-Oxford atlas
* Custom MNI-space brain atlases

The resulting ROI table can be used for statistical analysis, group comparisons, or correlation with biological and clinical variables.

---

## Important Notes

* PET images, atlas, and optional mask must be in the same space.
* PET images, atlas, and optional mask should have matching dimensions.
* The atlas must contain numerical ROI labels.
* Label `0` is treated as background and ignored.
* If SPM12 cannot read an atlas due to datatype issues, convert the atlas to an SPM-compatible NIfTI format before using it.
* Large PET/MRI datasets should not be uploaded to GitHub.
* This toolbox is intended for research use and is not a clinical diagnostic tool.

---

## Troubleshooting

### MATLAB Engine is not found

Make sure MATLAB Engine is installed in the same Python environment used by Spyder or the terminal:

```bash
pip install matlabengine
```

### SPM12 is not detected

Make sure SPM12 is added to the MATLAB path:

```matlab
addpath('C:\spm12')
savepath
```

### Atlas datatype error

Some atlases may use a NIfTI datatype that SPM12 cannot read. If this happens, convert the atlas to an SPM-compatible NIfTI format, such as `int16`.

### PET, atlas, and mask dimension mismatch

Make sure all input images are in the same space and resolution. If needed, reslice the atlas or mask to match the PET image dimensions before running ROI extraction.

---

## Technical Concepts Used

This toolbox was developed using:

* **Python GUI programming:** creates the user interface for file selection, parameter input, status updates, and result preview.
* **MATLAB Engine for Python:** connects the Python GUI to MATLAB and allows the toolbox to run SPM12 commands.
* **SPM12:** reads PET, atlas, and mask images and supports NIfTI-based neuroimaging workflows.
* **Automation:** reduces manual ROI extraction steps by processing multiple subjects through one workflow.
* **Multithreading:** keeps the GUI responsive while MATLAB/SPM12 processing runs in the background.
* **CSV export:** saves extracted ROI values in a format that can be opened in Excel, R, Python, MATLAB, or statistical software.

---

## Author

Praveen Dassanayake

---

## Acknowledgement

This toolbox was developed to support PET neuroimaging analysis workflows and improve accessibility for researchers who may not have programming experience.
