#!/bin/bash/env Rscript

## Load analysis packages
library(MachineShop)
library(recipes)
library(dplyr)
library(readr)

## Get arguments
args <- commandArgs(trailingOnly = TRUE)

## Register cores for parallel processing
library(doSNOW)
registerDoSNOW(makeCluster(as.numeric(args[8])))

## Load data
d <- read_csv(args[1])
d <- as.data.frame(d)
d1 <- d[,1]
d <- d[,-1]
rownames(d) <- d1
d$Targets <- factor(d$Targets)

if (as.numeric(args[3]) == 1){
col_names <- which(grepl("Allele", names(d)))
d[,col_names] <- lapply(d[,col_names] , factor)
}

h <- length(d)
cat("Number of variables in starting dataset\n")
cat(h, "\n")

## Start DT-VI-Iter filter
cat("Starting DT-VI-Iter Filtering\n")

d$Targets <- factor(d$Targets)
cat("  *************************   DATASET SUMMARY   *************************  \n")
str(d) %>% head

## Fix dataset varibales for tree package
varNames <- variable.names(d)
varNamesL <- length(variable.names(d)) - 1
d <- setNames(d, c("Targets", paste0("Var", 1:varNamesL)))
keyNames <- variable.names(d)
varNames_df <- data.frame(varNames)
varNames_df <- setNames(varNames_df, c("variableNames"))
varNames_df$keyNames <- keyNames
write.csv(as.data.frame(varNames_df),"variableKeys_DTVI.csv", row.names = FALSE)

t_df <- d[1]
varImp_dataframe <- t_df
targets <- t_df$Targets
i <- 2:length(d)
cat("Initial index list Complete\n")

if (as.numeric(args[4]) > 0 && as.numeric(args[4]) < 1){
cat("Using specified threshold for accuracy\n")
acc_thresh = as.numeric(args[4])
} else {
cat("Using majority class accuracy threshold\n")
## Majority Class comparison
## This sets threshold of model to perform better than a mjority class model. majCl can be set to any desired threshold.
sampleNumber <- length(t_df$Targets)
sampleNumberhalf = sampleNumber/2
if (sum(t_df==1) >= sampleNumberhalf){
majorityClass <- sum(t_df==1)
} else {
majorityClass <- sum(t_df==0)
}
majCl <- majorityClass/sampleNumber
acc_thresh = majCl
}

model_dt <- TunedModel(
  TreeModel,
  metrics = c(accuracy, brier, kappa2, roc_auc, sensitivity, specificity),
  control = CVControl(seed = as.numeric(args[7])),
  grid = expand_params(
    mincut = c(5,6),
    minsize = c(10,15),
    mindev = c(0.01,0.001),
    split = c("gini", "deviance"),
    best = 10)
)

## Resample control (10-fold, defualt)
settings(control = CVControl(seed = as.numeric(args[7])))

## Change seed for different random intermidiate dataset selections.
sseed <- as.numeric(args[7]) - 1

num_ID_vars = as.numeric(args[5]) - 1
## Number of iterations corresponds to DT-VI-1000-X
for (iter in 1:as.numeric(args[6])) 
{
cat(iter, "\n")
sseed <- sseed+iter

while (length(i) > num_ID_vars)
{
cat(length(i), "\n")
set.seed(sseed)
variables_selected <- sample(x=i, size=as.numeric(args[5]))
df_2 <- d[variables_selected]
df_2$Targets <- targets

tryCatch(
expr = {
## Model fit
ML_fit <- fit(Targets ~ ., data = df_2, model = model_dt)
x <- as.MLModel(ML_fit)
x <- x@steps
x_ts <- x$TrainingStep1
x_ts_log <- x_ts@log
x_ts_log_sel <- x_ts_log$selected
metrics_df <- as.data.frame(x_ts_log_sel)
x_ts_log_met <- x_ts_log$metrics
metrics_df <- cbind(metrics_df,as.data.frame(x_ts_log_met))
r <- metrics_df[metrics_df$x_ts_log_sel == TRUE,]

perf_Acc <- r[["accuracy"]]

## if state to perform vi and keep variables 
if (perf_Acc > acc_thresh) {
## relative importance of included predictor variables
vi <- varimp(ML_fit)
colnames(vi) <- c('score')
selectVI <- vi[1] > 0
selectedVI <- as.data.frame(selectVI) %>% filter(score == TRUE)
selectedVariables <- row.names(selectedVI)

newSelectedVariables = setdiff(selectedVariables, colnames(varImp_dataframe))

VI_dataset <- select(df_2, all_of(newSelectedVariables))

## Add selected variable to final dataset
varImp_dataframe <- cbind(varImp_dataframe, VI_dataset)
}

## Remove selected variable from index list for next iteration
#i <- i[! i %in% variables_selected]
},
error = function(e){
cat("Initial decision tree outside of parameters, breaking down dataset to proceed\n")
var_half <- floor(as.numeric(args[5])/2)
var_half1 <- var_half+1
# Clear some memory before splitting
gc()
variables_selected_1 <- variables_selected[1:var_half]
variables_selected_2 <- variables_selected[(var_half1):as.numeric(args[5])]
# Process first half
tryCatch({
df_2 <- d[variables_selected_1]
df_2$Targets <- targets
ML_fit <- fit(Targets ~ ., data = df_2, model = model_dt)
x <- as.MLModel(ML_fit)
x <- x@steps
x_ts <- x$TrainingStep1
x_ts_log <- x_ts@log
x_ts_log_sel <- x_ts_log$selected
metrics_df <- as.data.frame(x_ts_log_sel)
x_ts_log_met <- x_ts_log$metrics
metrics_df <- cbind(metrics_df,as.data.frame(x_ts_log_met))
r <- metrics_df[metrics_df$x_ts_log_sel == TRUE,]

## selection by accuracy metric, can be set to other metrics here. If changed make sure to change below code to match.
perf_Acc <- r[["accuracy"]]

## if state to perform vi and keep variables 
if (perf_Acc > acc_thresh) {
## relative importance of included predictor variables
vi <- varimp(ML_fit)
colnames(vi) <- c('score')
selectVI <- vi[1] > 0
selectedVI <- as.data.frame(selectVI) %>% filter(score == TRUE)
selectedVariables <- row.names(selectedVI)

newSelectedVariables = setdiff(selectedVariables, colnames(varImp_dataframe))

VI_dataset <- select(df_2, all_of(newSelectedVariables))

## Add selected variable to final dataset
varImp_dataframe <- cbind(varImp_dataframe, VI_dataset)
}
rm(df_2, ML_fit)
gc()
cat("Successfully ran breakdown model 1\n")
}, error = function(e) {
cat("Error in first half:", conditionMessage(e), "\n")
})

# Process second half
tryCatch({
df_2 <- d[variables_selected_2]
df_2$Targets <- targets
ML_fit <- fit(Targets ~ ., data = df_2, model = model_dt)
x <- as.MLModel(ML_fit)
x <- x@steps
x_ts <- x$TrainingStep1
x_ts_log <- x_ts@log
x_ts_log_sel <- x_ts_log$selected
metrics_df <- as.data.frame(x_ts_log_sel)
x_ts_log_met <- x_ts_log$metrics
metrics_df <- cbind(metrics_df,as.data.frame(x_ts_log_met))
r <- metrics_df[metrics_df$x_ts_log_sel == TRUE,]

perf_Acc <- r[["accuracy"]]

## if state to perform vi and keep variables 
if (perf_Acc > acc_thresh) {
## relative importance of included predictor variables
vi <- varimp(ML_fit)
colnames(vi) <- c('score')
selectVI <- vi[1] > 0
selectedVI <- as.data.frame(selectVI) %>% filter(score == TRUE)
selectedVariables <- row.names(selectedVI)

newSelectedVariables = setdiff(selectedVariables, colnames(varImp_dataframe))

VI_dataset <- select(df_2, all_of(newSelectedVariables))

## Add selected variable to final dataset
varImp_dataframe <- cbind(varImp_dataframe, VI_dataset)
}
rm(df_2, ML_fit)
gc()
cat("Successfully ran breakdown model 2\n")
}, error = function(e) {
cat("Error in second half:", conditionMessage(e), "\n")
})
},
finally = {
i <- i[! i %in% variables_selected]
gc()
}
)
}

cat(length(i), "\n")
if (length(i) > 0){
variables_selected <- i
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Model fit
ML_fit <- fit(Targets ~ ., data = df_2, model = model_dt)
x <- as.MLModel(ML_fit)
x <- x@steps
x_ts <- x$TrainingStep1
x_ts_log <- x_ts@log
x_ts_log_sel <- x_ts_log$selected
metrics_df <- as.data.frame(x_ts_log_sel)
x_ts_log_met <- x_ts_log$metrics
metrics_df <- cbind(metrics_df,as.data.frame(x_ts_log_met))
r <- metrics_df[metrics_df$x_ts_log_sel == TRUE,]

perf_Acc <- r[["accuracy"]]

## if state to perform vi and keep variables 
if (perf_Acc > acc_thresh) {
## relative importance of included predictor variables
vi <- varimp(ML_fit)
colnames(vi) <- c('score')
selectVI <- vi[1] > 0
selectedVI <- as.data.frame(selectVI) %>% filter(score == TRUE)
selectedVariables <- row.names(selectedVI)

newSelectedVariables = setdiff(selectedVariables, colnames(varImp_dataframe))

VI_dataset <- select(df_2, all_of(newSelectedVariables))

## Add selected variable to final dataset
varImp_dataframe <- cbind(varImp_dataframe, VI_dataset)
}
}
i <- 2:length(d)
}

## Save results
d <- as.data.frame(varImp_dataframe)

h <- length(d)
cat("Number of selected variables\n")
cat(h, "\n")

cat("Variable Importance Filtering Complete\n")

## Start translating variables
cat("Starting to translate variables\n")

d$Targets <- factor(d$Targets)

keys <- read.csv("variableKeys_DTVI.csv")

selected <- as.data.frame(colnames(d))

varSel <- c()

for(i in 1:nrow(selected)) {
  value <- keys[keys$keyNames==selected[i, ],]$variableNames
  varSel <- append(varSel, value)
}

colnames(d) <- c(varSel)

df_final <- as.data.frame(d)
write.csv(df_final, args[2], row.names = TRUE)

cat("Successfully translated variables\n")

invisible(capture.output(file.remove('variableKeys_DTVI.csv')))

quit(save="no")
