Write up by Abiral Tuladhar:

**Deliverables:**
- `optimize.py` (one file containing both methods)
- `satellite_gen.py` (synthetic input generator used for testing)
- This `README.md` (brief report)

**Input Format:**
The solver expects a CSV with the following header/columns:

- `satellite` (string identifier)
- `fuel_cost_kg` (float)
- `revenue_usd` (int)

The challenge instructions referenced two attachments (PDF + input CSV). I received the PDF, but the input CSV was not included in the email. Initially, I was nervous that I was not going to be able to complete the challenge, however, I decided not to let that stop me. Instead, I additionally wrote a python script that randomly generates N number of satellites which I used as my own test data, I have also included the 3 randomly generated csv files I used in order to work on this.

Implemented Methods:

1) Greedy

The idea is to compute the density for each opportunity where density is revenue / fuel. I then sorted the opportunities by density descending, then iterate through the list and take each opportunity if it fits within the remaining fuel budget.

Pros: 
- Very simple and easy to implement
- Runs with time complexity O(n log n)

Cons:
- Greedy is an algorithm notorious for not being guaranteed optimal (cutting itself off from better combinations)

Returns selected_indices as well as total_revenue where the selected_indices is a set of row indices from the csv

2) Recursive DP (Memoization)

Use a recursive approach where we pass index and current fuel units remaining, at each opportunity we skip or take depending on which one is better, adding to revenue and reducing the remaining capacity.

For this approach I scaled fuel to integer units at scale 100 to avoid floating point issues in DP state keys.

A memoization dictionary stores each subproblem result so that if the exact subproblem is encountered again, we can simply return the stored value.

Pros:
- Finds the optimal selection

Cons: 
- More complex than greedy

To Run:
Input own csv file and edit csv_path in optimize.py, or run satellite_gen.py which can also be configured for row count, seed, and ranges. Then run optimize.py.

Notes:

synthetic.csv: Seed 42: Greedy matched DP
synthetic2.csv: Seed 70: Greedy matched DP
synthetic3.csv: Seed 112: DP outperformed Greedy by $2000
