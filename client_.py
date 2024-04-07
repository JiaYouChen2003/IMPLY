import math


def generate_dict_with_ones(i):
    data = {
        'LH_U': (0, 0, 0),
        'LH_D': (0, 0, 0),
        'RH_U': (1, 0, -1),
        'RH_D': (1, 0, -1),
        'LF_U': (0, 1, -1),
        'LF_D': (0, 0, -1),
        'RF_U': (0, -1, -1),
        'RF_D': (-1, 0, 0),
        'HEAD': (0, 0, 0)}
    data = normalize_data(data)
    return data


def normalize_data(data):
    normalized_data = {}
    for key, value in data.items():
        magnitude = math.sqrt(sum(x ** 2 for x in value))
        normalized_vector = tuple(x / magnitude for x in value) if magnitude != 0 else value
        normalized_data[key] = normalized_vector
        
        if key in factors:
            scaled_vector = tuple(factors[key] * x for x in normalized_vector)
            normalized_data[key] = scaled_vector
    return normalized_data


factors = {
    'LH_U': 0.75,
    'LH_D': 1.5,
    'RH_U': 0.75,
    'RH_D': 1.5,
    'LF_U': 3.5,
    'LF_D': 1.75,
    'RF_U': 3.5,
    'RF_D': 1.75,
    'HEAD': 1
}
