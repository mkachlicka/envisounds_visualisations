#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 10:19:33 2023

@author: mkachlicka
"""
# Load packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#from PIL import Image # for image control, activate when adding logo/banner
#from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold

# Title page
st.set_page_config(layout="wide", page_title="EnviSounds Dataset")
#image = Image.open('templogo.jpg')
#st.image(image, use_column_width=True)
st.write("""
# EnviSounds Dataset

***
""")

##################
### Similarity ###
##################

st.subheader('Similarity Matrices')

rng = range(0, 11) # Set range so it's the same for all plots

sim_all = pd.read_csv("data/similarity_data_averaged.csv")

# Add dropdown for category selection
cat_options = sorted(sim_all["category"].unique())
selected_cat = st.selectbox("Select a category", cat_options)

temp = sim_all[sim_all["category"]==selected_cat]

# Reshape DataFrame for plotting
temp_pivot = temp.pivot(index="sound1", columns="sound2", values="response")

plt.figure(figsize=(8,8))
#ax = sns.heatmap(data=temp_pivot, annot=True, cmap=sns.diverging_palette(240, 10, as_cmap=True), square=True)
ax = sns.heatmap(data=temp_pivot, annot=True, cmap="Spectral_r", square=True)
ax.set_xlabel("Sound 1")
ax.set_ylabel("Sound 2")
ax.set_title(selected_cat)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_ylim(ax.get_ylim()[::-1]) # flip y-axis

cbar = ax.collections[0].colorbar
cbar.set_ticks(np.linspace(rng[0], rng[-1], num=11))
cbar.set_ticklabels(np.linspace(rng[0], rng[-1], num=11))
cbar.ax.set_ylabel("Response", rotation=-90, va="bottom")

st.pyplot(plt) # show plot in Streamlit

###########
### MDS ###
###########

st.subheader('MDS Representations')

# Load similarity rating data
similarity_data = pd.read_csv("data/similarity_data.csv")

# Add dropdown for category selection
cat_options = sorted(similarity_data["category"].unique())
#selected_cat = st.selectbox("Select a category", cat_options)

# Filter data by selected category
similarity_data = similarity_data[similarity_data["category"] == selected_cat]

# Compute mean response for each sound pair
#similarity_data = similarity_data.groupby(["sound1", "sound2"]).mean().reset_index()
similarity_data = similarity_data.groupby(["sound1", "sound2"]).agg({'response': 'mean'}).reset_index()


# Create a dictionary that maps each sound to an integer
sound_to_int = {sound: i for i, sound in enumerate(similarity_data["sound1"].unique())}

# Compute dissimilarity matrix
n_sounds = len(sound_to_int)
dissimilarity_matrix = np.zeros((n_sounds, n_sounds))
for _, row in similarity_data.iterrows():
    i = sound_to_int[row["sound1"]]
    j = sound_to_int[row["sound2"]]
    dissimilarity_matrix[i, j] = 1 - row["response"]
    dissimilarity_matrix[j, i] = 1 - row["response"]

# Perform MDS in 2D and 3D
mds_seed = 123
mds_2d = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=mds_seed)
mds_3d = manifold.MDS(n_components=3, dissimilarity="precomputed", random_state=mds_seed)
coordinates_2d = mds_2d.fit_transform(dissimilarity_matrix)
coordinates_3d = mds_3d.fit_transform(dissimilarity_matrix)

# Plot MDS in 2D
plt.figure(figsize=(8, 8))
plt.scatter(coordinates_2d[:, 0], coordinates_2d[:, 1])
plt.scatter(np.mean(coordinates_2d[:, 0]), np.mean(coordinates_2d[:, 1]), marker='*', s=200, color='red')
for i, label in enumerate(sound_to_int.keys()):
    plt.annotate(label, (coordinates_2d[i, 0], coordinates_2d[i, 1]))
plt.axis("equal")
plt.title(f"MDS Plot in 2D for {selected_cat}")
st.pyplot(plt) # show plot in Streamlit

# Plot MDS in 3D
figstat = plt.figure(figsize=(8, 8))
ax = figstat.add_subplot(111, projection="3d")
ax.scatter(coordinates_3d[:, 0], coordinates_3d[:, 1], coordinates_3d[:, 2])
ax.scatter(np.mean(coordinates_3d[:, 0]), np.mean(coordinates_3d[:, 1]), np.mean(coordinates_3d[:, 2]), marker='*', s=200, color='red')
for i, label in enumerate(sound_to_int.keys()):
    ax.text(coordinates_3d[i, 0], coordinates_3d[i, 1], coordinates_3d[i, 2], label)
ax.set_title(f"MDS Plot in 3D for {selected_cat}")
st.pyplot(figstat) # show plot in Streamlit


# Using Plotly for rotating MDS
import plotly.graph_objs as go

# Convert sound_to_int keys to string
sound_labels = [list(sound_to_int.keys())[i] for i in range(len(sound_to_int.keys()))]

# Create trace for 3D scatter plot
trace = go.Scatter3d(
    x=coordinates_3d[:, 0],
    y=coordinates_3d[:, 1],
    z=coordinates_3d[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=list(sound_to_int.values()),
        colorscale='Viridis',
        opacity=0.8,
        symbol='circle'
    ),
    text=sound_labels
)


# Create layout for 3D scatter plot
layout = go.Layout(
    title="Rotating MDS Plot in 3D",
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    ),
    width=800,
    height=800
)

# Create figure object and add trace and layout to it
fig = go.Figure(data=[trace], layout=layout)

# Display the figure
st.plotly_chart(fig)

################
### Goodness ###
################

st.subheader('Goodness of Category')

# Load data
good_summary = pd.read_csv("data/goodness_data.csv")

# Add dropdown for category selection
cat_options = sorted(good_summary["category"].unique())
#selected_cat = st.selectbox("Select a category", cat_options)

# Filter data by selected category and calculate mean and standard error of response
temp = good_summary[good_summary["category"] == selected_cat]
temp = temp.groupby("sound1")["response"].agg(["mean", "sem"]).reset_index()

# Create bar plot with error bars
plt.figure(figsize=(8, 8))
plt.bar(temp["sound1"], temp["mean"], yerr=temp["sem"], color="darkslateblue", capsize=4)
plt.ylim(0, 10)
plt.xlabel("Sound")
plt.ylabel("Average rating")
plt.title(selected_cat)
plt.xticks(range(1, 11)) # set x axis to show all numbers from 1 to 10
plt.gca().set_aspect('equal', adjustable='box')
plt.style.use('classic')
st.pyplot(plt) # show plot in Streamlit



