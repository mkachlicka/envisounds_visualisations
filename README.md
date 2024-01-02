# EnviSounds dataset visualisations
Vairous Streamlit apps exploring the contents of EnviSounds dataset (in preparation)

## Within-category plots

Launch the app:
https://envisoundsvisualisations-within-category.streamlit.app/

Select the category to preview from the dropdown menu

Available plots:
- Similarity matrices - show similiariy for all 10 items within each class rated by human participants via pairwise similarity task
- MDS representations - derived from similarity data; available as 2D, 3D and rotable 3D plot
- Goodness of category - show average ratings (with arror bars) of human participants of how good exemplar of each category a given sounds is

### Notes
3D rotable plot requires WebGL enabled on your browser. To check if it works go to: https://get.webgl.org/ you should see a spinning cube there. If you don't, you might need to enable WebGL.

#### Chrome
WebGL should be enabled in recent versions of Chrome. If you aren’t able to run WebGL in Chrome, make sure that you update to the most recent version of Chrome.

If you are using the most recent version of Chrome and can’t access WebGL content, make sure that hardware acceleration is enabled in your Chrome settings.

Go to chrome://settings in your address bar, or select the Chrome menu in the upper-right corner of your browser window and select Settings.

Use the search bar to locate the hardware acceleration setting, or scroll to the bottom of the Settings page, select Advanced and look in the System section.

Toggle Use hardware acceleration when available to on (the toggle is blue when hardware acceleration is on, and white when hardware acceleration is off).

The Chrome System settings. Next to "Use hardware acceleration when available" the switch is toggled to the On position.
Select the Relaunch button to restart Chrome.

After Chrome opens again, go to chrome://gpu and check that the words Hardware accelerated appear next to WebGL and WebGL2 in the Graphics Feature Status heading.

If, instead of "Hardware accelerated," you see "Software only, hardware acceleration unavailable," Chrome has automatically disabled WebGL because of a potential stability issue.

## Audio file visualisations

Launch the app:
https://envisoundsvisualisations-audiofile-visualisation.streamlit.app/

Select the audio file you want to preview
- For now you need to select a file stored on your local machine
- For now only visualisation of a single file are available

Available plots:
- Waveform
- Spectrogram

Available acoustic features:
- Amplitude envelope
- Frequency spectrum

Both features need refinement (envelope too detailed, spectrum range too wide); there will be more features to preview for single file

## Requirements

Listed in the attached requirements.txt file