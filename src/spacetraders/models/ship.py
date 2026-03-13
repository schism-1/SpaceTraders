from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Ship:
    symbol: str
    role: str
    nav_status: str # IN_TRANSIT, ORBIT, DOCKED
    flight_mode: str
    waypoint_symbol: str
    cargo_capacity: int
    cargo_units: int
    fuel_capacity: int
    fuel_current: int
    
    raw_data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # Create Ship object directly from json response
        return cls(
            symbol = data['symbol'],
            role = data['regstration']['role'],
            nav_status = data['nav']['status'],
            flight_mode = data['nav']['flightMode'],
            waypoint_symbol = data['nav']['waypointSymbol'],
            cargo_capacity = data['cargo']['capacity'],
            cargo_units = data['cargo']['units'],
            fuel_capacity = data['fuel']['capacity'],
            fuel_current = data['fuel']['current'],
        )

    @property
    def is_full(self):
        return self.cargo_units >= self.cargo_capacity
    
    @property
    def needs_fuel(self):
        return self.fuel_current < (self.fuel_capacity * 0.4)
