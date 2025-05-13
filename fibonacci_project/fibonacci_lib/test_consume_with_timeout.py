import pytest
from unittest.mock import patch
from fibonacci_lib.consume_with_timeout import ConsumeWithTimeout


def test_empty_iterator() -> None:
    data = iter([])

    with patch('time.time') as mock_time, patch('time.sleep'):
        mock_time.side_effect = [0]
        consumer = ConsumeWithTimeout(data, timeout_seconds=5, delay=0.1)
        result = list(consumer)

    assert result == []
    assert consumer.total == 0
    assert consumer.count == 0


def test_large_delay_but_small_timeout() -> None:
    data = iter([1, 2, 3])

    with patch('time.time') as mock_time, patch('time.sleep'):
        mock_time.side_effect = [0, 0.1, 2.5]
        consumer = ConsumeWithTimeout(data, timeout_seconds=2, delay=2)
        result = list(consumer)

    assert result == [1]
    assert consumer.total == 1
    assert consumer.count == 1


def test_iterator_with_zeros() -> None:
    data = iter([0, 0, 0])

    with patch('time.time') as mock_time, patch('time.sleep'):
        mock_time.side_effect = [0, 0.1, 0.2, 0.3, 1.0]
        consumer = ConsumeWithTimeout(data, timeout_seconds=2, delay=0.1)
        result = list(consumer)

    assert result == [0, 0, 0]
    assert consumer.total == 0
    assert consumer.count == 3


def test_timeout_exactly_reached() -> None:
    data = iter([1, 2])

    with patch('time.time') as mock_time, patch('time.sleep'):
        mock_time.side_effect = [0, 0.5, 1.0]
        consumer = ConsumeWithTimeout(data, timeout_seconds=1.0, delay=0.1)
        result = list(consumer)

    assert result == [1]
    assert consumer.count == 1


def test_stop_iteration_raised() -> None:
    data = iter([1])

    with patch('time.time') as mock_time, patch('time.sleep'):
        mock_time.side_effect = [0, 0.1, 0.2]
        consumer = ConsumeWithTimeout(data, timeout_seconds=2, delay=0.1)
        it = iter(consumer)

        current_value = next(it)
        assert current_value == 1

        with pytest.raises(StopIteration):
            next(it)
