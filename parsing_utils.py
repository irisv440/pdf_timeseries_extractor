# -*- coding: utf-8 -*-
"""
Date String Parsing Utilities  
Developed by Iris Vantieghem (July 2025)

This module provides utility functions for recognizing and parsing date strings 
from semi-structured text data (e.g., extracted PDF lines).

Functions:
• is_likely_date_line(line): detects whether a line likely contains a date, 
  based on known numeric and textual patterns (EU and US).
• parse_flexible_date(date_str, dayfirst=True): attempts to convert a date string 
  to a Python datetime object using multiple fallback strategies.

"""

import re
from datetime import datetime
from dateutil.parser import parse

def is_likely_date_line(line):
    line = line.strip()

    numeric_match = re.match(r"^(?:\w+\s+)?\d{1,2}[/-]\d{1,2}[/-]\d{4}$", line)
    eu_text_match = re.match(r"^(?:\w+\s+)?\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$", line)
    us_text_match = re.match(r"^(?:\w+\s+)?(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s+\d{4}$", line)

    return bool(numeric_match or eu_text_match or us_text_match)   
        
def parse_flexible_date(date_str, dayfirst=True):
    """
    Attempts to parse a date string using several known formats.
    Supports both numeric (e.g. 13/07/2020) and full month name formats (e.g. 13 July 2020).
    """
    try:
        return datetime.strptime(date_str, "%A %d/%m/%Y")  # e.g., Thursday 13/07/2020
    except ValueError:
        try:
            return datetime.strptime(date_str, "%A %d %B %Y")  # e.g., Thursday 13 July 2020
        except ValueError:
            try:
                return parse(date_str, dayfirst=dayfirst)  # fallback using dateutil
            except Exception as e:
                print(f"Could not parse date '{date_str}': {e}")
                return None

