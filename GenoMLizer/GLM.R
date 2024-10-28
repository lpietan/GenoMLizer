#!/bin/bash/env Rscript

## Load analysis packages
library(MachineShop)
library(recipes)
library(readr)

## Get arguments
args <- commandArgs(trailingOnly = TRUE)

## Register cores for parallel processing
library(doSNOW)
registerDoSNOW(makeCluster(as.numeric(args[6])))

## Load data
d <- read_csv(args[1])
d <- as.data.frame(d)
d1 <- d[,1]
d <- d[,-1]
rownames(d) <- d1
d$Targets <- factor(d$Targets)

h <- length(d)
cat("Number of variables in starting dataset")
cat(h)

## Start GLM filter
cat("Starting GLM Filtering")
cat("  *************************   DATASET SUMMARY   *************************  ")
str(d) %>% head

t_df <- d[1]
UniGLM_dataframe <- t_df
targets <- t_df$Targets
i <- 2:length(d)
cat("Initial index list Complete")

if (args[3] == "F"){
cat("Using F test for GLM filter")
glm_filter <- function(x, y, step) {
  model_fit <- glm(y ~ ., family = binomial, data = data.frame(y, x))
  p_value <- drop1(model_fit, test = "F")[-1, "Pr(>F)"]
  p_value < step$threshold
}
} else {
cat("Using Chisq test for GLM filter")
glm_filter <- function(x, y, step) {
  model_fit <- glm(y ~ ., family = binomial, data = data.frame(y, x))
  p_value <- drop1(model_fit, test = "Chisq")[-1, "Pr(>Chi)"]
  p_value < step$threshold
}
}

set.seed(as.numeric(args[5]))
while (length(i) > 999)
{
cat(length(i))
variables_selected <- sample(x=i, size=1000)
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Recipe with custom univariate SBF step
sbf_rec <- recipe(Targets ~ ., data = df_2) %>%
  step_sbf(all_predictors(), filter = glm_filter,
           options = list(threshold = as.numeric(args[4])))

## Trained recipe
sbf_prep <- prep(sbf_rec)
#tidy(sbf_prep, number = 1)

## Applied recipe
f <- bake(sbf_prep, df_2)
f <- f[1:length(f) - 1]

## Add CMI selected variable to final dataset
UniGLM_dataframe <- cbind(UniGLM_dataframe, f)

## Remove selected variable from index list for next iteration
i <- i[! i %in% variables_selected]
}

cat(length(i))
variables_selected <- i
df_2 <- d[variables_selected]
df_2$Targets <- targets

## Recipe with custom univariate SBF step
sbf_rec <- recipe(Targets ~ ., data = df_2) %>%
  step_sbf(all_predictors(), filter = glm_filter,
           options = list(threshold = as.numeric(args[4])))

## Trained recipe
sbf_prep <- prep(sbf_rec)

## Applied recipe
f <- bake(sbf_prep, df_2)
f <- f[1:length(f) - 1]

## Add CMI selected variable to final dataset
UniGLM_dataframe <- cbind(UniGLM_dataframe, f)

## Save results
d <- as.data.frame(UniGLM_dataframe)
write.csv(d, args[2], row.names = TRUE)

h <- length(d)
cat("Number of selected variables")
cat(h)

cat("Univariate GLM Filtering Complete")

quit(save="no")
