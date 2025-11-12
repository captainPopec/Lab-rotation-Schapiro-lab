#!/bin/sh
#SBATCH --partition=cpu-single
#SBATCH --ntasks=1
#SBATCH --time=08:00:00
#SBATCH --mem=12gb
#SBATCH --job-name=Melanoma_Brain_Metastasis_Segmentation
#SBATCH --output=ny_metastasis-%j.out
#SBATCH --export=NONE

module load system/singularity/3.11.3
module load devel/java_jdk/1.18

## Define paths
main_project_dir=/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/segmentation_input
singluarity_cache=/home/hd/hd_hd/hd_vh340/singularity_cachedir 
orig_tif_dir=/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/input_tifs
registr_dir=$main_project_dir/registration

cd $orig_tif_dir

for FILE in *.tif
do
	## Parse the input filename
	new_filename="${FILE//[/}"
	new_filename="${new_filename//]/}"
	new_filename="${new_filename//,/-}"
	new_filename="${new_filename//_component_data/}"
	new_filename="${new_filename%.tif}" # remove trailing '.tif'

       	if [ ! -f "$registr_dir/${new_filename}.ome.tif" ]; then
                echo "File $new_filename does not exist in Registration directory. Proceeding with conversion."
		bfconvert "$FILE" "$registr_dir/${new_filename}.ome.tif"
        else
                echo "File $new_filename already exists in MCMICRO output directory. Skipping conversion."
                continue
        fi
	
done  

cd $main_project_dir
## run MCMICRO
NXF_VER=24.04.2 nextflow run labsyspharm/mcmicro -r "ac3b267e31eecad0d189400be790f056501cdbf6" -c config.yml -profile singularity --in $main_project_dir --params params.yaml --start-at segmentation --stop-at quantification -with-report report.html


