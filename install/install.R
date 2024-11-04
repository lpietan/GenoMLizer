#!/bin/bash/env Rscript
if(!require(MachineShop)) install.packages("MachineShop",repos = "http://cran.us.r-project.org")
if(!require(recipes)) install.packages("recipes",repos = "http://cran.us.r-project.org")
if(!require(readr)) install.packages("readr",repos = "http://cran.us.r-project.org")
if(!require(doSNOW)) install.packages("doSNOW",repos = "http://cran.us.r-project.org")
if(!require(dplyr)) install.packages("dplyr",repos = "http://cran.us.r-project.org")
