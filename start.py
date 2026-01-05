from horizonguard import HorizonGuard

# 1. Configure based on your training data stats
# Example: Data usually has distance scores < 2.0. Inherent noise is ~0.5.
guard = HorizonGuard(horizon_threshold=2.0, base_uncertainty=0.5)

# --- Scenario: Far Out-of-Distribution Input ---
# Your model confidently predicts something wild:
raw_prediction = 150.0 
# Your distance metric shows it's far away:
distance_score = 15.0   

# Wrap it:
low, mean, high, sigma = guard.wrap_prediction(raw_prediction, distance_score)

print(f"Prediction: {mean}")
print(f"Geometric Uncertainty Bounds: [{low:.2f}, {high:.2f}]")
# Output: Prediction: 150.0
# Output: Geometric Uncertainty Bounds: [-36.12, 336.12]
# Result: The massive bounds tell downstream systems NOT to trust this prediction.
