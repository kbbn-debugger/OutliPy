# OutliPy
OutliPy is a lightweight, object-oriented Python library built on top of Pandas and NumPy for detecting and handling outliers in tabular data.

# Key Features
1. Pandas Accessor: Use the fluent df.outli.<method> API for detection and handling.

2. Robust Validation: Intelligent column validation and clear, custom error messages (e.g., missing columns, zero-variance data).

3. Outlier Detection:  Users can easily switch between methods or customize detection sensitivity. Automatically detect outliers using multiple statistical methods such as
    - Interquartile Range (IQR)
    - Z-score
    - Percentile thresholds
    - Modified Absolute Deviation

4. Outlier Handling: Choose how to deal with detected outliers:
    - Remove outliers from your dataset
    - Cap or replace them with defined limits or mean/median values
    - grouped handling

# Where to find it? and Installation

The Github Repository is found here: https://github.com/kbbn-debugger/OutliPy

### Installation

```bash
pip install outlipy

# Dependencies

**Pandas** - The main structure of this library.

**Numpy** - Heavily relies on computation.

# License

BSD 3

# Documentation

[Under construction]