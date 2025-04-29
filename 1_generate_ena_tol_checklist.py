#!/usr/bin/env python3
"""
ENA Sample Sheet Generator for Tree of Life Project

This script converts input CSV files containing specimen data into properly formatted TSV files
that comply with the European Nucleotide Archive (ENA) sample checklist format (ERC000053).
It only processes entries that have corresponding sequencing files in the specified directory.

The script handles the following operations:
1. Reads specimen data from an input CSV file
2. Checks for matching sequencing files in the specified directory
3. Transforms the data to match ENA's required format
4. Adds necessary headers and unit specifications
5. Writes the formatted data to a tab-separated (TSV) output file
6. Generates a detailed log file of the processing

Required Input CSV Fields:
- species: Scientific name of the specimen
- genus: Genus name (used when species is 'not collected')
- Process ID: BOLD Process ID for the specimen
- organism_part: Type of tissue/material sampled
- lifestage: Life stage of the specimen when collected
- collected_by: Name of collector
- collection_date: Date when specimen was collected
- geographic_location: Country or sea where specimen was collected
- latitude: Decimal degrees
- longitude: Decimal degrees
- geographic_location_locality: Specific region and locality details
- identified_by: Name of identifier
- habitat: Habitat description
- sex: Sex of specimen
- collecting_institution: Institution that collected the specimen
- specimen_voucher: Voucher ID for the specimen

Output TSV Format:
- Includes ENA checklist identifier (ERC000053)
- Contains required field headers
- Specifies units where required (DD for latitude/longitude)
- Maps input fields to ENA-compliant format
- Handles missing data with 'not collected' placeholder

Usage:
    python 1_generate_ena_tol_checklist.py -i path/to/input.csv -d path/to/seq/files/dir -o path/to/output.tsv

Arguments:
    -i, --input: Path to input CSV file (sample_metadata.csv)
    -d, --directory: Path to directory containing sequencing files
    -o, --output: Path to output TSV file (Tree of Life ENA checklist)

Notes:
    - The script assumes input CSV uses ',' as delimiter
    - Output TSV uses tab as delimiter
    - Missing or empty fields are populated with 'not collected'
    - TAXID field is currently left empty
    - Geographic coordinates must be in decimal degrees
    - Part of the Biodiversity Genomics Europe project

Dependencies:
    - Python 3.6+
    - csv module
    - pathlib module
    - argparse module
"""

import csv
import sys
import argparse
from pathlib import Path
import re
import logging
from datetime import datetime

def setup_logging(output_dir):
    # Create log filename based on timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = output_dir / f'ena_tol_checklist_generator_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file

def get_process_ids_from_directory(directory_path):
    process_ids = set()
    pattern = r'([A-Z0-9]+-\d+)'  # Updated pattern to include numbers in the prefix
    
    # Log the directory contents first
    logging.info(f"Scanning directory: {directory_path}")
    files = list(directory_path.glob('*'))
    logging.info(f"Total files found in directory: {len(files)}")
    
    # Log first few files to see what we're working with
    for file_path in files[:5]:
        logging.info(f"Example file: {file_path.name}")
    
    for file_path in directory_path.glob('*'):
        filename = file_path.name
        match = re.search(pattern, filename)
        
        # Debug output for pattern matching
        logging.debug(f"Processing file: {filename}")
        if match:
            process_id = match.group(1)
            # Print the exact match we found
            logging.info(f"Found match: '{process_id}' in file: {filename}")
            process_ids.add(process_id)
    
    logging.info(f"Found {len(process_ids)} unique Process IDs in directory")
    if process_ids:
        logging.info("Process IDs found:")
        for pid in sorted(process_ids):
            logging.info(f"- {pid}")
    else:
        logging.warning("No Process IDs found in any files!")
    
    return process_ids

def populate_ena_sample_sheet(input_file, directory_path, output_file):
    # Get Process IDs from directory
    valid_process_ids = get_process_ids_from_directory(Path(directory_path))
    
    fieldnames = [
        'taxid', 'scientific_name', 'sample_alias', 'sample_title', 'sample_description',
        'organism part', 'lifestage', 'project name', 'identified_by', 'collected_by', 
        'collection date', 'geographic location (country and/or sea)', 
        'geographic location (latitude)', 'geographic location (longitude)',
        'geographic location (region and locality)', 'habitat', 'sex',
        'collecting institution', 'specimen_voucher'
    ]

    processed_ids = []
    skipped_ids = []

    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')

            # Write header rows
            writer.writerow(['Checklist', 'ERC000053', 'Tree of Life Checklist'])
            writer.writerow(fieldnames)
            units_row = ['#units'] + [''] * 11 + ['DD', 'DD'] + [''] * 6
            writer.writerow(units_row)

            dict_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')

            for row in reader:
                process_id = row.get('Process ID', '').strip()
                
                # Skip if Process ID doesn't match any files in directory
                if process_id not in valid_process_ids:
                    skipped_ids.append(process_id)
                    continue
                
                # Handle scientific name based on species and genus information
                species_value = row.get('species', 'not collected')
                if species_value == 'not collected' and row.get('genus'):
                    scientific_name = f"{row['genus']} sp."
                else:
                    scientific_name = species_value

                # Set output file column headers
                output_row = {
                    'taxid': '',
                    'scientific_name': scientific_name,
                    'sample_alias': f'BOLD Process ID: {process_id}',
                    'sample_title': process_id,
                    'sample_description': 'Museum voucher specimen',
                    'organism part': row.get('organism_part', 'not collected') if row.get('organism_part') else 'not collected',
                    'lifestage': row.get('lifestage', 'not collected') if row.get('lifestage') else 'not collected',
                    'project name': 'Biodiversity Genomics Europe',
                    'collected_by': row.get('collected_by', 'not collected') if row.get('collected_by') else 'not collected',
                    'collection date': row.get('collection_date', 'not collected') if row.get('collection_date') else 'not collected',
                    'geographic location (country and/or sea)': row.get('geographic_location', 'not collected') if row.get('geographic_location') else 'not collected',
                    'geographic location (latitude)': row.get('latitude', 'not collected') if row.get('latitude') else 'not collected',
                    'geographic location (longitude)': row.get('longitude', 'not collected') if row.get('longitude') else 'not collected',
                    'geographic location (region and locality)': row.get('geographic_location_locality', 'not collected') if row.get('geographic_location_locality') else 'not collected',
                    'identified_by': row.get('identified_by', 'not collected') if row.get('identified_by') else 'not collected',
                    'habitat': row.get('habitat', 'not collected') if row.get('habitat') else 'not collected',
                    'sex': row.get('sex', 'not collected') if row.get('sex') else 'not collected',
                    'collecting institution': row.get('collecting_institution', 'not collected') if row.get('collecting_institution') else 'not collected',
                    'specimen_voucher': row.get('specimen_voucher', 'not collected') if row.get('specimen_voucher') else 'not collected'
                }

                dict_writer.writerow(output_row)
                processed_ids.append(process_id)

    # Log processing summary
    logging.info("Processing Summary:")
    logging.info(f"Total entries processed: {len(processed_ids)}")
    logging.info(f"Total entries skipped: {len(skipped_ids)}")
    
    # Log processed IDs
    logging.info("\nProcessed Process IDs:")
    for pid in sorted(processed_ids):
        logging.info(f"- {pid}")
    
    # Log skipped IDs if any
    if skipped_ids:
        logging.info("\nSkipped Process IDs (no matching files found):")
        for pid in sorted(skipped_ids):
            logging.info(f"- {pid}")
    
    logging.info(f"\nOutput written to: {output_file}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert specimen data to ENA sample sheet format.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to input CSV file (sample_metadata.csv)'
    )
    
    parser.add_argument(
        '-d', '--directory',
        required=True,
        help='Path to directory containing sequencing files'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Path to output TSV file (Tree of Life ENA checklist)'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Convert paths to Path objects
    input_path = Path(args.input)
    directory_path = Path(args.directory)
    output_path = Path(args.output)
    
    # Validate input file exists
    if not input_path.exists():
        print(f"Error: The input file {args.input} does not exist.")
        sys.exit(1)
    
    # Validate directory exists
    if not directory_path.exists():
        print(f"Error: The directory {args.directory} does not exist.")
        sys.exit(1)
    
    # Validate directory is actually a directory
    if not directory_path.is_dir():
        print(f"Error: {args.directory} is not a directory.")
        sys.exit(1)
    
    # Setup logging (log file will be in same directory as output file)
    log_file = setup_logging(output_path.parent)
    logging.info(f"Starting ENA Sample Sheet Generator")
    logging.info(f"Input file: {input_path}")
    logging.info(f"Directory: {directory_path}")
    logging.info(f"Output file: {output_path}")
    
    # Process the files
    populate_ena_sample_sheet(input_path, directory_path, output_path)
    
    logging.info(f"Log file written to: {log_file}")
