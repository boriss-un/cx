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


def calculate_loss_discount(years) -> float:
    return math.pow((1 + DISCOUNT_RATE), years)


def calculate_projected_losses(
    building_data: List[Building], years: int
) -> Tuple[float, List[float]]:
    total_loss = 0

    for building in building_data:
        floor_area = building["floor_area"]
        construction_cost = building["construction_cost"]
        hazard_probability = building["hazard_probability"]
        inflation_rate = building["inflation_rate"]

        # calculate present constraction cost as: Construction cost per square meter * Floor area in square meters
        constraction_cost_today = construction_cost * floor_area

        # calculate constraction cost at future date assuming that inflation rate stays unchanged during given calculation period (e.g. 10 years)
        future_cost = constraction_cost_today * ((1 + inflation_rate) ** years)

        # Calculate risk-adjusted loss assuming that climate-related hazard can only occur once during given calculation period (e.g. 10 years).
        # If hazard can occur independently each year, we will need to multiply the formula below with number of years.
        risk_adjusted_loss = future_cost * hazard_probability

        # Calculate present value of the risk-adjusted loss (assuming that $100 today is worth more than $100 in the future)
        present_value_loss = risk_adjusted_loss / calculate_loss_discount(years=years)

        total_loss += present_value_loss

    return total_loss


def main() -> None:
    try:
        years = int(input("Enter calculation period as number of years: "))
        if years < 1:
            raise ValueError
    except ValueError:
        print("Please enter a valid number of years")
        return

    data = load_data("data.json")

    total_loss = calculate_projected_losses(data, years)
    print(f"Total Projected Financial Loss: ${total_loss:,.2f}")


if __name__ == "__main__":
    main()
