# GenoMLizer


# Desciption
A machine learning pipeline for prioritizing variants as genetic modifiers of rare disorders.

The goal of GenoMLizer is to help identify and prioritize genomic variants associated with disesase, specifically genetic modifiers of rare disorder.

GenoMLizer takes in variant data from whole genome or exome squencing in a VCF file and performs feature selection using several available techniques that are optimizable to each analysis, and then assesses the variant's (feature's) ability to predict disease/symptome/phenotype status by fitting several machine learning models. The output of GenoMLizer includes predictive performance metrics for each model tested, along with a permutation-based variable importance assessment for each model's variables. The GenoMLizer pipeline creates and formats two allele features (one for each allele) and two CADD features (using the CADD score of the variant) per variant to construct the initial dataset that then goes through a robust and reproducible protocol with an 80/20 training and test set split, feature selection and transformations, machine learning model hyperparameter tuning and model selection with 10-fold cross validation, and final testing of models on a true held-out test set. GenoMLizer can perform a variant assessment by utilzing the variant variables for model fitting or a gene assesment by binning the variant variables into gene regions and utilizing the gene variables for model fitting. Feature selection can be performed on either variant or gene variables. 

Available feature selection algorithms
* CMI - Conditional Mutual Information Maximization Filtering
* GLM - Logistic Regression Filtering
* DTVI - Decision Tree Variable Importance Filtering

Available machine learning models
* Decision Tree (DT)
* Random Forest (RF)
* Extreme Gradient Boosted Tree model (XGBTree)
* Lasso
* Elastic Net (EN)
* Logistic Regression (Log Reg)
* Naïve Bayes (NB)
* Support Vector Machine with Linear kernel function (SVM-L)
* Support Vector Machine with Polynomial kernel function (SVM-P)
* Support Vector Machine with Radial Basis kernel function (SVM-RB)

More details on GenoMLizer and its performance on a Turner syndrome dataset assessing genetics modifier for the development of a bicuspid aortic valve can be found in the following paper. If you use GenoMLizer in your publication, please cite the following paper.
```

Pietan, Lucas, Authors, Brian J Smith, Benjamin Darbro, Terry Braun, and Thomas Casavant. “GenoMLizer: Genome-wide Machine Learning Analysis for Genetic Modifiers.” Manuscript in Preparation for the journal Genome Research.

```


Initial establishment of the anlysis GenoMLizer was constructed from and its performance on a COVID-19 dataset assessing genetics modifier for the loss of smell and/or taste symptoms can be found at the following paper
```

Pietan, Lucas, Elizabeth Phillippi, Marcelo Melo, Hatem El-Shanti, Brian J Smith, Benjamin Darbro, Terry Braun, and Thomas Casavant. “Genome-wide Machine Learning Analysis of Anosmia and Ageusia in COVID-19.” Manuscript in Preparation for the journal Bioinformatics.

```


# Getting Started

## Installation

Installation of GenoMLizer and its dependencies can be done with the following commands. Bcftools is a requirement. The following script will check for installation, but not install. BCFtools will need to be installed manually, if needed. 
```

# Current setup and examples files
git clone https://github.com/lpietan/GenoMLizerSetup.git

cd GenoMLizerSetup

# Run install script
bash install.sh

```
If the above command do not intall or GenoMLizer is not functioning propperly, check the following requirments. They may need to be updated or installed manually depending on your system. 
```

pandas>=1.5.0    
numpy>=1.21.5
vcf_parser
psutil

```


-requirements
  -mention if install does not work will have to meet requirements another way such as virtual environment with conda
-bcftools
-vep process with example 


 ## Usage

- datsetCreator - add specifics about allele and cadd variables
-commands and args and descriptions 
-specific output files

 ## Tutorial

 -used pipelines from paper
 
