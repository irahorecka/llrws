#! /usr/bin/Rscript

options(stringsAsFactors=FALSE)

library(optparse)
library(maveLLR)

# Get external arguments passed by the command line
option_list = list(
    make_option(c("-r", "--reference"), type="character", default=NULL,
                help="reference dataset name", metavar="character"),
    make_option(c("-s", "--score"), type="character", default=NULL,
                help="score dataset name", metavar="character"),
    make_option(c("-d", "--downloadpath"), type="character", default=NULL,
                help="path to download output", metavar="character"),
    make_option(c("-k", "--key"), type="character", default=NULL,
                help="unique identifier key", metavar="character")
                );

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

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

#calculate the actual LLR values for the full MAVE dataset using the LLR function
mave$llr <- llrObj$llr(mave$score)

#calculate a 95% confidence interval for the LLR values
mave$llrCIlower <- llrObj$llr(qnorm(0.025,mave$score,mave$se))
mave$llrCIupper <- llrObj$llr(qnorm(0.975,mave$score,mave$se))

#export results to file
export_filename <- paste(opt$downloadpath, "/", opt$key, "-maveLLRs.csv", sep="")
write.csv(mave, paste(export_filename, sep=""))

# write unique filename to stdout
write(export_filename, stdout())
