# Voter Demographics Analysis Tool

## Overview
This project is a Python-based application designed to process and analyze voter data from NGP/VAN alongside U.S. Census data. The tool provides insights into the racial demographics of voters in specific regions and generates outputs ready for visualization in Tableau. Emphasizing modularity, scalability, and flexibility, it is a robust solution for voter demographic analysis.

## Features

### 1. Data Handling and Preprocessing

- Cleans and standardizes voter data to ensure consistency across datasets.
- Validates and handles missing data fields, such as ZIP codes.

### 2. Geocoding Functionality

- Utilizes `geopy` to convert voter addresses into geographic coordinates for spatial analysis.
- Includes error handling and retry mechanisms for rate-limited or failed requests.

### 3. Data Integration

- Merges NGP/VAN voter data with Census demographic data using ZIP codes as the primary key.
- Computes key demographic metrics such as racial population percentages (e.g., White, Black, Hispanic).

### 4. Flexible Data Export

- Exports data in multiple formats:
  - **CSV**: Standard data files for analysis.
  - **Tableau Hyper Format**: Enables seamless integration with Tableau for visualization.

### 5. Robust Error Handling

- Dynamically installs missing Python libraries.
- Manages issues such as missing files, geocoding errors, and inconsistencies during data merges.

---

## Technical Details

### Tech Stack

- **Programming Language**: Python
- **Libraries**:
  - Pandas: For data manipulation and cleaning.
  - Geopy: For geocoding voter addresses.
  - Tableau Hyper API: For generating Tableau-ready `.hyper` files.
- **Visualization**: Tableau

### How It Works

1. **Data Input**: The application ingests voter data (CSV) and Census data (CSV).
2. **Geocoding**: Converts voter addresses into geographic coordinates.
3. **Data Merging**: Aligns voter and Census data using ZIP codes.
4. **Analysis**: Computes demographic metrics.
5. **Output**: Produces CSV and `.hyper` files for Tableau.

### Challenges Addressed

- **Geocoding Rate Limits**: Implements retry mechanisms and logs errors to handle rate-limited requests.
- **Large Dataset Integration**: Optimizes data merging and ensures consistency in key fields.
- **Dynamic Dependencies**: Supports on-the-fly installation of missing libraries for enhanced portability.

---

## Installation

### Prerequisites

- Python 3.8 or later.
- Required Python libraries:
  - `pandas`
  - `geopy`
  - `tableauhyperapi`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/voter-demographics-analysis-tool.git
   ```
2. Navigate to the project directory:
   ```bash
   cd voter-demographics-analysis-tool
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

1. **Prepare Input Files**:
   - Place voter data in `voter_data.csv`.
   - Place Census data in `census_data.csv`.
2. **Run the Script**:
   ```bash
   python main.py
   ```
3. **View Outputs**:
   - Outputs are saved in the `output/` directory as `voter_analysis.csv` and `voter_analysis.hyper`.
4. **Visualize in Tableau**:
   - Import the `.hyper` file into Tableau to create dashboards and analyze trends.

---

## Example Outputs

### CSV Output

| ZIP Code | Total Population | White (%) | Black (%) | Hispanic (%) |
| -------- | ---------------- | --------- | --------- | ------------ |
| 12345    | 15,000           | 50        | 30        | 20           |

### Tableau Visualization

- A heatmap showing voter racial demographics by ZIP code.
- Charts illustrating regional demographic trends.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or feedback, please contact:

- **Sowande Crews**
- Email: [sowandec@gmail.com](mailto\:sowandec@gmail.com)
- GitHub: sowandec



