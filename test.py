from io import StringIO

import requests
import pandas as pd


files = {
    "benchmark_file": open("CALM123_jointReference.csv", "rb"),
    "score_file": open("CALM1_full_imputation_refined_mavedb.csv", "rb"),
}

response = requests.post("http://localhost:5000/api/", files=files)
df = pd.read_csv(StringIO(response.content.decode("utf-8")))
df.to_csv("test.csv")
print(df)
