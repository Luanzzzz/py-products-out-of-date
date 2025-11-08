import datetime
import pytest
import app.main as main


@pytest.fixture
def sample_products() -> list[dict]:
    return [
        {"name": "milk", "expiration_date": datetime.date(2025, 1, 1)},
        {"name": "bread", "expiration_date": datetime.date(2024, 11, 5)},
        {"name": "cheese", "expiration_date": datetime.date(2024, 11, 4)},
    ]


def test_products_outdated(
        monkeypatch: pytest.MonkeyPatch,
        sample_products: list[dict]
) -> None:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return cls(2024, 11, 5)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    result = main.outdated_products(sample_products)
    assert result == ["cheese"]


def test_products_fresh(
        monkeypatch: pytest.MonkeyPatch,
        sample_products: list[dict]
) -> None:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return cls(2024, 11, 3)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    result = main.outdated_products(sample_products)
    assert result == []


def test_products_all_expired(
        monkeypatch: pytest.MonkeyPatch,
        sample_products: list[dict]
) -> None:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return cls(2026, 1, 1)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    result = main.outdated_products(sample_products)
    assert set(result) == {"milk", "bread", "cheese"}


def test_expiration_day_today_not_outdated(
        monkeypatch: pytest.MonkeyPatch
) -> None:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return cls(2024, 11, 5)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    products = [
        {"name": "butter", "expiration_date": datetime.date(2024, 11, 5)}
    ]
    result = main.outdated_products(products)
    assert result == []


def test_expiration_day_yesterday_outdated(
        monkeypatch: pytest.MonkeyPatch
) -> None:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return cls(2024, 11, 5)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    products = [
        {"name": "yogurt", "expiration_date": datetime.date(2024, 11, 4)}
    ]
    result = main.outdated_products(products)
    assert result == ["yogurt"]
