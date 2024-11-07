#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --qos=low
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=30G
#SBATCH --time=3-00:00:00
#SBATCH --no-container-remap-root
#SBATCH --container-mounts=/data/pelvis/projects/tiago/DWI_IQA/validation_procanceri_100:/dataset:ro,/data/pelvis/projects/tiago/DWI_IQA/validation_procanceri_100/BDAV_Y:/results
#SBATCH --container-image="doduo1.umcn.nl#joeran/picai_bday_inference_docker_batched:v1.5"

python batch_inference.py \
    --t2w_input={patient_id}/{subject_id}_t2w.mha \
    --adc_input={patient_id}/{subject_id}_adc.mha \
    --hbv_input={patient_id}/{subject_id}_hbv.mha \
    --subject_list=/dataset/subject_list.txt
