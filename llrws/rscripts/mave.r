#! /usr/bin/Rscript

options(stringsAsFactors=FALSE)

library(optparse)
library(maveLLR)

# Get external arguments passed by the command line
option_list = list(
    make_option(c("-r", "--reference"), type="character", default=NULL,
                help="reference dataset name", metavar="character"),
    make_option(c("-s", "--score"), type="character", default=NULL,
                help="score dataset name", metavar="character")
                );

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# Check valid file path is provided
if (is.null(opt$reference)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).", call.=FALSE)
}

#load MAVE dataset from file
mave <- read.csv(opt$score,comment.char="#")
#and index by variant descriptor (HGVS)
rownames(mave) <- mave$hgvs_pro
#load benchmark from file
benchmark <- read.csv(opt$reference)

#extract MAVE scores for positive reference variants from benchmark
posScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Positive"]),"score"])
#and the same for negative reference variants
negScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Negative"]),"score"])

#call the buildLLR.kernel function from maveLLR using the two reference score vectors
llrObj <- buildLLR.kernel(posScores,negScores,bw=0.1,kernel="gaussian")

#optional: use a helper function to draw a visualization of the LLR function
drawDensityLLR(mave$score, llrObj$llr, llrObj$posDens, llrObj$negDens, posScores, negScores)

#calculate the actual LLR values for the full MAVE dataset using the LLR function
mave$llr <- llrObj$llr(mave$score)

#calculate a 95% confidence interval for the LLR values
mave$llrCIlower <- llrObj$llr(qnorm(0.025,mave$score,mave$se))
mave$llrCIupper <- llrObj$llr(qnorm(0.975,mave$score,mave$se))
#export results to file
write.csv(mave,"maveLLRs.csv")
