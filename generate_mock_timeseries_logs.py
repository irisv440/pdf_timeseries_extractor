# -*- coding: utf-8 -*-
"""
Mock Timeseries Log Generator  
Developed by Iris Vantieghem (July 2025)

This script generates semi-structured PDF logs simulating participant-level daily tracking data. 
Each PDF includes 4–7 day entries sampled from a realistic date range, with optional gaps between days.

Outputs are saved to `example_data/` using participant IDs (e.g., Participant_005) and week suffixes.

Customizable parameters:
- Number of PDFs and days per PDF
- Range of date offsets
- Task samples, energy ratings, and notes
"""


from fpdf import FPDF
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

base_path = Path(__file__).resolve().parent

# Output path
output_dir = "example_data"
os.makedirs(output_dir, exist_ok=True)

# Parameters for generation
participant_ids = ["Participant_005", "Participant_006", "Participant_007", "Participant_008"]
base_date = datetime(2020, 7, 17)
num_pdfs = 4
days_per_pdf = [4, 5, 6, 7]

task_samples = [
    "Processed emails", "Cleaned codebase", "Wrote summary report",
    "Attended meeting", "Sorted project files", "Reviewed document",
    "Drafted proposal", "Annotated dataset", "Updated dashboard"
]

notes = [
    "Felt slightly distracted in the afternoon.",
    "Good focus in the morning.",
    "No major issues today.",
    "Interrupted a few times.",
    "Felt productive overall.",
    "Energy drop after lunch.",
    "Struggled to concentrate mid-afternoon."
]

def random_scale():
    return f"{random.randint(3, 9)} / 10"

def generate_day_block(date_obj):
    # block = f"==== {date_obj.strftime('%A %d %B %Y')} ====\n\n" Uncomment this to generate dates in 'Friday 11 July 2024'-format
    # block = f"{date_obj.strftime('%A %d/%m/%Y')}\\n"
    block = f"===={date_obj.strftime('%A %d/%m/%Y')}====\n\n" # Use this to generate dats in 'Friday 11/07/2024'-format
    
    block += f"Energy before work start in the morning: {random_scale()}\n"
    block += f"Energy after morning work block: {random_scale()}\n"
    block += f"Morning tasks: {random.choice(task_samples)}, {random.choice(task_samples)}\n\n"
    block += f"Energy before work start in the afternoon: {random_scale()}\n"
    block += f"Energy after afternoon work block: {random_scale()}\n"
    block += f"Afternoon tasks: {random.choice(task_samples)}, {random.choice(task_samples)}\n\n"
    block += f"Focus level: {random.randint(4, 9)} / 10\n"
    block += f"Interruptions: {random.randint(0, 4)}\n"
    block += f"Mental effort: {random.randint(3, 8)} / 10\n"
    block += f"User notes: {random.choice(notes)}\n\n"
    return block

# Assign a unique start date to each participant
participant_offsets = {
    pid: base_date + timedelta(days=random.randint(-15, 15))
    for pid in participant_ids
}

# Generate PDFs
for pid in participant_ids:
    current_date = participant_offsets[pid]
    for i in range(num_pdfs):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        days = days_per_pdf[i]
        for d in range(days):
            if random.random() < 0.2:
                current_date += timedelta(days=1)
                continue

            block = generate_day_block(current_date)
            for line in block.splitlines():
                pdf.cell(0, 10, txt=line, ln=True)

            current_date += timedelta(days=1)

            if random.random() < 0.15:
                current_date += timedelta(days=random.randint(1, 2))

        filename = f"{pid}_week{i+1}.pdf"
        #path = os.path.join(output_dir, filename)
        participant_dir = os.path.join(output_dir, pid)
        os.makedirs(participant_dir, exist_ok=True) # Create folder for each participant
        path = os.path.join(participant_dir, filename)
        pdf.output(path)
