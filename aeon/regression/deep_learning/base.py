"""
Abstract base class for the Keras neural network regressors.

The reason for this class between BaseClassifier and deep_learning classifiers is
because we can generalise tags and _predict
"""

from __future__ import annotations

__maintainer__ = []
__all__ = ["BaseDeepRegressor"]

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import numpy as np

from aeon.regression.base import BaseRegressor

if TYPE_CHECKING:
    import tensorflow as tf
    from tensorflow.keras.callbacks import Callback


class BaseDeepRegressor(BaseRegressor):
    """Abstract base class for deep learning time series regression.

    The base classifier provides a deep learning default method for
    _predict, and provides a new abstract method for building a
    model.

    Parameters
    ----------
    batch_size : int, default = 40
        training batch size for the model
    last_file_name      : str, default = "last_model"
        The name of the file of the last model, used
        only if save_last_model_to_file is used
    """

    _tags = {
        "X_inner_type": "numpy3D",
        "capability:multivariate": True,
        "algorithm_type": "deeplearning",
        "non_deterministic": True,
        "cant_pickle": True,
        "python_dependencies": "tensorflow",
    }

    @abstractmethod
    def __init__(self, batch_size: int = 40, last_file_name: str = "last_model"):
        self.batch_size = batch_size
        self.last_file_name = last_file_name

        self.model_ = None

        super().__init__()

    @abstractmethod
    def build_model(self, input_shape: tuple[int, ...]) -> tf.keras.Model:
        """
        Construct a compiled, un-trained, keras model that is ready for training.

        Parameters
        ----------
        input_shape : tuple
            The shape of the data fed into the input layer

        Returns
        -------
        A compiled Keras Model
        """
        ...

    def summary(self) -> dict[str, Any] | None:
        """
        Summary function to return the losses/metrics for model fit.

        Returns
        -------
        history: dict or None,
            Dictionary containing model's train/validation losses and metrics

        """
        return self.history.history if self.history is not None else None

    def _predict(self, X: np.ndarray) -> np.ndarray:
        """
        Find regression estimate for all cases in X.

        Parameters
        ----------
        X : an np.ndarray of shape = (n_cases, n_channels, n_timepoints)
            The training input samples.

        Returns
        -------
        predictions : 1d numpy array
            array of predictions of each instance
        """
        X = X.transpose((0, 2, 1))
        y_pred = self.model_.predict(X, self.batch_size)
        y_pred = np.squeeze(y_pred, axis=-1)
        return y_pred

    def save_last_model_to_file(self, file_path: str = "./") -> None:
        """Save the last epoch of the trained deep learning model.

        Parameters
        ----------
        file_path : str, default = "./"
            The directory where the model will be saved

        Returns
        -------
        None
        """
        self.model_.save(file_path + self.last_file_name + ".keras")

    def load_model(self, model_path: str) -> None:
        """Load a pre-trained keras model instead of fitting.

        When calling this function, all functionalities can be used
        such as predict etc. with the loaded model.

        Parameters
        ----------
        model_path : str (path including model name and extension)
            The directory where the model will be saved including the model
            name with a ".keras" extension.
            Example: model_path="path/to/file/best_model.keras"

        Returns
        -------
        None
        """
        import tensorflow as tf

        self.model_ = tf.keras.models.load_model(model_path)
        self.is_fitted = True

    def _get_model_checkpoint_callback(
        self, callbacks: Callback | list[Callback], file_path: str, file_name: str
    ) -> list[Callback]:
        import tensorflow as tf

        model_checkpoint_ = tf.keras.callbacks.ModelCheckpoint(
            filepath=file_path + file_name + ".keras",
            monitor="loss",
            save_best_only=True,
        )

        if isinstance(callbacks, list):
            return callbacks + [model_checkpoint_]
        else:
            return [callbacks] + [model_checkpoint_]
