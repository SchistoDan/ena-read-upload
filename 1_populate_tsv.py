import csv
import sys
from pathlib import Path



def populate_ena_sample_sheet(input_file, output_file):

#Define the field names for the data rows
    fieldnames = [
        'taxid', 'scientific_name', 'sample_alias', 'sample_title', 'sample_description',
        'organism part', 'lifestage', 'project name', 'identified_by', 'collected_by', 
        'collection date', 'geographic location (country and/or eea)', 
        'geographic location (latitude)', 'geographic location (longitude)',
        'geographic location (region and locality)', 'habitat', 'sex',
        'collecting institution', 'specimen_voucher'
    ]

    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')

#Write fixed headers
            writer.writerow(['Checklist', 'ERC000053', 'Tree of Life Checklist'])

#Write field headers
            writer.writerow(fieldnames)

#Write '#units' headers
            units_row = ['#units'] + [''] * 11 + ['DD', 'DD'] + [''] * 6
            writer.writerow(units_row)

            dict_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')


#Process each row in input.csv and populate rows in output.tsv
            for row in reader:
                output_row = {
                    'taxid': '',  #EMPTY COLUMN FOR TAXID AT THE MOMENT
                    'scientific_name': row.get('Species', 'not collected'),
                    'sample_alias': f'BOLD Process ID: {row.get("Process ID", "not collected")}',
                    'sample_title': row.get('Process ID', 'not collected'),
                    'sample_description': 'Museum voucher specimen',
                    'organism part': row.get('organism part', 'not collected') if row.get('organism part') else 'not collected',
                    'lifestage': row.get('lifestage', 'not collected') if row.get('lifestage') else 'not collected',
                    'project name': 'Biodiversity Genomics Europe',
                    'collected_by': row.get('collected_by', 'not collected') if row.get('collected_by') else 'not collected',
                    'collection date': row.get('collection date', 'not collected') if row.get('collection date') else 'not collected',
                    'geographic location (country and/or sea)': row.get('geographic_location', 'not collected') if row.get('geographic_location') else 'not collected',
                    'geographic location (latitude)': row.get('latitude', 'not collected') if row.get('latitude') else 'not collected',
                    'geographic location (longitude)': row.get('longitude', 'not collected') if row.get('longitude') else 'not collected',
                    'geographic location (region and locality)': row.get('geographic_location_locality', 'not collected') if row.get('geographic_location_locality') else 'not collected',
                    'identified_by': row.get('identified_by', 'not collected') if row.get('identified_by') else 'not collected',
                    'habitat': row.get('habitat', 'not collected') if row.get('habitat') else 'not collected',
                    'sex': row.get('sex', 'not collected') if row.get('sex') else 'not collected',
                    'collecting institution': row.get('collecting_institution', 'not collected') if row.get('collection_institution') else 'not collected',
                    'specimen_voucher': row.get('specimen_voucher', 'not collected') if row.get('specimen_voucher') else 'not collected'
                }

                dict_writer.writerow(output_row)

    print(f"Data has been processed and written to {output_file}.")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""
        Usage: python populate_tsv.py path/to/input.csv path/to/output.tsv
		input.csv = sample2taxid_out.csv
		output.tsv = Tree of Life ENA checklist for sample registration
        """)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: The input file {input_file} does not exist.")
        sys.exit(1)

    populate_ena_sample_sheet(input_file, output_file)
