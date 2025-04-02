#!/usr/bin/env python3
import os
import json
import re
from bs4 import BeautifulSoup

def check_unit_references():
    print("Verifying Unit 2 References...")
    
    # Read the index.html file
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check for any remaining "Unit 1" references that should have been updated
    unit1_references = re.findall(r'Unit 1', html_content)
    if unit1_references:
        print(f"WARNING: Found {len(unit1_references)} references to 'Unit 1' that might need updating")
    else:
        print("✓ No remaining 'Unit 1' references found")
    
    # Check that exam weight is correctly set to 5-7%
    exam_weight_pattern = r'Unit 2 represents (\d+-\d+)% of the AP Statistics Exam'
    exam_weight_match = re.search(exam_weight_pattern, html_content)
    
    if exam_weight_match and exam_weight_match.group(1) == '5-7':
        print("✓ Exam weight correctly set to 5-7%")
    else:
        print("WARNING: Exam weight not correctly set to 5-7%")
    
    # Parse the HTML to extract the pdfFiles array 
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the script tag containing the pdfFiles array
    script_tags = soup.find_all('script')
    pdf_files_script = None
    
    for tag in script_tags:
        if tag.string and 'pdfFiles =' in tag.string:
            pdf_files_script = tag.string
            break
    
    if not pdf_files_script:
        print("ERROR: Could not find pdfFiles array in the HTML")
        return
    
    # Check PDF paths in the pdfFiles array
    expected_pdfs = []
    for i in range(2, 10):  # Topics 2.2 to 2.9
        expected_pdfs.append(f"pdfs/unit2/2.{i}_quiz.pdf")
        expected_pdfs.append(f"pdfs/unit2/2.{i}_answers.pdf")
    
    # Add progress check PDFs
    expected_pdfs.extend([
        "pdfs/unit2/unit2_pc_frq_quiz.pdf",
        "pdfs/unit2/unit2_pc_frq_answers.pdf",
        "pdfs/unit2/unit2_pc_mcq_parta_answers.pdf",
        "pdfs/unit2/unit2_pc_mcq_partb_answers.pdf"
    ])
    
    missing_pdfs = []
    for expected_pdf in expected_pdfs:
        if expected_pdf not in html_content:
            missing_pdfs.append(expected_pdf)
    
    if missing_pdfs:
        print(f"WARNING: {len(missing_pdfs)} expected PDF paths not found in HTML:")
        for pdf in missing_pdfs:
            print(f"  - {pdf}")
    else:
        print("✓ All expected PDF paths found in HTML")
    
    print("\nVerification complete!")

if __name__ == "__main__":
    check_unit_references()