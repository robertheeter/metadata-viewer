# metadata-viewer
Visual Studio Code extension for cryo-electron microscopy `.star` and `.pkl` metadata viewing. Completed Fall 2025 at Princeton University.

## Features
Supports the following file formats and data structures:
- **`.star`**: Displays tables for each array in a `.star` file using the [`starfile`](https://github.com/teamtomo/starfile) package.
- **`.pkl`**: Displays contents of 1D–3D NumPy arrays, 1D–2D Pandas DataFrames, lists, tuples, and scalar values (e.g., strings, floats). This extension also automatically formats the `ctf.pkl` and `pose.pkl` files that are used in data processing with the [`cryodrgn`](https://github.com/ml-struct-bio/cryodrgn) package.

Tabular data is truncated to the first and last 50 rows and/or columns. Lists are truncated to the first and last 5 elements. CryoDRGN CTF and pose `.pkl` files are assumed from their file format and file name.

## Installation
1. Install the Metadata Viewer extension via `Extensions (Window)` > `Install from VSIX` using the included `metadata-viewer-0.0.1.vsix` file.
2. Ensure Python is installed on your machine; the extension requires a Python interpreter to function.
3. Install the required Python dependencies globally (i.e., outside of a virtual environemnt) with `pip install starfile numpy pandas`.

## Usage
There are two options for viewing files with this extension:
- Right click on a `.pkl` or `.star` file and select `Metadata Viewer: View PKL File` or `Metadata Viewer: View STAR File`.
- Run the extension using the Command Palette (`Cmd + Shift + P` or `Ctrl + Shift + P`) > `Metadata Viewer: View PKL File` or `Metadata Viewer: View STAR File` and enter the file path.