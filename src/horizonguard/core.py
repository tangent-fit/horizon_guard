"""
HorizonGuard: Geometric Uncertainty Quantification for AI Models.

This library provides a post-hoc mechanism to wrap AI model predictions in a
geometrically derived uncertainty envelope. It addresses high-confidence OOD
failures ("hallucinations") by acknowledging the "horizon" of the training data.

It works by mapping a "distance-from-training-data" score onto a tangent
projection, scaling uncertainty asymptotically by sec^2(theta) as inputs
approach the geometric horizon of the model's knowledge.

No retraining required. Works on model outputs.
"""

import numpy as np

class HorizonGuard:
    """
    Wraps model predictions with geometric uncertainty based on distance from
    training distribution boundaries.
    """

    def __init__(self,
                 horizon_threshold: float = 1.0,
                 base_uncertainty: float = 0.1,
                 max_stretch_factor: float = 1e4,
                 distance_scaler: float = 1.0):
        """
        Initialize the HorizonGuard wrapper.

        Args:
            horizon_threshold (float): The distance score below which data is
                considered "in-distribution". Inside this radius, the geometric
                stretch factor is exactly 1.0 (linear regime).
            base_uncertainty (float): The inherent aleatoric noise assumed *inside*
                the training distribution. This is the minimum uncertainty width.
            max_stretch_factor (float): A numerical cap to prevent uncertainty from
                going to infinity at the exact asymptote. Defaults to 10,000x base.
            distance_scaler (float): Controls how quickly the horizon is approached
                once past the threshold. Higher values mean a slower approach to the
                asymptote. Often set equal to the horizon_threshold.
        """
        self.threshold = horizon_threshold
        self.base_sigma = base_uncertainty
        self.max_stretch = max_stretch_factor
        # Ensure scaler is positive to avoid divide-by-zero in arctan normalization
        self.scaler = max(distance_scaler, 1e-6) 

    def _calculate_geometric_stretch(self, distance_score: float) -> float:
        """
        Calculates the dilation factor (sec^2 theta) based on input distance.
        
        This is the core BOMA mechanism.
        """
        # 1. The Linear Regime (Inside the training center)
        if distance_score <= self.threshold:
            return 1.0

        # 2. The Horizon Regime (Outside the boundary)
        # Calculate how far past the threshold we are.
        excess_distance = distance_score - self.threshold
        
        # Map this excess distance to an angle theta approaching pi/2.
        # We use arctan as the bounded compression function.
        # theta approaches pi/2 as excess_distance approaches infinity.
        theta_rad = np.arctan(excess_distance / self.scaler)
        
        # Calculate the geometric dilation: sec^2(theta) = 1 / cos^2(theta)
        cos_theta = np.cos(theta_rad)
        
        # Guard against numerical instability at extreme edges just before the cap
        if cos_theta < 1e-9:
             stretch = self.max_stretch
        else:
             stretch = 1.0 / (cos_theta ** 2)

        # 3. Apply the hard numerical cap to
