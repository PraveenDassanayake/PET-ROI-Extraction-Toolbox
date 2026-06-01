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

