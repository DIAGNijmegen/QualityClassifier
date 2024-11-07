import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# paths
marksheet_path = Path('/Volumes/pelvis/projects/tiago/DWI_IQA/QualityClassifier/getting_data/10_get_patientlevel_info/markseets/proci_val_100.csv')
clinical_information_output_dir = Path('/Volumes/pelvis/projects/tiago/DWI_IQA/validation_procanceri_100/clinical_information_v2')

clinical_information_output_dir.mkdir(parents=True, exist_ok=True)
marksheet = pd.read_csv(marksheet_path)

for i, row in tqdm(marksheet.iterrows(), total=len(marksheet)):
    clinical_information = {
        "patient_age": row.patient_age,
        "PSA_report": row.psa,
        "PSAD_report": row.psad,
        "prostate_volume_report": row.prostate_volume,
        "scanner_manufacturer": row.scanner_manufacturer,
        "scanner_model_name": row.scanner_model,
        "diffusion_high_bvalue": None,
    }

    # save clinical information
    clinical_information_path = clinical_information_output_dir / f"{row.patient_id}_{row.study_id}.json"
    with open(clinical_information_path, "w") as fp:
        json.dump(clinical_information, fp)