# Peaks detection from data (mass spectrum)

This script is designed for peak detection in mass spectrometry data.

What this script does:

1. Loads data from a file (HDF5 format, see example "ExampleData.h5").
2. Selects a slice (m/z range) of the spectrum.
3. Performs peak detection on the selected slice (using the find_peaks function from scipy.signal).
4. Visualizes the results (using matplotlib.widgets and matplotlib.pyplot).

Additional notes:

- Example data consists of 415,600 data points in the mass-to-charge (m/z) range of 0 to 961.