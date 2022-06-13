# FIR Filter Design Using Convex Optimization and Multilabel Classification of Environmental Noise
LDI project for ELEN90088 System Optimisation &amp; Machine Learning, Semester 1 2022

This repository contains a number of jupyter notebooks associated with the exploration, problem formulation and solution implementation related to 
the chosen topic.  

#### Abstract
    We explore the problem of classification of urban environmental noise sources, using a number of optimisation 
    techniques, modern and classical machine learning methods. The project is contextualised by considering sensor data 
    gathered by a network of IoT style noise monitors, deployed in various urban environments. 
    The noise monitors measure a variety of noise sources, such as road traffic, wildlife, machinery and aircraft noise, 
    under a variety of conditions affecting the quality of data. 
    Applicable techniques will be compared and contrasted at data pre-processing and classification stages of a noise analysis 
    pipeline, with the broad goal of designing a robust implementation for classifying common environmental noise sources.
    
## Setup
As some datasets used are large, or closed source, certain files may not be available at runtime for the markers. 
Static images, summaries and results are provided where appropriate, along with saved notebook outputs.

Should you wish to run source code yourself
1. Activate your desired python environment
2. Install librariries into the environment.  `pip install -r requirements.txt`
3. Start the notebook `jupyter notebook`
4. Explore the notebooks!

## Content Summaries
### 01_optimisation/
#### bandpass
folder that stores sample data for bandpass filter design
#### lowpass
folder that stores sample data for lowpass filter design
#### Optimization (FIR Filter Design)-Lowpass.ipynb
Code for lowpass filter design
#### Optimization (FIR Filter Design)-Bandpass.ipynb
Code for bandpass filter design

### 02_machine_learning/
#### 01_dataset_curation.ipynb
Provides an introduction to the datasets, and tools to manipulate and explore.
#### 02_DNN_structure.ipynb
Different types of DNN models, also code for training
#### 03_Classical_vs_DNN.ipynb
Comparison between Classical ML method and DNN peroformance
#### 04_Model_Evaluation.ipynb
Evaluating the performance of the trained DNN model

## Data For DNN training
The dataset for training was too large for uploading, therefore if dataset is need to run the code
please feel free tosend email to <ins>jsouth@student.unimelb.edu.au</ins> to request sample dataset for training the DNN above
