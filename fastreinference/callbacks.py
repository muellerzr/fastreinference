# AUTOGENERATED! DO NOT EDIT! File to edit: 00_callbacks.ipynb (unless otherwise specified).

__all__ = ['InferenceCallback']

# Cell
from abc import ABC, abstractmethod

# Cell
class InferenceCallback(ABC):
    """
    The foundational class for customizing behaviors during inference.

    There are three methods available that must be implemented:
      - `after_drawn_batch`
      - `gather_predictions`
      - `decoding_values`

    If an implementation should stay to its default behavior, do the following:
      - `event_name(self, *args): return super().event_name(*args)`

    Where `event_name` is any of the three events listed above
    """
    @abstractmethod
    def after_drawn_batch(self, batch):
        """
        Called immediatly after a batch has been drawn from the `DataLoader`.
        Any final adjustments to the batch before being sent to the model should be done here.

        Default implementation is to return `batch`.
        """
        return batch

    @abstractmethod
    def gather_predictions(self, model, batch):
        """
        Performs inference with `model` on `batch`.
        Any specific inference decorators such as `no_grad` or `inference_mode` is done in `Performer`.

        Default implementation is `model(*batch)`.
        """
        return model(*batch)

    @abstractmethod
    def decoding_values(self, values):
        """
        Called after predictions have been gathered on a `batch`.
        Any specific class decoding and final datatype preparation should be done here.

        Default implementation is to return `values`.
        """
        return values