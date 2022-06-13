# FIR Filter Design Using Convex Optimization and Multilabel Classification of Environmental Noise
###LDI project for ELEN90088 System Optimisation &amp; Machine Learning, Semester 1 2022

######Yuqin Qiu 928065 and Jonathan South 1042806

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
Queries about datasets should be directed to <ins>j.south@student.unimelb.edu.au</ins>.

Should you wish to run source code yourself
1. Activate your desired python environment
2. Install librariries into the environment.  `pip install -r requirements.txt` (N.B. System libraries may also need to be installed).
3. Start the notebook `jupyter notebook`
4. Explore the notebooks!

## Content Summaries
```
.
├── 01_optimization
│   ├── Optimization\ (FIR\ Filter\ Design)-Bandpass.ipynb
│   ├── Optimization\ (FIR\ Filter\ Design)-Lowpass.ipynb
│   ├── bandpass
│   └── lowpass
├── 02_machine_learning
│   ├── 01_dataset_curation.ipynb
│   ├── 02_DNN_structure.ipynb
│   ├── 03_Classical_vs_DNN.ipynb
│   ├── 04_Model_Evaluation.ipynb
│   ├── example_data
│   └── images
├── README.md
└── requirements.txt
```

### 01_optimisation/
Notebooks associated with the optimisation (filtering) task
####Optimization (FIR Filter Design)-Bandpass.ipynb
Code for designing a bandpass filter using convex optimisation.
#### Optimization (FIR Filter Design)-Lowpass.ipynb
Code for designing a lowpass filter using convex optimisation.
#### bandpass/
Contains .wav files used as sample data in the bandpass filter design
#### lowpass/
Contains .wav files used as sample data in the lowpass filter design


### 02_machine_learning/
Notebooks associated with the machine learning (classification) task. Heavy use of the `pandas`, `numpy` and `tensorflow` python libraries.
#### 01_dataset_curation.ipynb
Provides an introduction to the datasets, and tools to manipulate, listen to and explore audio files.
Also gives utilities for data augmentation, and creating balanced classes for training.
Dataframes at this stage can be pickled to disk for easy retrieval in other notebooks.
#### 02_DNN_structure.ipynb
Create the architectures for the different CNN models. Load in and generate test/train splits from selected data (usually generated in 01_dataset_curation.ipynb).
Select loss and validation metrics, fit the models, and save weights as `.hdf5` files.
#### 03_Classical_vs_DNN.ipynb
Create a Gaussian HMM single label classifier, and compare performance to a CNN model (trained on identical data).
#### 04_Model_Evaluation.ipynb
Perform "fold" like model evaluation on the models trained in `02_DNN_structure.ipynb`. 
Select evaluation metrics and plot distribution of performance across k different "folds" (sensor deployments)
#### example_data/
Directory providing sample data in the structure of the larger dataset used for training.
#### images/
Static images for used for exemplary purposes, and to hold some outputs generated in notebooks.
## Data For DNN Training
The dataset used for DNN training was too large for uploading, and is also primarily closed source.
If any additional data is required to run the code, or if there are any questions, please feel free 
send email to <ins>j.south@student.unimelb.edu.au</ins> for further information.
