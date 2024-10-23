from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score


def calculate_metrics(y_true, y_pred, y_pred_prob):
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='binary'),
        'recall': recall_score(y_true, y_pred, average='binary'),
        'f1_score': f1_score(y_true, y_pred, average='binary'),
        'roc_auc': roc_auc_score(y_true, y_pred_prob),
    }
    return metrics


def has_better_metrics(current_metrics, best_metrics):
    metrics = ['roc_auc', 'f1_score', 'precision', 'recall', 'accuracy']

    for metric in metrics:
        if current_metrics[metric] > best_metrics[metric]:
            return True
        elif current_metrics[metric] < best_metrics[metric]:
            break

    return False
