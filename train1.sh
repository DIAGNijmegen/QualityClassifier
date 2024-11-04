#!/bin/bash

# Define default values
DATA_PATH="../data"
TASK_ID=1  # Replace with your default task ID
NUM_CPUS=4  # Set the number of CPUs you want to use
FOLD='1'
NETWORK='3d_fullres'
TRAINER='ClassifierTrainer'

# Check if the raw directory exists
if ! [ -d "$DATA_PATH/raw" ]; then
  echo "Please make sure that $DATA_PATH/raw/ exists"
  exit
fi

# Create preprocessed directory if it doesn't exist
mkdir -p "$DATA_PATH/preprocessed"

# Export required environment variables
export nnUNet_raw_data_base="$DATA_PATH/raw"
export nnUNet_preprocessed="$DATA_PATH/preprocessed"
export RESULTS_FOLDER="$DATA_PATH/trained_models"

# Run the preprocessing script with the specified task ID and CPU settings
echo running "python3 -u uc_train.py $NETWORK $TRAINER $TASK_ID $FOLD"
python3 -u uc_train.py $NETWORK $TRAINER $TASK_ID $FOLD