import subprocess

x = " ".join(
    ' Rscript mave.r --reference="CALM123_jointReference.csv" --score="CALM1_full_imputation_refined_mavedb.csv"   '.split()
)

subprocess.call(x, shell=True)
