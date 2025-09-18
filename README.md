# metadata-viewer
Visual Studio Code extension for cryo-electron microscopy `.star` and `.pkl` metadata viewing. Completed Fall 2025 at Princeton University.

## Features
Supports the following file formats and data structures:
- **`.star`**: Displays tables of the first and last 50 rows for each array in a `.star` file using the [`starfile`](https://github.com/teamtomo/starfile) package.
- **`.pkl`**: Displays contents of 1D–3D NumPy arrays, 1D–2D Pandas DataFrames, lists, tuples, and scalar values (e.g., strings, floats).

## Installation
1. Install the Metadata Viewer extension via `Extensions (Window)` > `Install from VSIX` using the included `metadata-viewer-0.0.1.vsix` file.
2. Ensure Python is installed on your machine; the extension requires a Python interpreter to function.
3. Install the required Python dependencies locally with `pip install starfile numpy pandas`.