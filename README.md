# Sales Data Analyzer

A menu-driven Python project for exploring, cleaning, analyzing, and visualizing data from CSV files. It uses **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn**.

## Features

- **Load CSV datasets** with basic error handling for missing, empty, or unreadable files.
- **Explore data**
  - Display the first and last five rows.
  - View column names and data types.
  - Display DataFrame information.
- **Handle missing data**
  - Display rows containing missing values.
  - Fill missing numeric values with column means.
  - Drop rows containing missing values.
  - Replace missing values in a selected column.
- **Perform DataFrame operations**
  - Display a selected column.
  - Sort rows by a column.
  - Drop a column.
  - Rename a column.
  - Display the full DataFrame.
- **Calculate descriptive statistics**
  - Mean, median, minimum, maximum, sum, variance, and standard deviation.
  - Display rows containing a column's maximum value.
- **Create visualizations**
  - Matplotlib: bar plot, line plot, scatter plot, pie chart, histogram, and stacked area plot.
  - Seaborn: correlation heatmap and box plot.
  - Save the current visualization as an image or PDF/SVG file.
- **Analyze with NumPy**
  - Convert a DataFrame to a NumPy array.
  - Calculate mean, median, and standard deviation for numeric data.
  - Access a cell by row and column index.
  - Split an array into multiple parts.
- **Create pivot tables** using mean, sum, count, maximum, or minimum aggregation.

## Technologies Used

- Python 3.10+
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Requirements

Install Python **3.10 or newer**. The program uses `match/case`, which is available from Python 3.10 onward.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   ```

2. **Open the project folder**

   ```bash
   cd YOUR-REPOSITORY
   ```

3. **Install the dependencies**

   ```bash
   python -m pip install pandas numpy matplotlib seaborn
   ```

4. **Run the program**

   ```bash
   python sales_data_analyzer.py
   ```

> If your Python installation uses `py` on Windows, you can also run `py sales_data_analyzer.py`.

## How to Use

1. Start the program.
2. Choose **1. Load dataset** from the main menu.
3. Enter the path to your CSV file. For example:

   ```text
   C:\Users\YourName\Desktop\sales.csv
   ```

   On Windows, you can also enter a path using forward slashes:

   ```text
   C:/Users/YourName/Desktop/sales.csv
   ```

4. Use the main menu to explore, clean, analyze, or visualize the loaded dataset.
5. To save a chart, first generate a visualization, then choose **Save visualization** from the main menu and enter a filename.

### Example CSV

You can test the program with a small CSV file such as:

```csv
Date,Product,Category,Quantity,Amount,Profit
2026-01-01,Notebook,Stationery,10,500,100
2026-01-02,Pen,Stationery,20,300,80
2026-01-03,Mouse,Electronics,5,2500,400
2026-01-04,Keyboard,Electronics,3,1800,250
2026-01-05,Notebook,Stationery,8,400,75
```

Save this sample as `sales.csv`, then load it in the program.

## Project Structure

```text
sales-data-analyzer/
├── sales_data_analyzer.py
└── README.md
```

## Notes and Limitations

- Load a dataset before choosing data exploration, cleaning, statistics, visualization, NumPy analysis, or pivot-table features.
- Numeric statistics and plots require suitable numeric columns.
- The mean-imputation option fills missing values in numeric columns only.
- NumPy mean, median, and standard deviation are calculated across the available numeric values in the dataset.
- Chart output depends on the columns and values in the selected CSV file.
- The program is a command-line application; it does not include a web interface or database connection.

## Future Improvements

- Add automated tests.
- Add export options for cleaned datasets and statistical summaries.
- Add column-specific missing-value strategies.
- Add more chart types and customization options.
- Add a configuration file for default dataset paths.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the program.
5. Submit a pull request.


