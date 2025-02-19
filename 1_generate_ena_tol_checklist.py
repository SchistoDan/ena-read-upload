#!/usr/bin/env python3
"""
ENA Sample Sheet Generator for Tree of Life Project

This script converts input CSV files containing specimen data into properly formatted TSV files
that comply with the European Nucleotide Archive (ENA) sample checklist format (ERC000053).

The script handles the following operations:
1. Reads specimen data from an input CSV file
2. Transforms the data to match ENA's required format
3. Adds necessary headers and unit specifications
4. Writes the formatted data to a tab-separated (TSV) output file

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
    python populate_tsv.py -i path/to/input.csv -o path/to/output.tsv

Arguments:
    -i, --input: Path to input CSV file (sample2taxid_out.csv)
    -o, --output: Path to output TSV file (Tree of Life ENA checklist)

Example:
    python 1_generate_ena_tol_checklist.py -i sample_metadata.csv -o ena_checklist.tsv

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

def populate_ena_sample_sheet(input_file, output_file):
    fieldnames = [
        'taxid', 'scientific_name', 'sample_alias', 'sample_title', 'sample_description',
        'organism part', 'lifestage', 'project name', 'identified_by', 'collected_by', 
        'collection date', 'geographic location (country and/or sea)', 
        'geographic location (latitude)', 'geographic location (longitude)',
        'geographic location (region and locality)', 'habitat', 'sex',
        'collecting institution', 'specimen_voucher'
    ]

    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')

            writer.writerow(['Checklist', 'ERC000053', 'Tree of Life Checklist'])
            writer.writerow(fieldnames)
            units_row = ['#units'] + [''] * 11 + ['DD', 'DD'] + [''] * 6
            writer.writerow(units_row)

            dict_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')

            for row in reader:
                # Handle scientific name based on species and genus information
                species_value = row.get('species', 'not collected')
                if species_value == 'not collected' and row.get('genus'):
                    scientific_name = f"{row['genus']} sp."
                else:
                    scientific_name = species_value

                output_row = {
                    'taxid': '',
                    'scientific_name': scientific_name,
                    'sample_alias': f'BOLD Process ID: {row.get("Process ID", "not collected")}',
                    'sample_title': row.get('Process ID', 'not collected'),
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

    print(f"Data has been processed and written to {output_file}.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert specimen data to ENA sample sheet format.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to input CSV file (sample2taxid_out.csv)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Path to output TSV file (Tree of Life ENA checklist)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    if not Path(args.input).exists():
        print(f"Error: The input file {args.input} does not exist.")
        sys.exit(1)
    
    populate_ena_sample_sheet(args.input, args.output)
