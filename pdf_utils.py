# -*- coding: utf-8 -*-
"""
PDF Extraction Functions  
Developed by Iris Vantieghem (July 2025)

This module contains core functions for extracting participant-level timeseries data 
from semi-structured PDFs. It identifies date-labelled sections and parses `parameter: value` lines 
into structured records.

Functions:
• extract_data_from_pdf(...)  
  Opens PDFs and extracts date-labelled data blocks per participant.

• process_current_data(...)  
  Parses individual blocks into row-wise dictionaries.

• extract_all_data(...)  
  Iterates through folders with participant PDFs and consolidates all data.

Designed for use via the main script 'pdf_timeseries_extractor.py' and config file.  
"""

import sys
import os
import re
import pdfplumber
import pandas as pd
from parsing_utils import is_likely_date_line, parse_flexible_date

def extract_data_from_pdf(file_paths, participant_id, dayfirst=True):
    
    extracted_data = []

    for file_path in file_paths:
        with pdfplumber.open(file_path) as pdf:
            current_date = None
            current_data = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    for line in text.splitlines():
                        clean_line = re.sub(r'^[=*\-–\s]+|[=*\-–\s]+$', '', line.strip()) # remove unnecessary signs

                        if is_likely_date_line(clean_line):
                            parsed_date = parse_flexible_date(clean_line, dayfirst=dayfirst)
                        else:
                            parsed_date = None

                        if parsed_date:
                            if current_date and current_data:
                                process_current_data(current_date, current_data, extracted_data, participant_id)
                            current_date = clean_line # unnecessary signs have been removed
                            current_data = ""

                        elif ":" in line:
                            current_data += line + "\n"
            if current_date and current_data:
                process_current_data(current_date, current_data, extracted_data, participant_id)
    return pd.DataFrame(extracted_data)

def process_current_data(current_date, current_data, extracted_data, participant_id):

    for line in current_data.splitlines():
        if ":" in line:
            param, value = line.split(":", 1)
            extracted_data.append({
                "Participant ID": participant_id,
                "Date": current_date,
                "Parameter": param.strip(),
                "Value": value.strip()
            })

def extract_all_data(main_folder, dayfirst=True):
    all_data = []
    for folder_name in os.listdir(main_folder):
        folder_path = os.path.join(main_folder, folder_name)
        if os.path.isdir(folder_path):
            participant_id = folder_name  # Generic: use folder name directly
            pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
            folder_data = extract_data_from_pdf(pdf_files, participant_id, dayfirst=dayfirst)
            all_data.append(folder_data)
    combined = pd.concat(all_data, ignore_index=True)
    
    if "Value" not in combined.columns:
        print("[ERROR] No 'Value' column found. Likely extraction failed.")
        print("Extracted columns:", combined.columns.tolist())
        sys.exit()

    wide = combined.pivot_table(index=["Participant ID", "Date"], columns="Parameter", values="Value", aggfunc="first").reset_index()

    wide["Date"] = wide["Date"].apply(lambda x: parse_flexible_date(x, dayfirst=dayfirst))
    wide = wide.dropna(subset=["Date"])
    wide = wide.sort_values(by=["Participant ID", "Date"]).reset_index(drop=True)
    return wide