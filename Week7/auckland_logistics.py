from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Lock
from typing import Dict, Type, Any

# ---------- Domain ----------
@dataclass(frozen=True)
class Shipment:
    ref: str
    origin: str
    destination: str
    weight_kg: float
    priority: int = 3  # 1=highest

@dataclass(frozen=True)
class DispatchResult:
    ok: bool
    message: str
    mode: str

# ---------- Strategy: transport interface ----------
class Transport(ABC):
    @abstractmethod
    def dispatch(self, s: Shipment) -> DispatchResult: ...

# ---------- Concrete transports ----------
class RoadTruck(Transport):
    def __init__(self, fleet_id: str): self.fleet_id = fleet_id
    def dispatch(self, s: Shipment) -> DispatchResult:
        return DispatchResult(True, f"Truck {self.fleet_id} → {s.destination} ({s.weight_kg}kg)", "road")

class SeaVessel(Transport):
    def __init__(self, imo: str): self.imo = imo
    def dispatch(self, s: Shipment) -> DispatchResult:
        return DispatchResult(True, f"Vessel {self.imo} sailing to {s.destination}", "sea")

class RailTrain(Transport):
    def __init__(self, service: str): self.service = service
    def dispatch(self, s: Shipment) -> DispatchResult:
        return DispatchResult(True, f"Rail {self.service} → {s.destination}", "rail")

class AirCargo(Transport):
    def __init__(self, flight: str): self.flight = flight
    def dispatch(self, s: Shipment) -> DispatchResult:
        return DispatchResult(True, f"Flight {self.flight} to {s.destination}", "air")

# ---------- Factory (registry-based) ----------
class TransportFactory:
    _registry: Dict[str, Type[Transport]] = {}

    @classmethod
    def register(cls, key: str, transport_cls: Type[Transport]) -> None:
        cls._registry[key.lower()] = transport_cls

    @classmethod
    def create(cls, key: str, **kwargs) -> Transport:
        k = key.lower()
        if k not in cls._registry:
            raise ValueError(f"Unknown transport mode: {key}")
        return cls._registry[k](**kwargs)

# register built-ins
TransportFactory.register("road", RoadTruck)
TransportFactory.register("sea", SeaVessel)
TransportFactory.register("rail", RailTrain)
TransportFactory.register("air", AirCargo)

# ---------- Singleton: Logistics Hub ----------
class LogisticsHub:
    """Singleton entrypoint for Auckland Port logistics."""
    _instance: "LogisticsHub | None" = None
    _lock = Lock()
    name: str  # Add attribute definition

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # one-time fields
                    cls._instance.name = "Auckland Port Hub"
        return cls._instance

    def route(self, s: Shipment) -> str:
        """Very naive routing rule just for demo."""
        if s.priority == 1:
            return "air"
        if s.weight_kg > 15000:
            return "sea"
        if "South" in s.destination or "Southland" in s.destination:
            return "rail"
        return "road"

    def dispatch(self, s: Shipment, override_mode: str | None = None, **init_kwargs: Any) -> DispatchResult:
        mode = override_mode or self.route(s)
        transport = TransportFactory.create(mode, **init_kwargs)
        return transport.dispatch(s)

if __name__ == "__main__":
    hub = LogisticsHub()                              # Singleton
    s1 = Shipment("REF1001", "Auckland Port", "Hamilton", 8000)
    s2 = Shipment("REF1002", "Auckland Port", "Wellington", 22000)
    s3 = Shipment("REF1003", "Auckland Port", "Christchurch", 5000, priority=1)

    print(hub.dispatch(s1, fleet_id="TRK-21"))                     # road
    print(hub.dispatch(s2, imo="IMO-9876543"))                     # sea (heavy)
    print(hub.dispatch(s3, flight="NZ321"))                        # air (priority)

    # 手动指定模式（覆盖路由）override routing
    print(hub.dispatch(s1, override_mode="rail", service="KiwiRail-EX"))
