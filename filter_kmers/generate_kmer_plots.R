#!/usr/bin/Rscript

library("ggplot2")
library("data.table")

args <- commandArgs(TRUE) 
filename <- args[1]

# Read input file
data <- data.table::fread(filename, sep="\t", header=F, col.names = c("kmers", "counts"))

# Plots
ggplot(data, aes(x=counts)) + geom_histogram() + theme_bw()
ggsave(paste(filename,"_hist.png", sep=""))

ggplot(data, aes(x=counts)) + geom_boxplot() + theme_bw()
ggsave(paste(filename,"_boxplot.png", sep=""))

ggplot(data, aes(x=counts)) + stat_ecdf(geom = "point") + theme_bw()
ggsave(paste(filename,"_ecdf.png", sep="")) 
