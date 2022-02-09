from openmc_plasma_source import FusionPointSource

import openmc
import pytest
import numpy as np


def test_creation():
    my_source = FusionPointSource()

    # Ensure it is of type openmc.Source
    assert isinstance(my_source, openmc.Source)

    # Ensure it has space, angle, and energy set
    assert isinstance(my_source.space, openmc.stats.Point)
    assert isinstance(my_source.angle, openmc.stats.Isotropic)
    assert isinstance(my_source.energy, openmc.stats.Muir)


@pytest.mark.parametrize(
    "coordinate", [(1.0, 2.0, 3.0), [4, 5, 6], np.linspace(1.0, 3.0, 3)]
)
def test_coordinate(coordinate):
    # Should allow any iterable of length 3 with contents convertible to float
    my_source = FusionPointSource(coordinate=coordinate)
    assert np.array_equal(my_source.coordinate, coordinate)


@pytest.mark.parametrize("coordinate", [(1, 2), [3, 4, 5, 6], 5, "abc"])
def test_bad_coordinate(coordinate):
    # Should reject iterables of length != 3, anything non iterable, and anything
    # that can't convert to float
    with pytest.raises(ValueError):
        FusionPointSource(coordinate=coordinate)


@pytest.mark.parametrize("temperature", [20000.0, 1e4, 0.1, 25000])
def test_temperature(temperature):
    # Should accept any positive float
    my_source = FusionPointSource(temperature=temperature)
    assert my_source.temperature == temperature


@pytest.mark.parametrize("temperature", [-20000.0, "hello world", [10000]])
def test_bad_temperature(temperature):
    # Should reject negative floats and anything that isn't convertible to float
    with pytest.raises(ValueError):
        FusionPointSource(temperature=temperature)


@pytest.mark.parametrize("fuel_type", ["DT", "DD"])
def test_fuel(fuel_type):
    # Should accept either 'DD' or 'DT'
    my_source = FusionPointSource(fuel_type=fuel_type)
    assert my_source.fuel_type == fuel_type


@pytest.mark.parametrize("fuel_type", ["топливо", 5])
def test_wrong_fuel(fuel_type):
    # Should reject fuel types besides those listed in fuel_types.py
    with pytest.raises(ValueError):
        FusionPointSource(fuel_type=fuel_type)
