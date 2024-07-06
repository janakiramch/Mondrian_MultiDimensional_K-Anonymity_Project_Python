import matplotlib.pyplot as plt
import numpy as np

# Sample discernability penalty data (replace this with your actual data)
k_values = [2, 3, 5, 10, 25, 50, 100, 200]
discernability_penalty_values = [0.000545472, 0.001447529, 0.003401643, 0.007309872, 0.01512633, 0.030759245, 0.062025076, 0.124556738]

# Plotting the discernability penalty
plt.plot(k_values, discernability_penalty_values, marker='o', linestyle='-', color='b', label='Discernability Penalty')

l = np.arange(0,0.1,0.05)

# Adding labels and title
plt.xlabel('k (anonymity parameter)')
plt.ylabel('Discernability Penalty')
plt.title('Discernability Penalty for Employee Dataset')
# plt.xscale('log')  # Log scale for better visualization if needed
# plt.yscale('log')  # Log scale for better visualization if needed
plt.xticks(k_values)
plt.yticks(l)
plt.legend()
plt.grid(True)

# Display the plot
plt.show()