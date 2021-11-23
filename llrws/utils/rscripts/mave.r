#!/usr/bin/env Rscript

options(stringsAsFactors=FALSE)

library(optparse)
library(maveLLR)


# Get external arguments passed by the command line.
# ==============================================================================

option_list <- list(
    # Full filepath to the benchmark CSV file.
    make_option(c("-b","--benchmark"),type="character",default=NULL,
                help="benchmark dataset filepath",metavar="character"),
    # Full filepath to the score CSV file.
    make_option(c("-s","--score"),type="character",default=NULL,
                help="score dataset filepath",metavar="character"),
    # Full filepath to the download (maveLLR-processed) CSV file.
    make_option(c("-d","--download"),type="character",default=NULL,
                help="download maveLLR dataset filepath",metavar="character")
);

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

benchmark_csv_filepath <- opt$benchmark
score_csv_filepath <- opt$score
download_csv_filepath <- opt$download

# ==============================================================================


# Begin MAVE data processing.
# ==============================================================================

# Load benchmark from file.
benchmark <- read.csv(benchmark_csv_filepath)
# Load MAVE dataset from file...
mave <- read.csv(score_csv_filepath,comment.char="#")
# ...and index by variant descriptor (HGVS).
rownames(mave) <- mave$hgvs_pro

# Extract MAVE scores for positive benchmark variants from benchmark...
posScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Positive"]),"score"])
# ...and the same for negative benchmark variants.
negScores <- na.omit(mave[with(benchmark,hgvsp[referenceSet=="Negative"]),"score"])

# Call the buildLLR.kernel function from maveLLR using the two benchmark score vectors.
llrObj <- buildLLR.kernel(posScores,negScores,bw=0.1,kernel="gaussian")

# Calculate the actual LLR values for the full MAVE dataset using the LLR function.
mave$llr <- llrObj$llr(mave$score)

# Calculate a 95% confidence interval for the LLR values.
mave$llrCIlower <- llrObj$llr(qnorm(0.025,mave$score,mave$se))
mave$llrCIupper <- llrObj$llr(qnorm(0.975,mave$score,mave$se))

# ==============================================================================


# Export results to file and return control to caller.
# ==============================================================================

write.csv(mave,download_csv_filepath,row.names=FALSE)
# Return success exit code to caller.
quit(status=0)

# ==============================================================================
