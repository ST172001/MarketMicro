import matplotlib.pyplot as plt
import numpy as np

# Company names from Rolls spread (only companies present in Rolls spread)
companies = [
    'CIPLA', 'NTPC', 'ASIANPAINT', 'AXISBANK', 'HDFC', 'BPCL', 'INFY', 'ACC',
    'ICICIBANK', 'WIPRO', 'RELIANCE', 'BAJAJ-AUTO', 'IDFC', 'ITC', 'TCS',
    'ONGC', 'LT', 'TATAMOTORS', 'MARUTI'
]

# Defining each spread estimator's values (only for companies in Rolls spread)
predicted_spreads_rolls = [
    None, None, 20.88, 14.50, 8.81, None, None, 9.70, 
    None, 2.22, None, 8.28, 2.19, 3.47, 19.76, 
    None, 7.00, None, 14.66
]

predicted_corwin_spreads = [
    3.88, 0.21, 46.93, 9.92, 7.61, 0, 12.01, 12.54,
    11.05, 1.63, 0, 19.99, 3.58, 0, 10.47,
    3.03, 0, 2.07, 18.46
]

predicted_abdi_spreads = [
    3.7, 0.18, 45.3, 9.5, 7.1, 0, 11.4, 12.0,
    10.5, 1.5, 0, 18.5, 3.4, 0, 9.8,
    2.9, 0, 1.95, 17.5
]

predicted_dai_spreads = [
    2.5, 0.12, 42.0, 8.0, 5.8, 0, 9.9, 10.5,
    9.0, 1.1, 0, 16.8, 2.2, 0, 8.2,
    1.7, 0, 1.2, 15.8
]

# Filtering out None values and calculating percentage error for each estimator
x_labels, rolls, corwin, abdi, dai = [], [], [], [], []

for i, company in enumerate(companies):
    if predicted_spreads_rolls[i] is not None:  # Only include non-None values
        x_labels.append(company)
        roll_value = predicted_spreads_rolls[i]
        rolls.append(roll_value)
        corwin.append(predicted_corwin_spreads[i])
        abdi.append(predicted_abdi_spreads[i])
        dai.append(predicted_dai_spreads[i])

# Plotting the spreads
plt.figure(figsize=(14, 8))
plt.plot(x_labels, rolls, marker='o', label='Rolls', linestyle='-')
plt.plot(x_labels, corwin, marker='o', label='Corwin', linestyle='--')
plt.plot(x_labels, abdi, marker='o', label='Abdi', linestyle='-.')
plt.plot(x_labels, dai, marker='o', label='Dai', linestyle=':')

plt.xlabel("Company")
plt.ylabel("Percentage Spread Error")
plt.title("Comparison of Predicted Spread Errors by Estimator")
plt.legend(title="Estimators")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig('comparison.png')