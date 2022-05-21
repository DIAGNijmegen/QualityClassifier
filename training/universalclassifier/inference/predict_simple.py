#    Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import torch
from universalclassifier.inference.predict import predict_from_folder
from nnunet.paths import network_training_output_dir
from batchgenerators.utilities.file_and_folder_operations import join, isdir
from nnunet.utilities.task_name_id_conversion import convert_id_to_task_name


def predict(args):
    input_folder = args.input_folder
    seg_folder = args.seg_folder
    output_folder = args.output_folder
    folds = args.folds
    overwrite_existing = args.overwrite_existing
    model = args.model
    trainer_class_name = args.trainer_class_name

    task_name = args.task_name

    if not task_name.startswith("Task"):
        task_id = int(task_name)
        task_name = convert_id_to_task_name(task_id)

    assert model in ["3d_fullres"], "-m must be 3d_fullres"

    if isinstance(folds, list):
        if folds[0] == 'all' and len(folds) == 1:
            pass
        else:
            folds = [int(i) for i in folds]
    elif folds == "None":
        folds = None
    else:
        raise ValueError("Unexpected value for argument folds")

    trainer = trainer_class_name

    model_folder_name = join(network_training_output_dir, model, task_name, trainer + "__" +
                             args.plans_identifier)
    print("using model stored in ", model_folder_name)
    assert isdir(model_folder_name), "model output folder not found. Expected: %s" % model_folder_name

    predict_from_folder(model_folder_name, input_folder, seg_folder, output_folder, folds,
                        mixed_precision=not args.disable_mixed_precision, overwrite_existing=overwrite_existing,
                        checkpoint_name=args.chk)
