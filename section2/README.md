Exercise 1 & exercises 2/3 are implemented independently.

There is a code that is repeated between the scripts (e.g. `load_data`), but that's done becuase tasks are implemented independently with an assumption that it's not neccessary to reuse the code between them.

# Exercise 1: Correcting and Enhancing the Loss Calculation Script

`exercise1_losses_calculator.py` represents corrected loss calculation script.

Script assumes 5% as standard discount rate. If can't be assumed, script would have to ask for user input. The same way it asks for calculation period in years.

Script doesn't have external dependencies. Execute the following command in your terminal to use the script:

```
python exercise1_losses_calculator.py
```

# Exercise 2: Implementing a Complex Mathematical Loss Formula

`exercise2_complex_mathematical_loss_formula.py` represents complex mathematical loss calculation script.

This script also assumes 5% as standard discount rate.

Script doesn't have external dependencies. Execute the following command in your terminal to use the script:

```
python exercise2_complex_mathematical_loss_formula.py
```

# Exercise 3: Scaling the Loss Calculation Model

Scalability analysis:

1. Scripts execution time is increasing from 2s for 1.000.000 buildings, to 12s for 10.000.000 buildings and 300s for 100.000.000 buildings. Exact values are less important and dependent on the used hardware, but it's clear that increase isn't linear.
2. Although memory limit wasn't hit during quick tests, it's obvious that memory constraints will eventually be hit and that naive script implementation has limits.

Strategies for scaling the script from exercise 2:

1. Instead of loading whole JSON file in memory, data could be loaded in chunks. For example, `data.json` can be treated as plain text file read chunk by chunk (e.g. line by line), processed as a string where substrings of that big string will be treated as chunks for processing. Alternative path would be to use alternative file format (e.g. CSV) which is easier to read in chunkgs.
2. Doing vectorized calculations in `numpy` would cut the calculation time. Once there is more than 1.000.000 buildings to process, numpy calculations were roughly 2 times faster on a computer used for testing. For N x 100.000.000 datasets numpy performance were more than 2 times better. See below for `calculate_potential_financial_losses_estimate` function implementions using numpy.
3. Further optimisations are possible with explicit parallelization (e.g. joblib, multiprocessing, dask), with computations on GPU (instead of CPU).
4. A possible altenative to vectorized `numpy` calculations would be to use Cython to compile python code to C code.

Which strategy will give the best results depends on what are the acceptable performances (e.g. maybe performances without explicit parallelization are already acceptable), availability of CPU/GPU resources, maintainability (e.g. Cython path introduces additional complexity).

Calculating complex mathematical loss formula using numpy (function receives building data in chunks, chunk isn't the whole JSON file):

```python
DISCOUNT_RATE = 0.05

def calculate_loss_discount(years):
    return math.pow((1 + DISCOUNT_RATE), years)

def calculate_potential_financial_losses_estimate_unsing_numpy(
    building_data: List[Building], years: int
) -> Tuple[float, List[float]]:

    floor_area_array = np.array([building["floor_area"] for building in building_data])
    construction_cost_array = np.array([building["construction_cost"] for building in building_data])
    hazard_probability_array = np.array([building["hazard_probability"] for building in building_data], dtype=np.float32)
    inflation_rate_array = np.array([building["inflation_rate"] for building in building_data], dtype=np.float32)

    denominator = calculate_loss_discount(years=years)
    complex_value_loss_array = (
        construction_cost_array
        * np.exp(inflation_rate_array * floor_area_array / 1000)
        * hazard_probability_array
    ) / denominator

    buildings_losses = np.round(complex_value_loss_array, 2)

    total_loss = np.sum(buildings_losses)
    return total_loss, buildings_losses.tolist()
```
