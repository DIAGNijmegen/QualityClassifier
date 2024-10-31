import random
from getting_data.exclusion_lists.procanceri_inclusion_lists import inclusion_list_picai_v1 as inclusion_list
from getting_data.utils.utils import load_seed, save_elements_to_json


def pick_random_elements(input_list, num_elements, seed_file):
    seed = load_seed(seed_file)
    random.seed(seed)
    return random.sample(input_list, num_elements)


if __name__ == '__main__':

    selected_elements = pick_random_elements(inclusion_list, 900,
                                             'getting_data/utils/seed/seed.txt')  # 20% of the inclusion list
    save_elements_to_json(selected_elements, 'procanceri_val_set.json')


