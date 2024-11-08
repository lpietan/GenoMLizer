# GenoMLizer
================

# Desciption
A machine learning pipeline for prioritizing variants as genetic modifiers of rare disorders.

The goal of GenoMLizer is to help identify and prioritize genomic variants associated with disesase, specifically genetic modifiers of rare disorder.

GenoMLizer takes in variant data from whole genome or exome squencing in a VCF file and performs feature selection using several available techniques, optimized to each analysis, and then assess the variants (features) ability to predict disease/symptome/phenotype status by fitting several machine learning models. The output of GenoMLizer are the predictive performance metrics of each model tested and a permutation-based variable importance assessment of the variables with each model. 

