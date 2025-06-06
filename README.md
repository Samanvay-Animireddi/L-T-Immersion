# Task #01 Product Failure Analysis

This dataset simulates real-world performance degradation and failure in AMOLED screens over time. It includes 10,000 samples with realistic parameter combinations based on usage patterns, temperature, brightness levels, and other operational factors. Each entry represents an individual screen's state and whether it has failed.

### 🔧 Features

- **Usage Hours** – Total time the screen has been in use (in hours)
- **Average Brightness Level** – Typical brightness setting (0–100%)
- **Average Temperature** – Operating temperature (°C)
- **Number of Dead Pixels** – Count of non-functioning pixels
- **Firmware Updates** – Number of firmware patches installed
- **Color Shift Index** – Degree of color distortion (0–100)
- **Burn-In Level** – Screen burn-in severity (0–100)
- **Refresh Rate Decrement Percent** – Reduction in screen refresh rate (%)
- **Failure Type** – Cause of failure (e.g., Burn-In, Color Shift, Dead Pixels)
- **Failed?** – Boolean flag indicating screen failure

### 📦 Use Cases

- Predictive maintenance for displays
- Machine learning model training for failure classification
- Feature importance analysis for screen degradation

| Parameter | Good State Range | Notes |
| --- | --- | --- |
| **Usage Hours** | `0 – 4000` hours | Beyond 4000, screen aging starts, but varies by usage patterns |
| **Average Brightness Level** | `30% – 70%` | Higher brightness accelerates burn-in |
| **Average Temperature** | `30°C – 45°C` | Above 50°C may degrade organic compounds in AMOLED |
| **Number of Dead Pixels** | `0 – 1` | Dead pixels should be minimal or none; >5 often unacceptable |
| **Firmware Updates** | `≥ 1` | At least one firmware update recommended for performance/stability |
| **Color Shift Index** | `0.00 – 0.20` | Above 0.4 typically indicates noticeable degradation |
| **Burn In Level** | `0 – 1` | Levels 2+ imply visible burn-in |
| **Refresh Rate Decrement %** | `0% – 5%` | A decrease >10% signals performance degradation |
| **Failure Type** | `No_Failure` | Any other type indicates an issue |
