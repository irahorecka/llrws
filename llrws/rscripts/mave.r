#!/usr/bin/env Rscript

options(stringsAsFactors=FALSE)

library(optparse)
library(maveLLR)


# Get external arguments passed by the command line.
# ==============================================================================

option_list = list(
    # Full filepath to the reference CSV file.
    make_option(c("-r", "--reference"), type="character", default=NULL,
                help="reference dataset filepath", metavar="character"),
    # Full filepath to the score CSV file.
    make_option(c("-s", "--score"), type="character", default=NULL,
                help="score dataset filepath", metavar="character"),
    # Full filepath to the download (postprocessed) CSV file.
    make_option(c("-d", "--downloadpath"), type="character", default=NULL,
                help="download dataset filepath", metavar="character"),
    # Unique identifier (str).
    make_option(c("-k", "--key"), type="character", default=NULL,
                help="unique identifier key", metavar="character")
);

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# ==============================================================================


# Begin MAVE data processing.
# ==============================================================================

# Load MAVE dataset from file...
mave <- read.csv(opt$score,comment.char="#")
# ...and index by variant descriptor (HGVS).
rownames(mave) <- mave$hgvs_pro
# Load benchmark from file.
benchmark <- read.csv(opt$reference)

# Extract MAVE scores for positive reference variants from benchmark...
posScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Positive"]),"score"])
# ...and the same for negative reference variants.
negScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Negative"]),"score"])

# Call the buildLLR.kernel function from maveLLR using the two reference score vectors.
llrObj <- buildLLR.kernel(posScores,negScores,bw=0.1,kernel="gaussian")

# Calculate the actual LLR values for the full MAVE dataset using the LLR function.
mave$llr <- llrObj$llr(mave$score)

# Calculate a 95% confidence interval for the LLR values.
mave$llrCIlower <- llrObj$llr(qnorm(0.025,mave$score,mave$se))
mave$llrCIupper <- llrObj$llr(qnorm(0.975,mave$score,mave$se))

# ==============================================================================


# Export results to file and return control to caller.
# ==============================================================================

export_filename <- paste(opt$downloadpath, "/", opt$key, "-maveLLRs.csv", sep="")
write.csv(mave, paste(export_filename, sep=""))
# Write unique filename to stdout.
write(export_filename, stdout())

# ==============================================================================
