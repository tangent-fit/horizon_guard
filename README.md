# HorizonGuard

### Stop High-Confidence AI Hallucinations with Geometry.

HorizonGuard is a lightweight, post-hoc Python library that retrofits existing AI models with geometrically aware uncertainty quantification.

It addresses the "linear arrogance" problem where models make high-confidence, wrong predictions outside their training distribution (OOD). It works by wrapping predictions in an uncertainty envelope that scales asymptotically based on the tangent projection geometry intrinsic to bounded observation.

**No retraining required. Works on model outputs.**

## The Problem in 10 Seconds

Your model is trained on a finite set of data. When it sees something far outside that set, it doesn't know it doesn't know. It extrapolates linearly and confidently returns garbage (a "hallucination").

## The Fix

HorizonGuard takes your model's prediction and a "distance score" (how far the input is from training data). It uses a closed-form geometric calculation to apply a "horizon tax" to the uncertainty.

If the input is near the horizon of the model's knowledge, the uncertainty bounds explode, turning a dangerous hallucination into a safe, quantified statement of ignorance.

## Installation

```bash
pip install horizonguard
