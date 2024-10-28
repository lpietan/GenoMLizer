#!/bin/bash/env Rscript

## Load analysis packages
library(MachineShop)
library(recipes)
library(readr)

## Get arguments
args <- commandArgs(trailingOnly = TRUE)

## Register cores for parallel processing
library(doSNOW)
registerDoSNOW(makeCluster(as.numeric(args[5])))

## Load data
d <- read_csv(args[1])
d <- as.data.frame(d)
d1 <- d[,1]
d <- d[,-1]
rownames(d) <- d1
d$Targets <- factor(d$Targets)

cat("  *************************   DATASET SUMMARY   *************************  ")
str(d) %>% head

t_df <- d[1]
CMI_dataframe <- t_df
targets <- t_df$Targets
i <- 2:length(d)
cat("Initial index list Complete")

## CMI filter for step_sbf()
cmi_filter <- function(x, y, step) {
  res <- praznik::CMI(x, y, k = step$k)
  selected <- rep(FALSE, ncol(x))
  selected[res$selection] <- TRUE
  score <- rep(NA, ncol(x))
  score[res$selection] <- res$score
  data.frame(selected = selected, score = score)
}

## Change seed for different random intermidiate dataset selections.
set.seed(as.numeric(args[4]))
while (length(i) > 999)
{
cat(length(i))
variables_selected <- sample(x=i, size=1000)
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Recipe with custom CMI step
cmi_rec <- recipe(Targets ~ ., data = df_2) %>%
  step_sbf(all_predictors(), filter = cmi_filter, multivariate = TRUE,
           options = list(k = as.numeric(args[3])))

## Trained recipe
cmi_prep <- prep(cmi_rec)
## Applied recipe
f <- bake(cmi_prep, df_2)
f <- f[1:length(f) - 1]
## Add CMI selected variable to final dataset
CMI_dataframe <- cbind(CMI_dataframe, f)
## Remove selected variable from index list for next iteration
i <- i[! i %in% variables_selected]
}


cat(length(i))
if (length(i) < 999 & length(i) >= as.numeric(args[3])){
variables_selected <- i
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Recipe with custom CMI step
cmi_rec <- recipe(Targets ~ ., data = df_2) %>%
  step_sbf(all_predictors(), filter = cmi_filter, multivariate = TRUE,
           options = list(k = as.numeric(args[3])))

## Trained recipe
cmi_prep <- prep(cmi_rec)
## Applied recipe
f <- bake(cmi_prep, df_2)
f <- f[1:length(f) - 1]
## Add CMI selected variable to final dataset
CMI_dataframe <- cbind(CMI_dataframe, f)
} else if (length(i) < as.numeric(args[3]) & length(i) > 0){

variables_selected <- i
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Recipe with custom CMI step
cmi_rec <- recipe(Targets ~ ., data = df_2) %>%
  step_sbf(all_predictors(), filter = cmi_filter, multivariate = TRUE,
           options = list(k = length(i)))

## Trained recipe
cmi_prep <- prep(cmi_rec)
## Applied recipe
f <- bake(cmi_prep, df_2)
f <- f[1:length(f) - 1]
## Add CMI selected variable to final dataset
CMI_dataframe <- cbind(CMI_dataframe, f)
}

## Save results
df_final <- as.data.frame(CMI_dataframe)
write.csv(df_final, args[2], row.names = TRUE)

h <- length(df_final)
cat("Number of selected variables")
cat(h)

print("CMI Filtering Complete")

if (int(args[6])==1){
col_names <- colnames(df_final)
write.csv(col_names, "", row.names=FALSE)
}

quit(save="no")

