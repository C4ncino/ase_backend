from .validate import inspect_movement, inspect_fingers, get_centroid
from .train import prepare_data
from .models import get_model
from .metrics import calculate_metrics, compare_metrics
from .save import save_model_as_tensorflowjs

MODEL_POOL = {
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

__all__ = [
    'inspect_movement',
    'inspect_fingers',
    'get_centroid',
    'MODEL_POOL',
    'calculate_metrics',
    'prepare_data',
    'compare_metrics'
]
