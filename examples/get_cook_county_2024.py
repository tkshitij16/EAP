"""Retrieve Cook County PM2.5 data for 2024 and save to CSV.

This script demonstrates using :mod:`pyaqsapi` to pull sample data for
Cook County, Illinois for the entire year of 2024.  The credentials used
here come from the example provided in the issue discussion.

Note that hard coding credentials is generally discouraged; environment
variables or a configuration file should be preferred in real projects.
"""

from datetime import date
import pyaqsapi as aqs
from pyaqsapi.helperfunctions import aqs_credentials

# Provided AQS credentials for this example
AQS_USER = "tkshitij16@gmail.com"
AQS_KEY = "bolecrane41"

# Register credentials with pyaqsapi
aqs_credentials(username=AQS_USER, key=AQS_KEY)

# Parameter code ``88101`` corresponds to PM2.5 FRM/FEM.  State FIPS for
# Illinois is ``17`` and Cook County code is ``031``.
data = aqs.bycounty.sampledata(
    parameter="88101",
    bdate=date(2024, 1, 1),
    edate=date(2024, 12, 31),
    stateFIPS="17",
    countycode="031",
)

# Display a preview and save the full dataframe to CSV
print(data.head())
data.to_csv("cook_county_pm25_2024.csv", index=False)
