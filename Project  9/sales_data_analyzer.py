import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SalesDataAnalyzer:
    def __init__(self):
        self.df = None
        self.fig = None

    # -------------------- DATA LOADING --------------------
    def load_data(self):
        print("\n===== LOAD DATA =====")
        path = input("Enter the path of the dataset (CSV file): ").strip()

        if not path:
            print("File path cannot be empty!")
            return

        try:
            df = pd.read_csv(path)
            self.df = df
            print("Data loaded successfully!")
            if df.empty:
                print("Warning: The CSV contains column headers but no data rows.")
            print(df.head())

        except FileNotFoundError:
            print("Error: CSV file not found. Please check the file path.")
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")
        except PermissionError:
            print("Error: Permission denied while reading this file.")
        except Exception as e:
            print(f"Unexpected error while loading CSV: {e}")

    def _data_ready(self):
        if self.df is None:
            print("Please load a dataset first!")
            return False
        if self.df.empty:
            print("The dataset has no rows.")
            return False
        return True

    @staticmethod
    def _get_numeric_columns(df):
        return df.select_dtypes(include=[np.number]).columns.tolist()

    def _get_column(self, prompt, numeric=False):
        """Ask for a column name and validate it."""
        col = input(prompt).strip()
        if col not in self.df.columns:
            print("Invalid column name!")
            return None
        if numeric and not pd.api.types.is_numeric_dtype(self.df[col]):
            print("This operation requires a numeric column.")
            return None
        return col

    # -------------------- DATA EXPLORATION --------------------
    def explore_data(self):
        while True:
            if not self._data_ready():
                return

            print("""
=======================
EXPLORE DATA
1. Display first 5 rows
2. Display last 5 rows
3. Display data types
4. Display column names
5. Display basic info
6. Go back
=======================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    print(self.df.head())
                case "2":
                    print(self.df.tail())
                case "3":
                    print(self.df.dtypes)
                case "4":
                    print(list(self.df.columns))
                case "5":
                    self.df.info()
                case "6":
                    print("Returning to main menu...")
                    break
                case _:
                    print("Invalid choice!")

    # -------------------- MISSING DATA --------------------
    def handling_missing(self):
        while True:
            if not self._data_ready():
                return

            print("""
==============================
HANDLE MISSING DATA
1. Display rows with missing values
2. Fill numeric missing values with mean
3. Drop rows with missing values
4. Replace missing values in a selected column
5. Go back
==============================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    missing_rows = self.df[self.df.isna().any(axis=1)]
                    if missing_rows.empty:
                        print("No missing values found.")
                    else:
                        print(missing_rows)

                case "2":
                    numeric_cols = self._get_numeric_columns(self.df)
                    if not numeric_cols:
                        print("No numeric columns found.")
                        continue
                    self.df[numeric_cols] = self.df[numeric_cols].fillna(
                        self.df[numeric_cols].mean()
                    )
                    print("Filled missing numeric values with column means.")
                    print(self.df)

                case "3":
                    before = len(self.df)
                    self.df = self.df.dropna()
                    print(f"Dropped {before - len(self.df)} row(s) containing missing values.")
                    print(self.df)

                case "4":
                    col = input("Enter column name: ").strip()
                    if col not in self.df.columns:
                        print("Invalid column name!")
                        continue
                    value_text = input("Enter replacement value: ")
                    try:
                        if pd.api.types.is_numeric_dtype(self.df[col]):
                            value = float(value_text)
                            if pd.api.types.is_integer_dtype(self.df[col]) and value.is_integer():
                                value = int(value)
                        else:
                            value = value_text
                        count = int(self.df[col].isna().sum())
                        self.df[col] = self.df[col].fillna(value)
                        print(f"Replaced {count} missing value(s) in '{col}'.")
                        print(self.df)
                    except (ValueError, TypeError) as e:
                        print(f"Could not use that replacement value: {e}")

                case "5":
                    print("Returning to main menu...")
                    break
                case _:
                    print("Invalid choice!")

    # -------------------- VISUALIZATION HELPERS --------------------
    def _save_current_figure(self):
        if self.fig is None:
            print("Please generate a visualization first!")
            return
        filename = input("Enter filename to save (e.g. sales_chart.png): ").strip()
        if not filename:
            print("Filename cannot be empty!")
            return
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".pdf", ".svg")):
            filename += ".png"
        try:
            self.fig.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"Visualization saved successfully as {filename}")
        except (OSError, ValueError) as e:
            print(f"Could not save visualization: {e}")

    def save_visual(self):
        self._save_current_figure()

    def _show_figure(self):
        self.fig = plt.gcf()
        plt.tight_layout()
        plt.show()

    def visualization(self):
        while True:
            if not self._data_ready():
                return

            print("""
=============================
VISUALIZATION TOOLS
1. Matplotlib
2. Seaborn
3. Go back
=============================""")
            choice = input("Choose an option: ").strip()

            match choice:
                case "1":
                    self._matplotlib_menu()
                case "2":
                    self._seaborn_menu()
                case "3":
                    print("Returning to main menu...")
                    break
                case _:
                    print("Invalid choice!")

    def _matplotlib_menu(self):
        while True:
            print("""
===========================
MATPLOTLIB VISUALIZATION
1. Bar plot
2. Line plot
3. Scatter plot
4. Pie chart
5. Histogram
6. Stacked area plot
7. Go back
===========================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    x = self._get_column("Enter category/X-axis column: ")
                    if x is None:
                        continue
                    y = self._get_column("Enter numeric Y-axis column: ", numeric=True)
                    if y is None:
                        continue
                    data = self.df.groupby(x, dropna=False)[y].sum()
                    if data.empty:
                        print("No data available to plot.")
                        continue
                    plt.figure(figsize=(10, 6))
                    plt.bar(data.index.astype(str), data.values)
                    plt.xlabel(x)
                    plt.ylabel(f"Total {y}")
                    plt.title(f"{y} by {x}")
                    plt.xticks(rotation=45)
                    self._show_figure()

                case "2":
                    x = self._get_column("Enter X-axis column: ")
                    if x is None:
                        continue
                    y = self._get_column("Enter numeric Y-axis column: ", numeric=True)
                    if y is None:
                        continue
                    plt.figure(figsize=(10, 6))
                    plt.plot(self.df[x], self.df[y], marker="o")
                    plt.xlabel(x)
                    plt.ylabel(y)
                    plt.title(f"{y} over {x}")
                    plt.xticks(rotation=45)
                    self._show_figure()

                case "3":
                    x = self._get_column("Enter numeric X-axis column: ", numeric=True)
                    if x is None:
                        continue
                    y = self._get_column("Enter numeric Y-axis column: ", numeric=True)
                    if y is None:
                        continue
                    plt.figure(figsize=(8, 6))
                    plt.scatter(self.df[x], self.df[y])
                    plt.xlabel(x)
                    plt.ylabel(y)
                    plt.title(f"{y} vs {x}")
                    self._show_figure()

                case "4":
                    x = self._get_column("Enter category column: ")
                    if x is None:
                        continue
                    y = self._get_column("Enter numeric column: ", numeric=True)
                    if y is None:
                        continue
                    data = self.df.groupby(x, dropna=False)[y].sum()
                    data = data[data > 0]
                    if data.empty:
                        print("Pie chart needs positive totals to display.")
                        continue
                    plt.figure(figsize=(8, 8))
                    plt.pie(data.values, labels=data.index.astype(str), autopct="%1.1f%%", startangle=90)
                    plt.title(f"{y} distribution by {x}")
                    self._show_figure()

                case "5":
                    x = self._get_column("Enter numeric column: ", numeric=True)
                    if x is None:
                        continue
                    values = self.df[x].dropna()
                    if values.empty:
                        print("This column has no numeric values to plot.")
                        continue
                    plt.figure(figsize=(10, 6))
                    plt.hist(values, bins=7, edgecolor="black")
                    plt.xlabel(x)
                    plt.ylabel("Frequency")
                    plt.title(f"Histogram of {x}")
                    self._show_figure()

                case "6":
                    x = self._get_column("Enter category/X-axis column: ")
                    if x is None:
                        continue
                    raw_cols = input("Enter numeric columns separated by commas (e.g. Amount,Profit): ")
                    y_cols = [c.strip() for c in raw_cols.split(",") if c.strip()]
                    if not y_cols or len(set(y_cols)) != len(y_cols):
                        print("Enter at least one distinct column.")
                        continue
                    if any(c not in self.df.columns for c in y_cols):
                        print("One or more column names are invalid.")
                        continue
                    if any(not pd.api.types.is_numeric_dtype(self.df[c]) for c in y_cols):
                        print("All selected Y columns must be numeric.")
                        continue
                    data = self.df.groupby(x, dropna=False)[y_cols].sum()
                    if data.empty:
                        print("No data available to plot.")
                        continue
                    plt.figure(figsize=(10, 6))
                    data.plot(kind="area", stacked=True, ax=plt.gca())
                    plt.xlabel(x)
                    plt.ylabel("Total value")
                    plt.title(f"Stacked area plot by {x}")
                    plt.xticks(rotation=45)
                    self._show_figure()

                case "7":
                    break
                case _:
                    print("Invalid choice!")

    def _seaborn_menu(self):
        while True:
            print("""
======================
SEABORN VISUALIZATION
1. Heatmap
2. Box plot
3. Go back
======================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    raw_cols = input(
                        "Enter at least two numeric columns separated by commas "
                        "(e.g. Amount,Profit,Quantity): "
                    )
                    cols = [c.strip() for c in raw_cols.split(",") if c.strip()]
                    if len(cols) < 2 or len(set(cols)) != len(cols):
                        print("Enter at least two distinct columns.")
                        continue
                    if any(c not in self.df.columns for c in cols):
                        print("One or more column names are invalid.")
                        continue
                    if any(not pd.api.types.is_numeric_dtype(self.df[c]) for c in cols):
                        print("All selected columns must be numeric.")
                        continue
                    corr = self.df[cols].corr()
                    if corr.empty:
                        print("Not enough numeric data to calculate correlations.")
                        continue
                    plt.figure(figsize=(10, 6))
                    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
                    plt.title("Correlation Heatmap")
                    self._show_figure()

                case "2":
                    x = self._get_column("Enter numeric column name: ", numeric=True)
                    if x is None:
                        continue
                    values = self.df[x].dropna()
                    if values.empty:
                        print("This column has no data to plot.")
                        continue
                    plt.figure(figsize=(8, 6))
                    sns.boxplot(y=values)
                    plt.ylabel(x)
                    plt.title(f"Box Plot of {x}")
                    self._show_figure()

                case "3":
                    break
                case _:
                    print("Invalid choice!")

    # -------------------- DATAFRAME OPERATIONS --------------------
    def data_operations(self):
        while True:
            if not self._data_ready():
                return

            print("""
=========================
DATAFRAME OPERATIONS
1. Select/display a column
2. Sort data by a column
3. Drop a column
4. Rename a column
5. Display DataFrame
6. Go back
=========================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    col = self._get_column("Enter column name: ")
                    if col is not None:
                        print(self.df[col])

                case "2":
                    col = self._get_column("Enter column name to sort by: ")
                    if col is not None:
                        order = input("Ascending order? (y/n): ").strip().lower()
                        self.df = self.df.sort_values(
                            by=col, ascending=(order != "n"), na_position="last"
                        )
                        print(self.df)

                case "3":
                    col = self._get_column("Enter column name to drop: ")
                    if col is not None:
                        confirm = input(f"Drop '{col}'? (y/n): ").strip().lower()
                        if confirm == "y":
                            self.df.drop(columns=[col], inplace=True)
                            print("Column dropped successfully!")

                case "4":
                    old = self._get_column("Enter current column name: ")
                    if old is None:
                        continue
                    new = input("Enter new column name: ").strip()
                    if not new:
                        print("New column name cannot be empty.")
                    elif new in self.df.columns:
                        print("A column with that name already exists.")
                    else:
                        self.df.rename(columns={old: new}, inplace=True)
                        print("Column renamed successfully!")

                case "5":
                    print(self.df)

                case "6":
                    break
                case _:
                    print("Invalid choice!")

    # -------------------- STATISTICS --------------------
    def statistic_aggregate(self):
        while True:
            if not self._data_ready():
                return

            print("""
========================================
DESCRIPTIVE STATISTICS
1. Find mean
2. Find standard deviation
3. Find minimum
4. Find maximum (also display matching rows)
5. Find sum
6. Find variance
7. Find median
8. Go back
========================================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    operation = "mean"
                case "2":
                    operation = "std"
                case "3":
                    operation = "min"
                case "4":
                    operation = "max"
                case "5":
                    operation = "sum"
                case "6":
                    operation = "var"
                case "7":
                    operation = "median"
                case "8":
                    break
                case _:
                    print("Invalid choice!")
                    continue

            col = self._get_column(
                f"Enter numeric column name to calculate {operation}: ",
                numeric=True,
            )
            if col is None:
                continue

            series = self.df[col].dropna()
            if series.empty:
                print("This column has no non-missing values.")
                continue

            if operation == "mean":
                result = series.mean()
            elif operation == "std":
                result = series.std()
            elif operation == "min":
                result = series.min()
            elif operation == "max":
                result = series.max()
            elif operation == "sum":
                result = series.sum()
            elif operation == "var":
                result = series.var()
            else:
                result = series.median()

            print(f"{operation.title()} of {col}: {result}")

            if operation == "max":
                print("Row(s) containing the maximum value:")
                print(self.df[self.df[col] == result])

    # -------------------- NUMPY ANALYSIS --------------------
    def numpy_analysis(self):
        while True:
            if not self._data_ready():
                return

            print("""
==============================
NUMPY ANALYSIS
1. Convert DataFrame to NumPy array
2. Calculate mean of numeric data
3. Calculate median of numeric data
4. Calculate standard deviation of numeric data
5. Indexing (get one cell)
6. Split array by rows
7. Return to main menu
==============================""")
            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    print("DataFrame converted to NumPy array:")
                    print(self.df.to_numpy())

                case "2" | "3" | "4":
                    numeric_data = self.df.select_dtypes(include=[np.number]).to_numpy()
                    if numeric_data.size == 0:
                        print("No numeric columns available.")
                        continue
                    if choice == "2":
                        print(f"Mean: {np.nanmean(numeric_data)}")
                    elif choice == "3":
                        print(f"Median: {np.nanmedian(numeric_data)}")
                    else:
                        print(f"Standard deviation: {np.nanstd(numeric_data)}")

                case "5":
                    array = self.df.to_numpy()
                    print("Array shape:", array.shape)
                    row_text = input("Enter row index (starting at 0): ").strip()
                    col_text = input("Enter column index (starting at 0): ").strip()
                    try:
                        row_index = int(row_text)
                        col_index = int(col_text)
                        if (0 <= row_index < array.shape[0]
                                and 0 <= col_index < array.shape[1]):
                            print("Value:", array[row_index, col_index])
                        else:
                            print("Index out of range.")
                    except ValueError:
                        print("Indices must be integers.")

                case "6":
                    array = self.df.to_numpy()
                    if array.shape[0] == 0:
                        print("No rows available to split.")
                        continue
                    try:
                        num_splits = int(input("Enter number of splits: "))
                        if num_splits <= 0:
                            print("Number of splits must be greater than zero.")
                            continue
                        split_arrays = np.array_split(array, num_splits, axis=0)
                        for i, part in enumerate(split_arrays, start=1):
                            print(f"Split {i}:")
                            print(part)
                    except ValueError:
                        print("Please enter a valid integer.")

                case "7":
                    break
                case _:
                    print("Invalid choice!")

    # -------------------- PIVOT TABLE --------------------
    def pivot_operation(self):
        if not self._data_ready():
            return

        print("\nDataFrame column names:", ", ".join(map(str, self.df.columns)))
        index_col = input("Enter column name for index: ").strip()
        values_col = input("Enter column name for values: ").strip()
        agg_func = input(
            "Enter aggregation function (mean, sum, count, max, min): "
        ).strip().lower()

        if index_col not in self.df.columns or values_col not in self.df.columns:
            print("One or both column names do not exist in the dataset.")
            return

        if agg_func not in {"mean", "sum", "count", "max", "min"}:
            print("Invalid aggregation function.")
            return

        if agg_func == "mean" and not pd.api.types.is_numeric_dtype(self.df[values_col]):
            print("Mean requires a numeric values column.")
            return

        try:
            pivot = pd.pivot_table(
                self.df,
                index=index_col,
                values=values_col,
                aggfunc=agg_func,
                dropna=False,
            )
            print("\n--- PIVOT TABLE RESULT ---")
            print(pivot)
        except Exception as e:
            print(f"Error creating pivot table: {e}")

    # -------------------- MAIN MENU --------------------
    def run(self):
        while True:
            print("""
================================================
WELCOME TO DATA ANALYSIS & VISUALIZATION PROGRAM
1. Load dataset
2. Explore data
3. Perform DataFrame operations
4. Handle missing data
5. Mathematical and descriptive statistics
6. Data visualization
7. Save visualization
8. NumPy analysis
9. Pivot operation
10. Exit
================================================""")
            choice = input("Please enter your choice: ").strip()

            match choice:
                case "1":
                    self.load_data()
                case "2":
                    self.explore_data()
                case "3":
                    self.data_operations()
                case "4":
                    self.handling_missing()
                case "5":
                    self.statistic_aggregate()
                case "6":
                    self.visualization()
                case "7":
                    self.save_visual()
                case "8":
                    self.numpy_analysis()
                case "9":
                    self.pivot_operation()
                case "10":
                    print("Exiting program. Goodbye!")
                    plt.close("all")
                    break
                case _:
                    print("Invalid choice! Please select 1-10.")


if __name__ == "__main__":
    analyzer = SalesDataAnalyzer()
    analyzer.run()
