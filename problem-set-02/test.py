from pathlib import Path
import pandas as pd

# Sets the directory relative to test.py's location
data_dir = Path(__file__).parent / "data"
flights = pd.read_csv(data_dir / "nycflights.csv")
gss = pd.read_csv(data_dir / "gss2010.csv")
study = pd.read_csv(data_dir / "gpa_study_hours.csv")
print("nycflights:", flights.shape)
print("gss2010:", gss.shape)
print("gpa_study_hours:", study.shape)