import h5py
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt


# Data loader
def data_loader(filename: str):
    # Load data from HDF5 file
    file = h5py.File(filename, 'r')
    mass_axis = np.array(file['FullSpectra']['MassAxis'])
    sum_spectr = np.array(file['FullSpectra']['SumSpectrum'])
    # Combine mass axis and sum spectrum into a DataFrame
    plot_data = np.c_[mass_axis, sum_spectr]
    plot_data_df = pd.DataFrame(plot_data).rename(columns={0: 'm_z', 1: 'SumSpectr'})

    return plot_data_df


# Data selector
def select_data(data_sliced, min_r=10, max_r=100):
    # Adjust min and max values for sliced data
    min_r = min_r - 0.5
    max_r = max_r + 0.5
    # Filter data within the specified m/z range
    data_sliced = data_sliced[(min_r <= data_sliced['m_z']) & (data_sliced['m_z'] < max_r)].reset_index(drop=True)

    return data_sliced


# Peak finder
def peak_finder(data_peaks, height=1e4):
    # Find peaks with scipy.find_peaks
    peaks_ids, _ = find_peaks(x=data_peaks['SumSpectr'], height=height)

    return peaks_ids


# plotter
def plot_image(data_for_plot, peaks_ids):
    # Create a plot with interactive height limit slider
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(data_for_plot['m_z'], data_for_plot['SumSpectr'])
    ax.plot(data_for_plot['m_z'][peaks_ids], data_for_plot['SumSpectr'][peaks_ids], 'x')
    ax.axhline(y=1e4, linestyle='dashed', color='grey')

    ax.set_title('m/z - SumSpectrum plot')
    # Adjust layout and add slider for height limit
    plt.subplots_adjust(bottom=0.25)
    ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05])

    # Update plot based on the selected height limit
    def update_plot(height_limit):
        peaks_upd = peak_finder(data_peaks=data_for_plot, height=height_limit)

        ax.clear()
        ax.plot(data_for_plot['m_z'], data_for_plot['SumSpectr'])
        ax.plot(data_for_plot['m_z'][peaks_upd], data_for_plot['SumSpectr'][peaks_upd], 'x')
        ax.axhline(y=height_limit, linestyle='dashed', color='grey')
        ax.set_title('m/z - SumSpectrum plot')
        plt.draw()

    # Add slider and call to update_plot
    slider = Slider(ax_slider, 'Height limit', valmin=0, valmax=2e7, valinit=0, valstep=10)
    slider.on_changed(update_plot)
    # Display the plot
    plt.show()


# Get user input for mass range
range_min, range_max = input('Type unit mass in the format: "x:y" (in range 1-960): ').split(':')
range_min, range_max = int(range_min), int(range_max)

# Load data and perform initial processing
data = data_loader('ExampleData.h5')
data_slice = select_data(data_sliced=data, min_r=range_min, max_r=range_max)
peaks = peak_finder(data_peaks=data_slice)

# Plot the data with interactive slider
plot_image(data_for_plot=data_slice, peaks_ids=peaks)
