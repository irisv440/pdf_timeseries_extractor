# PDF Timeseries Extractor
A Python repository for extracting participant-level timeseries data from semi-structured PDFs.
Supports multiple date formats (EU/US), flexible grouping (month/week), and clean Excel output formatting.

The tool has originally been developed for analyzing time-based diary data in neuroscience and health research contexts (e.g. energy levels, task types, perceived strain). 
The extractor has been rewritten in order to be domain-agnostic and can be reused in any context where PDFs contain temporal self-report logs.

## Key Features
- Extracts `parameter: value` entries following recognized date lines
- Recognizes various date formats (e.g. `24/07/2020`, `July 24, 2020`, `Monday 24 July 2020`)
- Automatically detects participant folders and loops through multiple PDFs
- Groups output per month, week, or not at all — depending on configuration
- Outputs cleaned `.xlsx` files in which each row represents a participant-day, and each column a separate parameter.

## Configuration
Settings are defined in `config.yaml`. Example:
main_folder: "example_data"
output_folder: "output"
grouping_mode: "month"        # Options: "month", "week", "none"
date_format_style: "EU"       # Options: "EU", "US"

## Project Structure

• **example_data/**  
 Contains sample participant folders with PDF logs. Each folder (e.g., `Participant_001/`) includes 4 weekly PDF files with semi-structured entries.

• **output/**  
 Output folder where grouped Excel files are saved. Example:  
 `timeseries_data_2020-07_EU_*.xlsx`, `timeseries_data_2020-08_US_*.xlsx`

• **config.yaml**  
 YAML file where you define the data folder, output folder, date format (EU/US), and grouping mode (month/week/none).

• **pdf_timeseries_extractor.py**  
 Main Python script: loads configuration, coordinates PDF processing and exports (grouped) Excel files.

• **pdf_utils.py**  
 Handles PDF reading and parsing per page, detects date labels and collects structured content.

• **parsing_utils.py**  
 Includes helpers for date parsing and flexible date-line detection.

• **generate_mock_timeseries_logs.py**  
 Optional script for generating synthetic participant PDF logs (for demo or testing).

Example of config.yaml:

grouping_mode: month     # 'month', 'week', 'none'
date_format_style: EU    # 'EU' or 'US'
main_folder: example_data
output_folder: output

## How to use

Make sure you are using Python 3.9 or higher.
1. Install required packages using pip:
   ```bash
   pip install pandas pdfplumber pyyaml python-dateutil
2. Place your participant PDFs in folders under `example_data/`
3. Adjust `config.yaml` as needed
4. Run the extractor: python pdf_timeseries_extractor.py
Excel output will appear in the `output/` folder.

Notes:
• There is no limit to the number of PDFs to be processed.
• The script automatically loops through all .pdf files in all participant folders under example_data/.
• Performance may vary depending on your system, but typical research datasets (e.g. 10–100 participants × 1–4 PDFs each) are handled efficiently.

## Example Output
- `timeseries_data_2020-07_EU_*.xlsx` → grouped per month (EU date style)
- `timeseries_data_2020-08_EU_*.xlsx`
- `timeseries_data_2020-07_US_*.xlsx` → grouped per month (US date style)
- `timeseries_data_2020-08_US_*.xlsx`
## Notes
- Non-date headers (e.g. "Log Week 1", decorative lines) are automatically skipped
- Parameter/value pairs are only extracted after a valid date label
- Can handle multi-page PDFs and gaps between days
- Fully anonymized and reusable in open-science projects

## Author
Created by Iris Vantieghem – Contact: via GitHub profile

## License
This project is licensed under the MIT License – see LICENSE for details.