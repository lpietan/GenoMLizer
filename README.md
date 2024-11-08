# GenoMLizer


# Desciption
A machine learning pipeline for prioritizing variants as genetic modifiers of rare disorders.

The goal of GenoMLizer is to help identify and prioritize genomic variants associated with disesase, specifically genetic modifiers of rare disorder.

GenoMLizer takes in variant data from whole genome or exome squencing in a VCF file and performs feature selection using several available techniques that are optimizable to each analysis, and then assesses the variants (features) ability to predict disease/symptome/phenotype status by fitting several machine learning models. The output of GenoMLizer includes predictive performance metrics for each model tested, along with a permutation-based variable importance assessment for each model's variables. GenoMLizer can perform a variant assessment by utilzing the variant variables for model fitting or a gene assesment by binning the variant variables into gene regions and utilizing the gene variables for model fitting. Feature selection can be performed on either variant or gene variables. 

dataset creation with robust and reproducible ml analysis 
dataset split 
model hyperparameter tuning with 10-fold cv


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



used pipelines from paper

publications

# Getting Started

## Installation

-install procedure
-requirements
  -mention if install does not work will have to meet requirements another way such as virtual environment with conda
-bcftools
-vep process with example 


 ## Usage
-commands and args and descriptions 
-specific output files

 ## Tutorial
 
