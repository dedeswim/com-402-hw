from hw7_ex1 import query_pred
import numpy as np
from tqdm import tqdm
from phe import paillier
from typing import Callable, List

N_PARAMS = 10


def steal(n_params: int, query_function: Callable[[List[float]], float]) -> np.ndarray:
    params = np.zeros(n_params)

    bias_input = np.zeros_like(params)
    bias = query_function(bias_input)

    for i in tqdm(range(n_params)):
        input_vector = np.zeros_like(params)
        input_vector[i] = 1
        response = query_function(input_vector) - bias
        params[i] = response

    return bias, params


def main():
    bias, params = steal(N_PARAMS, query_pred)

    test_input = np.random.rand(N_PARAMS)

    true_prediction = query_pred(test_input)

    clone_prediction = test_input @ params + bias

    print(f'True prediction = {true_prediction}')
    print(f'Clone prediction = {clone_prediction}')
    print(f'Difference = {true_prediction - clone_prediction}')

    assert 2**(-16) > abs(true_prediction - clone_prediction)

    print('Successfully stealed the model')
    print(f'Parameters:')
    [print(param) for param in params]
    print(f'Bias: {bias}')


if __name__ == '__main__':
    main()
