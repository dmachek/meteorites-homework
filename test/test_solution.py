import pytest
import requests

import solution


def test_fetch_meteorites(monkeypatch):
    expected_data = [
        {"name": "Test meteorite", "mass": "100"}
    ]

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return expected_data

    def fake_get(url, timeout):
        assert url == "https://example.com/data.json"
        assert timeout == (5, 30)
        return FakeResponse()

    monkeypatch.setattr(solution.requests, "get", fake_get)

    result = solution.fetch_meteorites(
        "https://example.com/data.json",
        (5, 30),
    )

    assert result == expected_data


def test_fetch_meteorites_rejects_non_list(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"error": "not a list"}

    monkeypatch.setattr(
        solution.requests,
        "get",
        lambda url, timeout: FakeResponse(),
    )

    with pytest.raises(
        ValueError,
        match="Expected JSON response to be a list",
    ):
        solution.fetch_meteorites(
            "https://example.com/data.json",
            (5, 30),
        )


def test_fetch_meteorites_invalid_json(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise requests.exceptions.JSONDecodeError(
                "Invalid JSON",
                "",
                0,
            )

    monkeypatch.setattr(
        solution.requests,
        "get",
        lambda url, timeout: FakeResponse(),
    )

    with pytest.raises(ValueError, match="Invalid JSON"):
        solution.fetch_meteorites(
            "https://example.com/data.json",
            (5, 30),
        )


def test_fetch_meteorites_network_error(monkeypatch):
    def fake_get(url, timeout):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(
        solution.requests,
        "get",
        fake_get,
    )

    with pytest.raises(requests.Timeout):
        solution.fetch_meteorites(
            "https://example.com/data.json",
            (5, 30),
        )


def test_find_largest_meteorite():
    data = [
        {"name": "Small", "mass": "9"},
        {"name": "Large", "mass": "100"},
        {"name": "Medium", "mass": "50"},
    ]

    result = solution.find_largest_meteorite(data)

    assert result["name"] == "Large"
    assert result["mass"] == "100"


def test_find_largest_ignores_invalid_masses():
    data = [
        {"name": "Missing"},
        {"name": "Empty", "mass": ""},
        {"name": "Invalid", "mass": "not-a-number"},
        {"name": "Valid", "mass": "100"},
    ]

    result = solution.find_largest_meteorite(data)

    assert result["name"] == "Valid"


def test_find_largest_raises_when_no_valid_mass():
    data = [
        {"name": "Missing"},
        {"name": "Empty", "mass": ""},
        {"name": "Invalid", "mass": "not-a-number"},
    ]

    with pytest.raises(
        ValueError,
        match="No valid meteorite masses found",
    ):
        solution.find_largest_meteorite(data)


def test_find_most_frequent_year():
    data = [
        {"year": "1979-01-01T00:00:00.000"},
        {"year": "1988-01-01T00:00:00.000"},
        {"year": "1979-01-01T00:00:00.000"},
        {"year": "2003-01-01T00:00:00.000"},
        {"year": "1979-01-01T00:00:00.000"},
    ]

    result = solution.find_most_frequent_year(data)

    assert result == (1979, 3)


def test_find_most_frequent_year_ignores_invalid_values():
    data = [
        {},
        {"year": None},
        {"year": ""},
        {"year": "invalid-date"},
        {"year": "2003-01-01T00:00:00.000"},
        {"year": "2003-01-01T00:00:00.000"},
    ]

    result = solution.find_most_frequent_year(data)

    assert result == (2003, 2)


def test_find_most_frequent_year_raises_when_no_valid_year():
    data = [
        {},
        {"year": None},
        {"year": "invalid-date"},
    ]

    with pytest.raises(
        ValueError,
        match="No valid meteorite years found",
    ):
        solution.find_most_frequent_year(data)