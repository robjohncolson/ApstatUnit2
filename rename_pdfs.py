#!/usr/bin/env python3
import os
import shutil
import re

# Define the mapping of topics to their topic numbers
topic_mapping = {
    'IntroducingStatisticsAreVariablesRelated': '2.1',
    'RepresentingTwoCategoricalVariables': '2.2',
    'StatisticsforTwoCategoricalVariables': '2.3',
    'RepresentingtheRelationshipBetweenTwoQuantitativeVariables': '2.4',
    'Correlation': '2.5',
    'LinearRegressionModels': '2.6',
    'Residuals': '2.7',
    'LeastSquaresRegression': '2.8',
    'AnalyzingDeparturesfromLinearity': '2.9',
    'Unit2ProgressCheckFRQ': 'unit2_pc_frq',
    'Unit2ProgressCheckMCQPartA': 'unit2_pc_mcq_parta',
    'Unit2ProgressCheckMCQPartB': 'unit2_pc_mcq_partb',
}

def rename_pdfs():
    # Path to the Unit 2 PDFs
    pdf_dir = 'pdfs/unit2'
    
    # Check if directory exists
    if not os.path.exists(pdf_dir):
        print(f"Directory {pdf_dir} does not exist!")
        return
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    # Create backup directory if it doesn't exist
    backup_dir = f"{pdf_dir}/original_files"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Track successful renames for report
    renamed_files = []
    skipped_files = []
    
    for pdf_file in pdf_files:
        # Skip files that are already in the backup directory
        if pdf_file.startswith("original_files/"):
            continue
        
        # Determine the document type (SG = answers, TB = quiz)
        if pdf_file.startswith('SG_'):
            doc_type = 'answers'
        elif pdf_file.startswith('TB_'):
            doc_type = 'quiz'
        else:
            skipped_files.append((pdf_file, "Unknown prefix"))
            continue
        
        # Extract the topic name
        match = None
        for topic_name in topic_mapping.keys():
            if topic_name in pdf_file:
                match = topic_name
                break
        
        if not match:
            skipped_files.append((pdf_file, "Could not identify topic"))
            continue
        
        # Get the topic number
        topic_num = topic_mapping[match]
        
        # Create the new filename
        new_filename = f"{topic_num}_{doc_type}.pdf"
        
        # Create full paths
        old_path = os.path.join(pdf_dir, pdf_file)
        new_path = os.path.join(pdf_dir, new_filename)
        backup_path = os.path.join(backup_dir, pdf_file)
        
        # Backup original
        shutil.copy2(old_path, backup_path)
        
        # Rename the file
        try:
            os.rename(old_path, new_path)
            renamed_files.append((pdf_file, new_filename))
            print(f"Renamed: {pdf_file} -> {new_filename}")
        except Exception as e:
            skipped_files.append((pdf_file, str(e)))
            print(f"Error renaming {pdf_file}: {e}")
    
    # Print summary
    print("\nRename Summary:")
    print(f"Successfully renamed {len(renamed_files)} files:")
    for old, new in renamed_files:
        print(f"  {old} -> {new}")
    
    if skipped_files:
        print(f"\nSkipped {len(skipped_files)} files:")
        for file, reason in skipped_files:
            print(f"  {file}: {reason}")

if __name__ == "__main__":
    rename_pdfs()
