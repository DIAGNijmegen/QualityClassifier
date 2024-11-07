#!/bin/bash


# Define hardcoded arguments for the Python script
DATA_PATH="../data_dwi"
INPUT_FOLDER="../data_dwi/raw/nnUnet_raw_data/Task001_ProstateQualityDWI/imagesTr"
OUTPUT_FOLDER="../data_dwi/raw/nnUnet_raw_data/Task001_ProstateQualityDWI/imagesTr/DWIQual"
TASKID="Task001_ProstateQualityDWI"

if ! [ -d "$DATA_PATH/trained_models" ]; then
  echo "Please make sure that $DATA_PATH/trained_models/ exists"
  exi
fi

export nnUNet_raw_data_base="$DATA_PATH/raw"
export nnUNet_preprocessed="$DATA_PATH/preprocessed"
export RESULTS_FOLDER="$DATA_PATH/trained_models"


# Run the Python script with the specified arguments
echo "Running python3 -u uc_predict.py with predefined arguments"
python3 -u uc_predict.py \
  -i $INPUT_FOLDER \
  -o $OUTPUT_FOLDER \
  -t $TASKID