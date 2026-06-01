# PET ROI Extraction Toolbox

A user-friendly Python GUI toolbox integrated with MATLAB SPM12 for atlas-based ROI extraction from preprocessed PET SUV brain images.

This toolbox allows users to load multiple PET images, apply a brain atlas in MNI space, optionally apply a gray matter mask, and extract mean PET values for each ROI. The output is saved as a subject-by-ROI CSV table.

---

## Overview

Quantitative PET brain analysis often requires extracting regional values from anatomical or functional brain atlases. This process can be repetitive, time-consuming, and prone to manual errors when performed subject-by-subject.

The PET ROI Extraction Toolbox simplifies this process by providing a graphical interface where users can:

- Load multiple preprocessed PET SUV images
- Load a brain atlas in MNI space
- Optionally load a gray matter mask
- Select specific ROI numbers or auto-detect all atlas labels
- Extract mean PET values per ROI
- Export results as a CSV table
- Preview results inside the GUI

---

## Features

- Python-based graphical user interface
- MATLAB SPM12 backend for NIfTI image handling
- Multiple-subject PET image loading
- Custom atlas support
- Automatic ROI label detection from atlas
- Optional gray matter mask application
- Manual ROI selection using comma-separated labels
- Subject-wise ROI mean extraction
- CSV export
- Results preview inside the GUI
- Progress/status updates during processing

---

## Workflow

The toolbox follows this general workflow:

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
* Contain integer ROI labels

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

The CSV output can be used for further statistical analysis, group comparisons, visualization, or correlation with biological and clinical variables.

## Files

PET-ROI-Extraction-Toolbox/
│
├── pet_roi_gui.py          # Python GUI
├── pet_roi_extract.m       # MATLAB/SPM12 ROI extraction backend
├── logo.png                # Optional toolbox logo
├── README.md
├── requirements.txt
└── images/
    └── gui_screenshot.png

## Requirements

Python 3.9–3.12
MATLAB
MATLAB Engine for Python
SPM12
Anaconda or another Python environment manager is recommended
Python Packages
pandas
Pillow
matlabengine

Before running the toolbox, make sure SPM12 works inside MATLAB.

In MATLAB:

addpath('C:\spm12')
savepath
spm

If the SPM12 GUI opens, the setup is working.

How to Run
Open Anaconda Prompt.
Activate your Python environment:
conda activate spyder_spm
Navigate to the toolbox folder:
cd "C:\Users\YourName\Documents\PET-ROI-Extraction-Toolbox"
Run the GUI:
python pet_roi_gui.py

Alternatively, open pet_roi_gui.py in Spyder and run the script.

How to Use the GUI
Click Load PET Images and select one or more preprocessed PET SUV images.
Select an atlas in MNI space.
Optionally select a gray matter mask.
Choose an output CSV path.
Enter ROI numbers separated by commas, or leave blank to auto-detect all atlas labels.
Click Run ROI Extraction.
The output table will be displayed in the preview panel and saved as a CSV file.
ROI Selection

Users can either:

Auto-detect all ROIs

Leave the ROI field blank.

The toolbox will automatically detect all non-zero ROI labels from the atlas.

Select specific ROIs

Enter ROI numbers separated by commas:

1,2,3,4,5

## Important Notes

PET images, atlas, and optional mask must be in the same space.
The atlas must contain numerical ROI labels.
Label 0 is treated as background and ignored.
If SPM12 cannot read an atlas due to datatype issues, convert the atlas to an SPM-compatible NIfTI format before using it.
Large PET/MRI datasets should not be uploaded to GitHub.
Example Use Case

This toolbox can be used to extract regional PET SUV values from preprocessed brain PET images using atlases such as:

AAL atlas
Harvard-Oxford atlas
Custom MNI-space brain atlases

The resulting ROI table can be used for statistical analysis, group comparisons, or correlation with biological/clinical variables.

## Technical Concepts Used

This toolbox was developed using:

Python GUI programming: for the user interface
MATLAB Engine for Python: to connect Python with MATLAB/SPM12
SPM12: for NIfTI image loading and processing
Automation: to reduce manual ROI extraction steps
Multithreading: to keep the GUI responsive during long processing tasks
CSV export: for easy downstream analysis

## Author

Praveen Dassanayake

## Acknowledgement

This toolbox was developed to support PET neuroimaging analysis workflows and improve accessibility for researchers who may not have programming experience.
