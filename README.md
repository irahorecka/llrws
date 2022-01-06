# LLRWS

Log Linear Regression (LLR) Web Service. LLRWS is a web service to generate an LLR dataset from a MAVE scoreset and variant reference file (both CSV).

<p align="center">
    <img src="documentation/landing-page.png">
</p>

## Background

It is often that a valuable tool is developed in research without an interface for the common user. This web application attempts to provide a facile interface for such a tool.

MAVE LLR is an algorithm that provides functional variant scores for a variant observed in the clinic. This evaluation provides a rapid estimate on its health effects on the patient.

The algorithm requires a functional score for each variant and a reference data set unto which the score is calibrated.

Functional score CSV file and reference data CSV file are to be dragged-and-dropped (or uploaded) into their respective
zones on the web page. An automated validator is implemented to ensure that required columns and data types are fulfilled
for both files.

Once both files have been successfully uploaded, the user may click "Get MAVE LLR" to generate LLR scores for each variant
sourced from the two uploaded files. The generated data will populate in the empty table at the bottom of the page. This
table allows various functionalities, such as searching keywords in the "HGVS Pro" column, displaying N number of entries
in the table before changing pages, and sorting for every column except "HGVS Pro".

The table currently does not have a feature for the user to download the LLR table as a CSV file, but this is planned to be
incorporated in future releases.

## Installation and configuration

Python>=3.6 is required. Install application requirements using pip:

`$ pip install -r requirements.txt`

Start up the flask web application:

`$ python run.py`

On macOS Big Sur, port 5000 is reserved for AirPlay. This app is configured for port 5001, instead.
Navigate to `http://localhost:5001` on your favorite browser.

## Navigation

Navigation

## Current release

Current release

## Contribute

- [Issues Tracker](https://github.com/irahorecka/llrws/issues)
- [Source Code](https://github.com/irahorecka/llrws/tree/master/llrws)

## Support

If you are having issues or would like to propose a new feature, please use the [issues tracker](https://github.com/irahorecka/llrws/issues).

## License

The project is licensed under the MIT license.
