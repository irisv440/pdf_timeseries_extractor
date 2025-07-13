# -*- coding: utf-8 -*-
"""
Generic PDF Timeseries Extractor  
Developed by Iris Vantieghem (July 2025)

This tool extracts date-stamped parameter values from semi-structured PDFs 
(e.g., diary-style logs) and converts them into wide-format Excel files.

This main script:
- Loads configuration from `config.yaml`
- Coordinates PDF parsing via helper modules
- Exports cleaned and optionally grouped Excel files

Configurable grouping options: 'month', 'week', or 'none'  
Participant IDs and metadata are generically extracted from folder names.
"""

import os
import yaml
import pandas as pd
from datetime import datetime
from pathlib import Path
from pdf_utils import extract_all_data


base_path = Path(__file__).resolve().parent

# Reading the configuration from a .yaml file:
with open(base_path / "config.yaml", "r") as f:
    config = yaml.safe_load(f)

GROUPING_MODE = config["grouping_mode"] # month, week or none
DATE_FORMAT_STYLE = config["date_format_style"] # EU or US
DAYFIRST = True if DATE_FORMAT_STYLE == "EU" else False

main_folder = base_path / config["main_folder"]
output_folder = base_path / config["output_folder"]

# Make output folder if it doesn't exist yet
os.makedirs(output_folder, exist_ok=True)
print('Using ', DATE_FORMAT_STYLE, ' -style for dates')

def group_and_export(df, output_folder, grouping_mode):
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if grouping_mode == "month":
        df["Group"] = df["Date"].dt.strftime("%Y-%m")
    elif grouping_mode == "week":
        df["Group"] = df["Date"].dt.strftime("W%U_%Y")
    else:
        df["Group"] = "All"

    for group, group_df in df.groupby("Group"):
        filename = f"timeseries_data_{group}_{DATE_FORMAT_STYLE}_{timestamp}.xlsx"
        group_df.to_excel(os.path.join(output_folder, filename), index=False)

# Extraction and export
df = extract_all_data(main_folder, dayfirst=DAYFIRST)
group_and_export(df, output_folder, GROUPING_MODE)
