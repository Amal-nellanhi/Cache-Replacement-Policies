import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# YOUR ACTUAL GEM5 RESULTS
# ==========================================
policies = ['Random', 'LRU', 'FIFO', 'MRU']

# 1. Miss Rates (Lower is Better)
miss_rates = [0.121915, 0.122648, 0.122890, 0.123289]

# 2. Simulation Seconds (Lower is Faster)
sim_seconds = [0.021674, 0.021737, 0.021772, 0.021798]

# 3. Writebacks (Lower is Less Memory Traffic)
writebacks = [2670, 2235, 2643, 3200]

# ==========================================
# PLOTTING LOGIC
# ==========================================
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
# Colors: Green (Best), Blue (Good), Orange (Okay), Red (Bad)
colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c'] 

# --- Plot 1: Miss Rate ---
bars1 = ax[0].bar(policies, miss_rates, color=colors, alpha=0.8)
ax[0].set_title('Cache Miss Rate\n(Lower is Better)', fontsize=14, fontweight='bold')
ax[0].set_ylabel('Miss Rate (Ratio)', fontsize=12)
# Zoom in on the Y-axis to show the small differences
ax[0].set_ylim(0.121, 0.124) 
ax[0].grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars1:
    height = bar.get_height()
    ax[0].text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# --- Plot 2: Execution Time ---
bars2 = ax[1].bar(policies, sim_seconds, color=colors, alpha=0.8)
ax[1].set_title('Execution Time\n(Lower is Faster)', fontsize=14, fontweight='bold')
ax[1].set_ylabel('Time (Seconds)', fontsize=12)
# Zoom in to show speed difference
ax[1].set_ylim(0.0216, 0.0219)
ax[1].grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars2:
    height = bar.get_height()
    ax[1].text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.5f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')

# --- Plot 3: Writebacks ---
# Note: Colors swapped here because LRU (2nd item) is best for writebacks
wb_colors = ['#f39c12', '#2ecc71', '#f39c12', '#e74c3c'] 
bars3 = ax[2].bar(policies, writebacks, color=wb_colors, alpha=0.8)
ax[2].set_title('Memory Writebacks\n(Lower = Less Energy/Traffic)', fontsize=14, fontweight='bold')
ax[2].set_ylabel('Count', fontsize=12)
ax[2].grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars3:
    height = bar.get_height()
    ax[2].text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('gem5_results.png', dpi=300)
print("SUCCESS: Graph saved as 'gem5_results.png'")