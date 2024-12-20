#!/bin/bash

# Define default values
DATA_PATH="../data"
TASK_ID=1  # Replace with your default task ID
NUM_CPUS=8  # Set the number of CPUs you want to use

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
echo running "python3 -u uc_plan_and_preprocess.py -t $TASK_ID -tf $NUM_CPUS -tl $NUM_CPUS"
python3 -u uc_plan_and_preprocess.py -t $TASK_ID -tf $NUM_CPUS -tl $NUM_CPUS