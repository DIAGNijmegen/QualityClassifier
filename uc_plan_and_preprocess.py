from universalclassifier.experiment_planning import plan_and_preprocess


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task_id", type=int, default=1,
                        help="Integer belonging to the task ids you wish to run"
                             " experiment planning and preprocessing for. Each of these "
                             "ids must, have a matching folder 'TaskXXX_' in the raw "
                             "data folder")
    parser.add_argument("-pl3d", "--planner3d", type=str, default="ClassificationExperimentPlanner3D",
                        help="Name of the ExperimentPlanner class. Default is ClassificationExperimentPlanner3D.")
    parser.add_argument("-no_pp", action="store_true",
                        help="Set this flag if you dont want to run the preprocessing. If this is set then this script "
                             "will only run the experiment planning and create the plans file")
    parser.add_argument("-tl", type=int, required=False, default=8,
                        help="Number of processes used for preprocessing the low resolution data for the 3D low "
                             "resolution U-Net. This can be larger than -tf. Don't overdo it or you will run out of "
                             "RAM")
    parser.add_argument("-tf", type=int, required=False, default=8,
                        help="Number of processes used for preprocessing the full resolution data of the 2D U-Net and "
                             "3D U-Net. Don't overdo it or you will run out of RAM")
    parser.add_argument("--verify_dataset_integrity", required=False, default=False, action="store_true",
                        help="Not implmented yet for universal classifier. Set this flag to check the dataset "
                             "integrity. This is useful and should be done once for each dataset!")


    args = parser.parse_args()
    return args



if __name__ == "__main__":
    plan_and_preprocess.main(parse_args())
    print("Completed planning and preprocessing.")
