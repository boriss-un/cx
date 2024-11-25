import json
import math
from typing import List, TypedDict, Tuple

# Assumed discount rate (copied from the original script).
DISCOUNT_RATE = 0.05


class Building(TypedDict):
    buildingId: int
    floor_area: float
    construction_cost: int
    hazard_probability: float
    inflation_rate: float


def load_data(filepath: str) -> List[Building]:
    with open(filepath, "r") as file:
        return json.load(file)


def calculate_loss_discount(years):
    return math.pow((1 + DISCOUNT_RATE), years)


def calculate_potential_financial_losses_estimate(
    building_data: List[Building], years: int
) -> Tuple[float, List[float]]:
    buildings_losses = []

    for building in building_data:
        floor_area = building["floor_area"]
        construction_cost = building["construction_cost"]
        hazard_probability = building["hazard_probability"]
        inflation_rate = building["inflation_rate"]

        complex_value_loss = (
            construction_cost
            * (math.e ** (inflation_rate * floor_area / 1000))
            * hazard_probability
        ) / calculate_loss_discount(years=years)

        # round to 2 decimal places to prevent differences when results are printed
        buildings_losses.append(round(complex_value_loss, 2))

    return math.fsum(buildings_losses), buildings_losses


def main() -> None:
    try:
        years = int(input("Enter calculation period as number of years: "))
        if years < 1:
            raise ValueError
    except ValueError:
        print("Please enter a valid number of years")
        return

    data = load_data("data.json")

    total_loss_estimate, buildings_losses = (
        calculate_potential_financial_losses_estimate(data, years)
    )

    print(f"\nTotal Potential Financial Loss Estimate: ${total_loss_estimate:,.2f}")
    print("\nPotential Financial Loss Estimate for individual buildings:")
    for i, building_loss in enumerate(buildings_losses, 1):
        print(f"\tLosses for building {i}: ${building_loss:,.2f}")


if __name__ == "__main__":
    main()
