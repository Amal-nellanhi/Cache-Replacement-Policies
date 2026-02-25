import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# FINAL DATASET (FROM YOUR GEM5 RESULTS)
# ==========================================
labels = ['Random', 'LRU', 'FIFO', 'MRU']

# Metrics (Normalized so they fit on the same chart)
# We invert "Better" metrics so that the OUTSIDE of the web is always BETTER.
# Here: Lower is better for all metrics, so we plot (1 / value) or relative performance.

# Raw Data
miss_rates = [0.1219, 0.1226, 0.1229, 0.1233]
cpi = [8.639, 8.664, 8.678, 8.689]
bandwidth = [619.6, 620.1, 621.5, 624.6] # MB/s
writebacks = [2670, 2235, 2643, 3200]

# --- 1. Create a Comparison Bar Chart for the "Big 2" (CPI & Bandwidth) ---
x = np.arange(len(labels))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Bandwidth (Bars)
bars = ax1.bar(x, bandwidth, width, label='Memory Bandwidth (MB/s)', color='#3498db', alpha=0.7)
ax1.set_ylabel('Bandwidth (MB/s)', color='#3498db', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#3498db')
ax1.set_ylim(615, 626) # Zoom in to show differences

# Plot CPI (Line)
ax2 = ax1.twinx()
line = ax2.plot(x, cpi, label='CPI (Lower is Better)', color='#e74c3c', marker='o', linewidth=3, markersize=8)
ax2.set_ylabel('CPI (Cycles Per Instruction)', color='#e74c3c', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2.set_ylim(8.62, 8.70) # Zoom in

# Formatting
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax1.set_title('Efficiency Analysis: CPI vs Bandwidth', fontsize=14)
ax1.grid(axis='x', linestyle='--')

# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('efficiency_analysis.png', dpi=300)
print("Graph saved as 'efficiency_analysis.png'")

# --- 2. Create the "Spider Web" (Radar) Chart ---
# We normalize everything to MRU (the worst) = 1.0
# Values < 1.0 mean BETTER performance
def normalize(data):
    baseline = max(data) # MRU is usually max (worst)
    return [x / baseline for x in data]

# Data preparation
categories = ['Miss Rate', 'CPI', 'Bandwidth', 'Writebacks']
N = len(categories)

# Create values for each policy
values_random = [
    miss_rates[0]/max(miss_rates), 
    cpi[0]/max(cpi), 
    bandwidth[0]/max(bandwidth), 
    writebacks[0]/max(writebacks)
]
values_lru = [
    miss_rates[1]/max(miss_rates), 
    cpi[1]/max(cpi), 
    bandwidth[1]/max(bandwidth), 
    writebacks[1]/max(writebacks)
]

# Repeat first value to close the circle
values_random += values_random[:1]
values_lru += values_lru[:1]

# Angles
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

# Draw Random
ax.plot(angles, values_random, linewidth=2, linestyle='solid', label='Random (Speed)', color='#2ecc71')
ax.fill(angles, values_random, '#2ecc71', alpha=0.1)

# Draw LRU
ax.plot(angles, values_lru, linewidth=2, linestyle='solid', label='LRU (Efficiency)', color='#e74c3c')
ax.fill(angles, values_lru, '#e74c3c', alpha=0.1)

# Labels
plt.xticks(angles[:-1], categories, size=12, fontweight='bold')
ax.set_rlabel_position(0)
plt.yticks([0.8, 0.9, 1.0], ["0.8", "0.9", "1.0"], color="grey", size=7)
plt.ylim(0.6, 1.05)

plt.title('Policy Trade-off: Random vs LRU\n(Smaller Shape = Better)', size=15, y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.tight_layout()
plt.savefig('radar_chart.png', dpi=300)
print("Graph saved as 'radar_chart.png'")