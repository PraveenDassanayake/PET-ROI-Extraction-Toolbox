# PET ROI Extraction Toolbox (SPM12)

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
