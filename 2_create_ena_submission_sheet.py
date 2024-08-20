import os
import csv
import sys




def usage():
    """
    Print usage information for the script.
    """
    print("""
    Usage: python 2_create_ena_submission_sheet.py path/to/sample_accession_output.csv path/to/trimmed/read/dir path/to/output_dir/output.tsv

    <input_csv_file>: Path to the input.tsv generated via ENA sample registration (containing sample accession numbers)
    <directory_path>: Path to the directory containing subdirectories with fastq files.
    <output_tsv_file>: Path to the output.tsv for input into ena-bulk-webincli tool.
    """)





def populate_csv(input_csv, output_tsv, directory_path):

#Set column headers for output.tsv (required by ena-bulk-webincli)
    output_headers = [
        "study_accession", "sample_accession", "experiment_name", "sequencing_platform",
        "sequencing_instrument", "library_name", "library_source", "library_selection",
        "library_strategy", "library_description", "insert_size", "uploaded file 1", "uploaded file 2"
    ]

#Set constant values for some columns
    study_accession = "PRJEB78703"
    experiment_name = "Biodiversity Genomics Europe"
    sequencing_platform = "ILLUMINA"
    sequencing_instrument = "Illumina NovaSeq X"
    library_source = "GENOMIC"
    library_strategy = "WGS"
    library_selection = "RANDOM"
    library_description = "Museum voucher specimen"

#Read and process input.csv
    with open(input_csv, newline='') as infile:
        reader = csv.DictReader(infile)
        input_headers = reader.fieldnames
#        print("Found columns:", input_headers)  
        input_data = [row for row in reader]

#get relevant data from input.csv
    output_data = []
    for row in input_data:
        library_name = row['title']
        sample_accession = row['id']
        insert_size = ""  #Insert_size is optional and so will leave empty

#Get trimmed_read.fastq paths
        uploaded_file_1 = ""
        uploaded_file_2 = ""

        for file in os.listdir(directory_path):
            if library_name in file:
                if "_R1_" in file:
                    uploaded_file_1 = os.path.abspath(os.path.join(directory_path, file))
                elif "_R2_" in file:
                    uploaded_file_2 = os.path.abspath(os.path.join(directory_path, file))

#Append values to output.tsv
        output_data.append({
            "study_accession": study_accession,
            "sample_accession": sample_accession,
            "experiment_name": experiment_name,
            "sequencing_platform": sequencing_platform,
            "sequencing_instrument": sequencing_instrument,
            "library_name": library_name,
            "library_source": library_source,
            "library_selection": library_selection,
            "library_strategy": library_strategy,
            "library_description": library_description,
            "insert_size": insert_size,
            "uploaded file 1": uploaded_file_1,
            "uploaded file 2": uploaded_file_2
        })

#Write to output.tsv
    with open(output_tsv, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_headers, delimiter='\t')
        writer.writeheader()
        writer.writerows(output_data)





if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)

    input_csv_file = sys.argv[1]
    directory_path = sys.argv[2]
    output_tsv_file = sys.argv[3]

    if not os.path.exists(input_csv_file):
        print(f"Error: The file '{input_csv_file}' does not exist.")
        usage()
        sys.exit(1)

    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        usage()
        sys.exit(1)

    populate_csv(input_csv_file, output_tsv_file, directory_path)
    print(f"Output TSV file has been created at '{output_tsv_file}'.")
