"""Tests for STRAY outlier estimator."""

__maintainer__ = []

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from aeon.anomaly_detection.series.outlier_detection import STRAY


def test_default_1D():
    """Test with default parameters and 1D input array."""
    X = np.array(
        [
            -7.207066,
            -5.722571,
            -4.915559,
            -8.345698,
            -5.570875,
            -5.493944,
            -6.574740,
            -6.546632,
            -6.564452,
            -6.890038,
            -6.477193,
            -6.998386,
            -6.776254,
            -5.935541,
            -5.040506,
            0.000000,
            5.889715,
            5.488990,
            5.088805,
            5.162828,
            8.415835,
            6.134088,
            5.509314,
            5.559452,
            6.459589,
            5.306280,
            4.551795,
            6.574756,
            4.976344,
            5.984862,
            5.064051,
            7.102298,
        ]
    )

    y_expected = np.array(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]
    )

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X.reshape(-1, 1))
    model = STRAY()
    y_actual = model.fit_predict(X, axis=0)
    assert np.allclose(y_actual, y_expected)


def test_default_2D():
    """Test with default parameters and 2D input array."""
    X = np.array(
        [
            [-1.207, -0.776, -0.694],
            [0.277, 0.064, -1.448],
            [1.084, 0.959, 0.575],
            [-2.346, -0.11, -1.024],
            [0.429, -0.511, -0.015],
            [0.506, -0.911, -0.936],
            [-0.575, -0.837, 1.102],
            [-0.547, 2.416, -0.476],
            [-0.564, 0.134, -0.709],
            [-0.89, -0.491, -0.501],
            [-0.477, -0.441, -1.629],
            [-0.998, 0.46, -1.168],
            [10.0, 12.0, 10.0],
            [3.0, 7.0, 10.0],
        ]
    )

    y_expected = np.array(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
        ]
    )

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    model = STRAY()
    y_actual = model.fit_predict(X, axis=0)
    assert np.allclose(y_actual, y_expected)


def test_1D_bool_with_na():
    """Test anomaly detection with 1D input array with missing values."""
    X = np.array(
        [
            np.nan,
            -5.72257076,
            -4.91555882,
            -8.3456977,
            -5.57087531,
            0.0,
            6.50605589,
            5.42526004,
            5.45336814,
            5.435548,
            5.10996217,
        ]
    )

    y_expected = np.array(
        [False, False, True, False, True, True, False, False, False, False, False]
    )

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X.reshape(-1, 1))
    model = STRAY(k=3)
    y_actual = model.fit_predict(X, axis=0)
    assert np.allclose(y_actual, y_expected)


def test_2D_bool_with_na():
    """Test anomaly detection with 2D input array with missing values."""
    X = np.array(
        [
            [-1.20706575, -0.57473996],
            [0.27742924, -0.54663186],
            [1.08444118, np.nan],
            [-2.3456977, -0.89003783],
            [0.42912469, -0.4771927],
            [0.50605589, -0.99838644],
        ]
    )

    y_expected = np.array([False, False, False, True, True, True])

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    model = STRAY(k=2, size_threshold=4)
    y_actual = model.fit_predict(X, axis=0)
    assert np.allclose(y_actual, y_expected)
