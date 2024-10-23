from .validate import inspect_movement, inspect_fingers, get_centroid
from .train import prepare_data
from .small_models import get_model
from .large_models import get_large_model
from .metrics import calculate_metrics, has_better_metrics
from .convert import convert_model_to_tfjs

SMALL_MODEL_POOL = {
    'L1': get_model('L1'),
    'L2': get_model('L2'),
    'L3': get_model('L3'),
    'L4': get_model('L4'),
    'L5': get_model('L5'),
    'G1': get_model('G1'),
    'G2': get_model('G2'),
    'G3': get_model('G3'),
    'G4': get_model('G4'),
    'G5': get_model('G5'),
}

LARGE_MODEL_POOL = [
    'L1',
]

__all__ = [
    'inspect_movement',
    'inspect_fingers',
    'get_centroid',
    'SMALL_MODEL_POOL',
    'LARGE_MODEL_POOL',
    'get_large_model',
    'calculate_metrics',
    'prepare_data',
    'has_better_metrics',
    'convert_model_to_tfjs',
]
