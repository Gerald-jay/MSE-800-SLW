from admin_service.car_service import PeeweeCarService
import pytest

svc = PeeweeCarService()

def test_create_car_ok():
    car = svc.create_car(make="T", model="M", year=2024, kilometre=0,
                         daily_rate=10.0, min_days=1, max_days=30, status="available")
    assert car.id is not None

def test_year_invalid():
    with pytest.raises(Exception):  # 建议用 from common.exceptions import ValidationError
        svc.create_car(make="T", model="M", year=1970, kilometre=0,
                       daily_rate=10.0, min_days=1, max_days=30, status="available")

def test_days_invalid():
    with pytest.raises(Exception):
        svc.create_car(make="T", model="M", year=2024, kilometre=0,
                       daily_rate=10.0, min_days=10, max_days=5, status="available")
