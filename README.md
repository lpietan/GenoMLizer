# GenoMLizer


# Desciption
A machine learning (ML) pipeline for prioritizing variants as genetic modifiers of rare disorders.

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

Pietan, Lucas, Authors, Brian J Smith, Benjamin Darbro, Terry Braun, and Thomas Casavant. “GenoMLizer: Genome-wide Machine Learning Analysis for Genetic Modifiers.” Manuscript submitted to the journal Genome Research.

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
With the install, example files will be downloaded to test the installation. These files are used in the [Tutorial](#tutorial) below. If the above commands do not intall or GenoMLizer is not functioning propperly, check the following requirments. They may need to be updated or installed manually depending on your system. 
```
   
Python >= 3.9
R ≥ 4.1.0
BCFtools

# Python Requirements
pandas>=1.5.0
numpy>=1.21.5
vcf_parser
psutil

# R Requirments
MachineShop
praznik
doSNOW
dplyr
readr
e1071
tree
randomForest
xgboost

```
Please refer to each package documentation for installation directions and individual requirements. Installation of R packages can be done with the following code. 
```R

# Example of R package installation
install.packages("MachineShop")
# Check installation and load package
library(MachineShop)

```
Installation of Python requirments in a virtual environment using conda is an option and can be done with the following code. BCFtools can also be installed with conda, if not already installed. 
```Python

# Create conda environment with requirements
conda create -n genomlizer_env python=3.9 r-base=4.1.0 numpy=1.21.5 pandas=1.5.0
# Activate environment
conda activate genomlizer_env
# Example install of bcftools with conda
conda install -c bioconda bcftools

```


 ## Usage

GenoMLizer takes in a joint called or merged VCF file with all samples and genotypes in the same file and requires the variants to be annotated with Ensembl's `VEP` (Variant Effect Predictor). The VCF file needs only one annotation per variant and to have a variant annotation for gene symbol and for the varaint's CADD score. This can be accomplished with the following command.
```

# Example VEP command
vep \
--assembly GRCh38 \
--cache \
--merged \
--plugin \
CADD,whole_genome_SNVs.tsv.gz,InDels.tsv.gz \
--pick_allele \
--symbol \
--vcf \
--fasta /homo_sapiens_merged/Homo_sapiens.GRCh38.dna.toplevel.fa.gz \
-i input.vcf.gz \
-o out.vcf.gz \
-offline

```

The input VCF file should be filtered to variants with only one alternative allele. This can be done with following command using `BCFtools`. For additional options for file setup and preparation see the [Advanced Setup](#advanced-setup) section. 
```

bcftools view -e 'N_ALT>1' -O z -o output.vcf.gz input.vcf.gz

```

The GenoMLizer has the following commands that can be ran from the command line. 
```

# Initial Commands     
datasetCreator          
splitTrainTest

# Feature Selection
CMI
GLM
DTVI

# Gene Variable Transformation
geneTransform

# Test Set Prep
varPrep
genePrep

# Model fitting, testing, and Variable Importance
mlVar
mlGene

```

#### datasetCreator
Transforms variants from the VCF file to usable ML features. Four variables are created from each variant. Two allele variables, one for each allele, encoded as a 0 for the reference allele and 1 for the alternative alelle. And two CADD variables, one for each allele, utilizing the CADD score for the variant for encoding the alternative allele and 0 for the reference allele. datasetCreator has 3 agruments (order matters).
```

datasetCreator input.vcf.gz target_file output.csv

   input.vcf.gz   -    preprocessed VCF file
   target_file    -    a file containing the names of the samples and corresponing phenotype data encoded as 0/1
   output.csv     -    the name of the output CSV file with the samples and transformed features

```
Structure of the `target_file`. The heading must be, `sampleNames,Targets`.
```
sampleNames,Targets
S1,1
S2,0
S3,0
S4,1
S5,1
```

#### splitTrainTest
Intended to be used after datasetCreator, splitTrainTest performs an 80/20 random split of the dataset. 80% of the samples for the training set and 20% for a true held-out test set. On the training set, ML house keeping corrections and filtering are performed. Variables are corrected for variant no calls (NC, '.' genotyopes in the VCF file) and variables are filtered for zero variance.
```

splitTrainTest input.csv NC_correction_threshold seed

   input.csv                    -      input CSV file, output from datasetCreator
   NC_correction_threshold      -      No call threshold, numeric value between 0 and 1 (Recommended value 0.8). Setting 0.8 would allow variables with a no call in 80% or more of the samples are filtered out. No calls of less than 80% are transformed to a '0' 
   seed                         -      

```


#### CMI


#### GLM


#### DTVI


#### geneTransform


#### varPrep


#### genePrep


#### mlVar


#### mlGene



-commands and args and descriptions 
-specific output files

 ## Tutorial

 -used pipelines from paper


 ## Advanced Setup 

 - dataset creator can handle up 9 alt allele
 - DTVI and ML fitting in ML script need 0/1 encoding for allele variables if selecting factor
 - can perform a custom transformation of variables to 0/1
 
