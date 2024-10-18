import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def prepare_data(sensor_data: list[dict]):
    n_samples = len(data)

    data = np.array([pd.DataFrame(i).values for i in sensor_data])
    labels = np.array([1]*n_samples)

    # TODO: tomar muestras de los demás modelos de la bd del usuario en caso de que haya
    # Añadir los datos en los mismos arrays de labels y data

    x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2)
    
    return x_train, x_val, y_train, y_val
