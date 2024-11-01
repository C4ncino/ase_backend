import json
import pandas as pd
import numpy as np


def generate_random(quantity=20) -> np.ndarray:
    samples = []

    for _ in range(quantity):
        random_size = np.random.randint(54, 65)

        first_five = np.random.randint(0, 6, size=(random_size, 5))

        last_three = np.random.uniform(-9.99, 10.0, size=(random_size, 3))
        last_three = np.round(last_three, 2)

        samples.append(np.concatenate((first_five, last_three), axis=1).tolist())

    return samples


a = generate_random()

for i in a:
    print(i)

# a = []
b = [1] * 20

print(b)


c = generate_random(10)

# with open(r'C:\VScode\ase_backend\test\prueba.json') as f:
#     json_data = json.load(f)

#     for i in json_data:
#         a.append(pd.DataFrame(i).values)
