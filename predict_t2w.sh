#!/bin/bash

# Define hardcoded arguments for the Python script
INPUT_FOLDER="../validation_picai_100"
DATA_PATH="../data_t2w"
OUTPUT_FOLDER="../validation_picai_100/T2WQual"
TASKID="Task001_ProstateQualityT2W"
FOLDS=0

if ! [ -d "$DATA_PATH/trained_models" ]; then
  echo "Please make sure that $DATA_PATH/trained_models/ exists"
  exit
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