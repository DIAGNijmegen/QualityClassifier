import os
import random


def generate_and_lock_seed(file_path='seed.txt'):
    if os.path.exists(file_path):
        print(f"Seed file '{file_path}' already exists.")
    else:
        # Generate and save a new seed
        seed = random.randint(0, 2 ** 32 - 1)
        with open(file_path, 'w') as f:
            f.write(str(seed))
        print(f"New seed generated and saved to '{file_path}': {seed}")

    # Make the file read-only
    os.chmod(file_path, 0o444)  # Read-only permission for all users


# Usage
generate_and_lock_seed()

