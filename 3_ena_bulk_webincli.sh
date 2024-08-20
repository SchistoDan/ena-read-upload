#!/bin/bash
#SBATCH --job-name=bulk_webincli
#SBATCH --partition=hour
#SBATCH --output=%x.out
#SBATCH --mem-per-cpu=5G
#SBATCH --cpus-per-task=8
#SBATCH --error=%x.err


#requires ena_bulk_webincli and dependencies to be installed in conda env
source ~/miniconda3/etc/profile.d/conda.sh
conda init bash
conda activate bulk_webin




#VARIABLES
	#-s INPUT_SPREADSHEET can be tab-separated .txt, .csv, .xlsx/.xls or .tsv
	#-pc = parallel cores (between 1 and 10).
	#-m = submit/validate
	#-t = ENA test services
	#-g = genetic context (reads, sequence, genome, transcriptome, taxrefset)



#PATHS
ENA_BULK_WEBINCLI=/gpfs/nhmfsa/bulk/share/data/mbl/share/workspaces/groups/genomics-collections/software/ena-bulk-webincli

INPUT_SHEET=/gpfs/nhmfsa/bulk/share/data/mbl/share/workspaces/groups/genomics-collections/BGE/BGE_scripts/ena_upload/Create_ena_submission_sheet-OUT.tsv





python "$ENA_BULK_WEBINCLI"/bulk_webincli.py \
	-u Webin-XXXXX -p XXXXX \
	-g reads -s $INPUT_SHEET \
	-m validate -pc 8




