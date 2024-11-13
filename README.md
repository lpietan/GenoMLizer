# GenoMLizer


# Desciption
A machine learning (ML) pipeline for prioritizing variants as genetic modifiers of rare disorders.

The goal of GenoMLizer is to help identify and prioritize genomic variants associated with disease, specifically genetic modifiers of rare disorders.

GenoMLizer accepts variant data from whole genome or exome sequencing in a VCF file, performs feature selection with several available techniques that are optimizable to each analysis, and then evaluates the variants' (features') predictive ability for disease/symptom/phenotype status by fitting multiple machine learning models. The output of GenoMLizer includes predictive performance metrics for each model tested, along with a permutation-based variable importance assessment for each model's variables. The GenoMLizer pipeline constructs the initial dataset by creating and formatting two allele features (one for each allele) and two CADD features (using the variant's CADD score) per variant. This dataset then undergoes a rigorous and reproducible protocol, including an 80/20 split for training and testing, feature selection and transformations, hyperparameter tuning and model selection using 10-fold cross-validation, followed by final testing on a fully held-out test set. GenoMLizer can perform a variant assessment by utilizing the variant variables for model fitting or a gene assessment by binning the variant variables into gene regions and utilizing the gene variables for model fitting. Feature selection can be performed on either variant or gene variables. 

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

More details on GenoMLizer and its performance on a Turner syndrome dataset assessing genetic modifiers for the development of a bicuspid aortic valve can be found in the following paper. If you use GenoMLizer in your publication, please cite the following paper.
```

Pietan, Lucas, Brian J Smith, Benjamin Darbro, Terry Braun, and Thomas Casavant. “GenoMLizer: Genome-wide Machine Learning Analysis for Genetic Modifiers.” Manuscript submitted to the journal Genome Research.

```


Details on the initial development of GenoMLizer and its performance on a COVID-19 dataset assessing genetic modifiers for loss of smell and/or taste symptoms can be found in the following paper.
```

Pietan, Lucas, Elizabeth Phillippi, Marcelo Melo, Hatem El-Shanti, Brian J Smith, Benjamin Darbro, Terry Braun, and Thomas Casavant. “Genome-wide Machine Learning Analysis of Anosmia and Ageusia in COVID-19.” Manuscript in Preparation for the journal Bioinformatics.

```


# Getting Started

## Installation

Installation of GenoMLizer and most of its dependencies can be done with the following commands. `BCFtools` is a requirement, and the following script will check for its installation but will not install. `BCFtools` will need to be installed manually, if needed. 
```

# Current setup and examples files
git clone https://github.com/lpietan/GenoMLizerSetup.git

cd GenoMLizerSetup

# Run install script
bash install.sh

```
With the installation, example files will be downloaded to test the setup. These files are used in the [Tutorial](#tutorial) below. If the above commands do not install GenoMLizer correctly or it is not functioning properly, check the following requirements. They may need to be updated or installed manually depending on your system. 
```
   
Python >= 3.9
R ≥ 4.1.0
BCFtools

# Python Requirements
pandas>=1.5.0
numpy>=1.21.5
vcf_parser
psutil

# R Requirements
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
Please refer to each package's documentation for installation instructions and individual requirements. Installation of R packages can be done with the following code. 
```R

# Example of R package installation
install.packages("MachineShop")
# Check installation and load package
library(MachineShop)

```
Installation of Python requirements in a virtual environment using `Conda` is an option and can be done with the following code. `BCFtools` can also be installed with `Conda`, if not already installed. 
```Python

# Create Conda environment with requirements
conda create -n genomlizer_env python=3.9 r-base=4.1.0 numpy=1.21.5 pandas=1.5.0
# Activate environment
conda activate genomlizer_env
# Example install of BCFtools with Conda
conda install -c bioconda bcftools

```


 ## Usage

GenoMLizer accepts a jointly-called or merged VCF file with all samples and genotypes in a single file and requires the variants to be annotated with Ensembl's `VEP` (Variant Effect Predictor). The VCF file should contain only one annotation per variant and must include annotations for the gene symbol and the variant's CADD score. This can be accomplished with the following command.
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

The input VCF file should be filtered to include variants with only one alternative allele. This can be done with the following command using `BCFtools`. For additional options for file setup and preparation, see the [Advanced Setup](#advanced-setup) section. 
```

bcftools view -e 'N_ALT>1' -O z -o output.vcf.gz input.vcf.gz

```

GenoMLizer includes the following commands, which can be run from the command line. 
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
Transforms variants from the VCF file into usable ML features. Four variables are created from each variant: two allele variables, one for each allele, encoded as a 0 for the reference allele and 1 for the alternative allele, and two CADD variables, one for each allele, using the CADD score to encode the alternative allele and 0 for the reference allele. `datasetCreator` has 3 arguments (order matters).
```

datasetCreator input.vcf.gz target_file output.csv

   input.vcf.gz   -    Preprocessed VCF file
   target_file    -    A file containing the names of the samples and corresponing phenotype data encoded as 0/1
   output.csv     -    The name of the output CSV file with the samples and transformed features

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
Example of per variant output variable naming structure
```
CHR:POS:GeneSymbol:Allele1
CHR:POS:GeneSymbol:CADD1
CHR:POS:GeneSymbol:Allele2
CHR:POS:GeneSymbol:CADD2
```


#### splitTrainTest
Intended to be used after `datasetCreator`, `splitTrainTest` performs an 80/20 random split of the dataset: 80% of the samples are assigned to the training set and 20% to a true held-out test set. On the training set, ML housekeeping corrections and filtering are performed. Variables are corrected for variant no-calls (NC, '.' genotypes in the VCF file), and variables are filtered for zero variance. The output of this command is the files `input_Train.csv` and `input_Test.csv`. `splitTrainTest` has 3 arguments (order matters).
```

splitTrainTest input.csv NC_correction_threshold seed

   input.csv                    -      Input CSV file, output from datasetCreator
   NC_correction_threshold      -      Numeric value between 0 and 1 (Recommended value 0.8). No-call threshold, setting 0.8 would allow variables with a no-call in 80% or more of the samples to be filtered out. No-calls of less than 80% are transformed to a 0 (reference allele). 
   seed                         -      Integer value, set seed for reproducible split

```


#### CMI
Performs Conditional Mutual Information Maximization Filtering on variant or gene variables. It breaks the input dataset into 1,000-variable intermediate datasets and selects the variables with the highest mutual information to pass the filter. `CMI` has 5 arguments (order matters).
```

CMI input.csv output.csv k seed number_of_clusters

   input.csv               -      Input CSV file
   output.csv              -      Output CSV file 
   k                       -      Integer value, k number of variables to select from each intermediate dataset
   seed                    -      Integer value, set seed for reproducible output
   number_of_clusters      -      Integer value, number of cluster for parallelization 

```

#### GLM
Performs Logistic Regression Filtering on variant or gene variables. Performs a logistic regression with either a Chi-squared or F-test to calculate a p-value for association of the feature (predictor variable) with the target (response variable). `GLM` has 6 arguments (order matters).
```

GLM input.csv output.csv test Pvalue_threshold seed number_of_clusters

   input.csv               -      Input CSV file
   output.csv              -      Output CSV file 
   test                    -      'Chisq' or 'F' value. 'Chisq' performs a chi-squared test of association and 'F' performs an F-test.
   Pvalue_threshold        -      Numeric value between 0 and 1 (recommended value <= 0.1). P-value treshold for association test. All variables with a p-value less than or equal to threshold will pass the filter. 
   seed                    -      Integer value, set seed for reproducible output
   number_of_clusters      -      Integer value, number of cluster for parallelization 

```

#### DTVI
Decision Tree Variable Importance Filtering on variant or gene variables. It breaks the input dataset into intermediate datasets with a user-specified number of variables and fits a decision tree model. Hyperparameter tuning and model selection are performed with 10-fold cross-validation. If the accuracy of the top decision tree model is greater than or equal to a user-specified accuracy threshold, a permutation-based variable importance assessment is performed. The variables with a variable importance score greater than 0 pass the filter. `DTVI` has 8 arguments (order matters).
```

DTVI input.csv output.csv allele_factorization ACC_threshold number_of_variables number_of_iterations seed number_of_clusters

   input.csv                  -      Input CSV file
   output.csv                 -      Output CSV file 
   allele_factorization       -      Integer value of 0/1. A value of 0 encodes all allele variables as numeric. A value of 1 encodes all allele variables as factor.
   ACC_threshold              -      Numeric value between 0 and 1 (recommended value >= majority class accuracy). Accuracy threshold for decision tree model. Setting value equal to 1 will set the accuracy threshold the the majority class accuracy of the input dataset.
   number_of_variables        -      Integer value, sets the number of variables to include in the intermidiate datasets
   number_of_iterations       -      Integer value, sets the number of time to filter through the initial input dataset
   seed                       -      Integer value, set seed for reproducible output
   number_of_clusters         -      Integer value, number of cluster for parallelization    

```

#### geneTransform
Transforms variant variables into gene variables. Variants within the same gene annotations are binned. All allele variables are summed to create a gene_allele variable and all CADD variables are summed to create a gene_CADD variable. `geneTransform` has 5 arguments (order matters). If `SFC` or `DC` are selected for the `correction`, the file `variables_corrected.csv` will also be output and is needed as input for the `genePrep` command. This file can and should be renamed if multiple runs of this command are performed in the same directory. 
```

geneTransform input.csv output.csv bpRegion correction correction_threshold

   input.csv                  -      Input CSV file
   output.csv                 -      Output CSV file 
   bpRegion                   -      Integer value (recommended value 25000). This sets the bin size in base pairs for variants to be binned into regions if the variants do not have a gene symbol annotation.  
   correction                 -      'NC', 'SFC', or 'DC'. 'NC' performs no correction
                                     and transforms variant variable as they are. 'SFC'
                                     performs a sample allele frequency correction. If a variable in the training set has a greater amount of samples with alternative alleles than the correction_threshold, the 0/1 encoding of the variable is swapped (0's to 1's and 1's to 0's) before adding to the gene variable. Same action for CADD variables. 'DC' performs a directional correction. Intended to adjust for protective effects. Calculates the ratio of a variable's alternative alleles to the controls and cases. If the ratio of alternative allele to controls exceeds the correction_threshold, the 0/1 encoding of the variable is swapped (0's to 1's and 1's to 0's) before adding to the gene variable. Same action for CADD variables.
   correction_threshold       -      Numeric value between 0 and 1 (recommended value 0.5). Sets correction threshold. Optional if correction = 'NC'.

```
Example of gene transformation output variable naming structure
```
GeneSymbol_Allele
GeneSymbol_CADD
# Or for variables without gene symbol annotation binned into regions
CHR:POS_POS2_Allele
CHR:POS_POS2_CADD
```

#### varPrep
Prepares the test set file and variant variables for ML model testing with the `mlVar` command. It is intended to be used after all feature selection is performed on the training set and before the `mlVar` command. `varPrep` has 3 arguments (order matters).
```

varPrep input_Train.csv input_Test.csv output_Test.csv

   input_Train.csv         -         Training input CSV file
   input_Test.csv          -         Test input CSV file
   output_Test.csv         -         Test output CSV file


```

#### genePrep
Prepares the test set file and transforms the variant variables into gene variables for ML model testing with the command mlGene. It is intended to be used after all feature selection and transformations are performed on the training set and before the `mlGene` command. `genePrep` has 6 arguments (order matters).
```

genePrep input_Train.csv input_Test.csv output_Test.csv bpRegion correction_performed correction_file

   input_Train.csv         -         Training input CSV file
   input_Test.csv          -         Test input CSV file
   output_Test.csv         -         Test output CSV file
   bpRegion                -         Integer value. Should be the same setting used with the geneTransform command with the training set. Setting has the same meaning as with the geneTransform command. 
   correction_performed    -         Interger value, binary 0/1. 0 is no correction performed with geneTransform with the training set. 1 is there was a correction ('SFC' or 'DC') performed with geneTransform with the training set.
   correction_file         -         correction CSV file output from geneTransform (variables_corrected.csv). If the file was renamed, use the renamed file. No file needed if no correction (NC) was performed.

```

#### mlVar
Performs model fitting and testing with the ML models mentioned above for variant variables. For each model, hyperparameters are tuned and models are selected using 10-fold cross-validation. The selected models are then tested on the held-out test set. The 10-fold cross-validation estimated predictive performance (training) metrics, and the true held-out test set performance metrics are included in the output files `prefix_train_results.csv` and `prefix_test_results.csv`, respectively. The performance metrics included are brier score, accuracy, Cohen’s kappa, area under the receiver operating characteristic (ROC) curve, sensitivity, and specificity. A permutation-based variable importance assessment is done for each top model with 25 permutations. Output for the variable importance assessments is in `prefix_model_vi.csv` (full results) and `prefix_model_vi.pdf` (plot of top 40 variables) for each model. The decision tree and random forest models have the features renamed due to syntax requirements. Because of this, there are two output files `variableKeys_ML_train_dt_rf.csv` and `variableKeys_ML_test_dt_rf.csv`, which act as keys to renaming the features in the variable importance output files. `mlVar` has 6 arguments (order matters).
```

mlVar input_Train.csv input_Test.csv allele_factorization prefix seed number_of_clusters

   input_Train.csv            -         Training input CSV file
   input_Test.csv             -         Test input CSV file
   allele_factorization       -         Integer value of 0/1. A value of 0 encodes all allele variables as numeric. A value of 1 encodes all allele variables as factor.
   prefix                     -         Prefix for output files
   seed                       -         Integer value, set seed for reproducible output
   number_of_clusters         -         Integer value, number of cluster for parallelization 

```

#### mlGene
Performs the same function as `mlVar` but for gene variables. Variable key output files for the decision tree and random forest models are `variableKeys_gene_ML_train_dt_rf.csv` and `variableKeys_gene_ML_test_dt_rf.csv`.  `mlGene` has 5 arguments (order matters).

```

mlGene input_Train.csv input_Test.csv prefix seed number_of_clusters

   input_Train.csv            -         Training input CSV file
   input_Test.csv             -         Test input CSV file
   prefix                     -         Prefix for output files
   seed                       -         Integer value, set seed for reproducible output
   number_of_clusters         -         Integer value, number of cluster for parallelization

```


 ## Tutorial
A set of example files is downloaded with the installation of GenoMLizer and should be in the `/GenoMLizerSetup` directory (`GenoMLizer_example.vcf.gz`, `GenoMLizer_example_targets`). These example files are provided for quick check of any issues with the installation or dependencies, as well as for testing the functionality of the GenoMLizer commands. Within the dataset, there is a synthetic variant at chr7:71248 with the gene symbol AC093627.7, which perfectly separates the synthetic case and controls in the target file. This variant is expected to be selected by all feature selection strategies, whether using variant or gene variables, and to enable perfect prediction with the ML models.

Here is a tutorial for a quick run through.
```

# Some processes may require additional memory in R
# If an error occurs, the --max-ppsize can be set from the command line with the following example command 
export GENOMLIZER_PPSIZE= 


# Variant assessment, number_of_clusters can be adjusted for your system

# Create dataset
datasetCreator GenoMLizer_example.vcf.gz GenoMLizer_example_targets GenoMLizer_example.csv

# Split the dataset
splitTrainTest GenoMLizer_example.csv 0.8 123

# Test CMI feature selection
# k = 5
CMI GenoMLizer_example_Train.csv GenoMLizer_example_Train_CMI.csv 5 123 1
# k = 2
CMI GenoMLizer_example_Train.csv GenoMLizer_example_Train_CMI.csv 2 123 1

# Test GLM feature selection
# test = Chisq
GLM GenoMLizer_example_Train.csv GenoMLizer_example_Train_GLM-chi.csv Chisq 0.1 123 1
# test = F
GLM GenoMLizer_example_Train.csv GenoMLizer_example_Train_GLM-F.csv F 0.1 123 1

# Test DTVI
DTVI GenoMLizer_example_Train_GLM-chi.csv GenoMLizer_example_Train_GLM-chi_DTVI.csv 0 0.51 1000 2 123 1

# Test variant test set prep
varPrep GenoMLizer_example_Train_GLM-chi_DTVI.csv GenoMLizer_example_Test.csv GenoMLizer_example_Test_prepped.csv

# Test ML variant analysis
mlVar GenoMLizer_example_Train_GLM-chi_DTVI.csv GenoMLizer_example_Test_prepped.csv 0 GLM-DTVI 123 1



# Gene assessment, number_of_clusters can be adjusted for your system

# Gene transformation SFC
geneTransform GenoMLizer_example_Train_GLM-chi.csv GenoMLizer_example_Train_GLM-chi_gene-SFC.csv 25000 SFC 0.5

# Test additional gene variable feature selection
GLM GenoMLizer_example_Train_GLM-chi_gene.csv GenoMLizer_example_Train_GLM-chi_gene_GLM-F.csv F 0.01 123 1

# Test gene test set prep
genePrep GenoMLizer_example_Train_GLM-chi.csv GenoMLizer_example_Test.csv GenoMLizer_example_Test_genePrepped.csv 25000 1 variables_corrected.csv

# Test ML gene analysis
mlGene GenoMLizer_example_Train_GLM-chi_gene_GLM-F.csv GenoMLizer_example_Test_genePrepped.csv gene_test 123 1


```

In our studies mentioned above, we found the best performance with our real datasets to be with the following pipelines.
Variant pipeline
* CMI-5_GLM-chisq-0.1_DTVI-1000-1
* CMI-20_DTVI-1000-10
Gene pipeline
* GLM-0.05_GeneTransform_CMI-20
The following commands will perform these analyses with GenoMLizer using the provided dataset as an example.
```

# Create dataset
datasetCreator GenoMLizer_example.vcf.gz GenoMLizer_example_targets GenoMLizer_example.csv

# Split the dataset
splitTrainTest GenoMLizer_example.csv 0.8 123


# CMI-5_GLM-chisq_DTVI-1000-1
# CMI-5
CMI GenoMLizer_example_Train.csv GenoMLizer_example_Train_CMI-5.csv 5 123 1
# GLM-chisq 0.1
GLM GenoMLizer_example_Train_CMI-5.csv GenoMLizer_example_Train_CMI-5_GLM-chi-01.csv Chisq 0.1 123 1
# DTVI-1000-1
DTVI GenoMLizer_example_Train_CMI-5_GLM-chi-01.csv GenoMLizer_example_Train_CMI-5_GLM-chi-01_DTVI.csv 0 1 1000 1 123 1
# Test prep
varPrep GenoMLizer_example_Train_CMI-5_GLM-chi-01_DTVI.csv GenoMLizer_example_Test.csv GenoMLizer_example_Test_prepped_CMI-5_GLM-chisq-01_DTVI-1000-1.csv
# ML variant analysis
mlVar GenoMLizer_example_Train_CMI-5_GLM-chi-01_DTVI.csv GenoMLizer_example_Test_prepped_CMI-5_GLM-chisq-01_DTVI-1000-1.csv 0 CMI_GLM_DTVI 123 1


# CMI-20_DTVI-1000-10
# CMI-20
CMI GenoMLizer_example_Train.csv GenoMLizer_example_Train_CMI-20.csv 20 123 1
# DTVI-1000-1
DTVI GenoMLizer_example_Train_CMI-20.csv GenoMLizer_example_Train_CMI-20_DTVI.csv 0 1 1000 10 123 1
# Test prep
varPrep GenoMLizer_example_Train_CMI-20_DTVI.csv GenoMLizer_example_Test.csv GenoMLizer_example_Test_prepped_CMI-20_DTVI-1000-10.csv
# ML variant analysis
mlVar GenoMLizer_example_Train_CMI-20_DTVI.csv GenoMLizer_example_Test_prepped_CMI-20_DTVI-1000-10.csv 0 CMI_DTVI 123 1


# GLM-0.05_GeneTransform_CMI-20
# GLM-chisq-0.05
GLM GenoMLizer_example_Train.csv GenoMLizer_example_Train_GLM-chi-005.csv Chisq 0.05 123 1
# Gene Transform NC
geneTransform GenoMLizer_example_Train_GLM-chi-005.csv GenoMLizer_example_Train_GLM-chi-005_gene-NC.csv 25000 NC
# CMI-20
CMI GenoMLizer_example_Train_GLM-chi-005_gene-NC.csv GenoMLizer_example_Train_GLM-chi-005_gene-NC_CMI-20.csv 20 123 1
# Test gene test set prep
genePrep GenoMLizer_example_Train_GLM-chi-005.csv GenoMLizer_example_Test.csv GenoMLizer_example_Test_genePrepped_GLM-005_GeneTransform_CMI-20.csv 25000 0
# Test ML gene analysis
mlGene GenoMLizer_example_Train_GLM-chi-005_gene-NC_CMI-20.csv GenoMLizer_example_Test_genePrepped_GLM-005_GeneTransform_CMI-20.csv GLM-005_GeneTransform_CMI-20 123 1


```


 ## Advanced Setup 

To increase memory for R processes, `--max-ppsize` can be set with the following command. 
```
export GENOMLIZER_PPSIZE=
```

As mentioned in the [Usage](#usage) section, The VCF file must be filtered to included variants with only one alternative allele. There are a few exceptions to this and some alternative options if there is a need to retain all the variants. 
* datasetCreator can function correctly with variants up to 9 alternative alleles
* DTVI and mlVar commands with the `allele_factorization = 1` must have variants/variables with only one alternative allele
* With `allele_factorization = 0` these commands will function correctly with multiple alternative alleles
* Another option would be to transform the variants in the VCF file or the allele variables after running `datasetCreator` to make all alternative alleles encoded as 1

Most of the GenoMLizer commands function with temporary files. If multiple of the same commands are running simultaneously in the same directory, this may cause an error due to writing to or deletion of temporary files. To mitigate this, try to set up directories for each run.


