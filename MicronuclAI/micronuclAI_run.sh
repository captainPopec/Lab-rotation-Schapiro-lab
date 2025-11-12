#!/bin/sh
#SBATCH --partition=cpu-single
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=12gb
#SBATCH --job-name=MicronuclAI_metastasis
#SBATCH --output=metastaze-%j.out
#SBATCH --export=NONE

module load system/singularity/3.11.3
module load devel/java_jdk/1.18

## Define paths
main_project_dir=/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI

# Create a descriptive output folder name
cd $main_project_dir

#run MicronuclAI
nextflow run SchapiroLabor/micronuclAI_nf \
	-profile singularity \
	-r "dev" \
	-c config_micronuclAI.yml \
	--input sampleshit_main.csv \
	--skip_segmentation true \
	--extract_channel true \
	--dapi_index 0 \
	--outdir $main_project_dir/results_6_55 \
	-params-file params_micronuclAI.yaml \
	-resume 
