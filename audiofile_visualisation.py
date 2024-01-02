#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Feb 19 18:27:21 2023

@author: mkachlicka
"""

import streamlit as st
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import hilbert, chirp
import matplotlib.pyplot as plt

# Load the wav file from the "sample" folder in the sidebar
st.sidebar.title("Select a WAV file")
file_path = st.sidebar.file_uploader("", type=["wav"])

if file_path is not None:
    # Read the WAV file and get the sample rate
    sample_rate, samples = wav.read(file_path)

    # Define acoustic features as a list of check boxes
    st.sidebar.title("Select acoustic features")
    features = ["Envelope", "Frequency"]
    feature_selection = st.sidebar.multiselect("", features)
    
    # Define a function to calculate the envelope of the signal
    def envelope(signal):
        analytic_signal = hilbert(signal)
        amplitude_envelope = np.abs(analytic_signal)
        return amplitude_envelope
    
    # Define a function to calculate the frequency of the signal
    def frequency(signal):
        time_array = np.arange(0, len(signal)) / sample_rate
        frequencies = np.fft.fftfreq(signal.size, time_array[1] - time_array[0])
        fft = np.fft.fft(signal)
        spectrum = np.abs(fft)
        return frequencies, spectrum
    
    # Display the waveform, spectrogram, and play button in the main window
    st.title("Selected Sound")
    col1, col2 = st.columns(2)
    col1.write("Waveform")
    col1.line_chart(samples)
    with col2:
        st.write("Spectrogram")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.specgram(samples, Fs=sample_rate)
        st.pyplot(fig, clear_figure=True)
    st.audio(samples, format="audio/wav", sample_rate=sample_rate)

    
    # Display the selected features below the main window
    if "Envelope" in feature_selection:
        st.title("Sound Envelope")
        envelope_data = envelope(samples)
        fig, ax = plt.subplots()
        ax.plot(envelope_data)
        st.pyplot(fig)
    
    if "Frequency" in feature_selection:
        st.title("Frequency Plot")
        freq_data, spec_data = frequency(samples)
        fig, ax = plt.subplots()
        ax.plot(freq_data, spec_data)
        st.pyplot(fig)



