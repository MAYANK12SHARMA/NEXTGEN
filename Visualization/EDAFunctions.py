import pandas as pd
from scipy import stats
import numpy as np


def Dataset_Overview(df):
    """
    Analyzes the given pandas DataFrame and returns a list containing:
    - Shape of the DataFrame (rows, columns)
    - Unique data types of columns in a specific format
    - Number of columns

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    list: A list containing (shape, unique datatypes, number of columns).
    """
    shape = df.shape                          # Get shape (rows, columns)
    unique_dtypes = df.dtypes.unique()        # Get unique data types
    formatted_dtypes = [str(dtype) for dtype in unique_dtypes]  # Convert to string format
    
    return [shape, formatted_dtypes]



def missing_values_report(df):
    """
    Analyzes the given pandas DataFrame and returns a list of sublists containing:
    - Column Name
    - Total Missing Values
    - Percentage Missing

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    list: A list of sublists containing [Column Name, Total Missing Values, Percentage Missing].
    """
    report = []  # Initialize the report list
    total_rows = df.shape[0]  # Total number of rows

    for column in df.columns:
        total_missing = df[column].isnull().sum()  # Total missing values in the column
        percentage_missing = (total_missing / total_rows) * 100  # Calculate percentage missing
        report.append([column, total_missing, percentage_missing])  # Append sublist to report

    return report

def missing_values_report_html(df):
    """
    Analyzes the given pandas DataFrame and returns an HTML string containing:
    - Column Name
    - Total Missing Values
    - Percentage Missing in an HTML table format.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    str: An HTML string containing the table of missing values information.
    """
    total_rows = df.shape[0]  # Total number of rows

    # Start the HTML string with the table headers
    html_output = """
    <table>
        <tr>
            <th>Column Name</th>
            <th>Total Missing Values</th>
            <th>Percentage Missing</th>
        </tr>
    """

    # Iterate through columns and format each row in HTML
    for column in df.columns:
        total_missing = df[column].isnull().sum()
        percentage_missing = (total_missing / total_rows) * 100
        # Add the HTML row for the current column
        html_output += f"""
        <tr>
            <td>{column}</td>
            <td>{total_missing}</td>
            <td>{percentage_missing:.1f}%</td>
        </tr>
        """

    # Close the HTML table
    html_output += "</table>"

    return html_output


def random_numerical_statistics(df):
    """
    Selects three random numerical columns from the DataFrame and computes various statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    list: A list containing [Statistic, Column A, Column B, Column C].
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Check if there are at least three numerical columns
    if len(numerical_cols) < 3:
        raise ValueError("The DataFrame must contain at least three numerical columns.")

    # Randomly select three columns
    selected_columns = np.random.choice(numerical_cols, size=3, replace=False)

    # Calculate statistics for the selected columns
    statistics = {
        'Count': [df[col].count() for col in selected_columns],
        'Mean': [df[col].mean() for col in selected_columns],
        'Standard Deviation': [df[col].std() for col in selected_columns],
        'Minimum': [df[col].min() for col in selected_columns],
        'Q1': [df[col].quantile(0.25) for col in selected_columns],
        'Median (Q2)': [df[col].median() for col in selected_columns],
        'Q3': [df[col].quantile(0.75) for col in selected_columns],
        'Maximum': [df[col].max() for col in selected_columns]
    }

    # Create the result list with the header
    result = [['Statistic', selected_columns[0], selected_columns[1], selected_columns[2]]]
    for stat_name, stat_values in statistics.items():
        # Format the values to 2 decimal places
        formatted_values = [f"{value:.2f}" if isinstance(value, float) else value for value in stat_values]
        result.append([stat_name] + formatted_values)

    return result

import numpy as np

def random_numerical_statistics_html(df):
    """
    Selects three random numerical columns from the DataFrame and computes various statistics,
    then returns the results as an HTML string in a table format.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    str: An HTML string containing the table of statistics for three random numerical columns.
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Check if there are at least three numerical columns
    if len(numerical_cols) < 3:
        raise ValueError("The DataFrame must contain at least three numerical columns.")

    # Randomly select three columns
    selected_columns = np.random.choice(numerical_cols, size=3, replace=False)

    # Calculate statistics for the selected columns
    statistics = {
        'Count': [df[col].count() for col in selected_columns],
        'Mean': [df[col].mean() for col in selected_columns],
        'Standard Deviation': [df[col].std() for col in selected_columns],
        'Minimum': [df[col].min() for col in selected_columns],
        'Q1': [df[col].quantile(0.25) for col in selected_columns],
        'Median (Q2)': [df[col].median() for col in selected_columns],
        'Q3': [df[col].quantile(0.75) for col in selected_columns],
        'Maximum': [df[col].max() for col in selected_columns]
    }

    # Start the HTML table with headers
    html_output = f"""
    <table>
        <tr>
            <th>Statistic</th>
            <th>{selected_columns[0]}</th>
            <th>{selected_columns[1]}</th>
            <th>{selected_columns[2]}</th>
        </tr>
    """

    # Populate the table rows with statistics
    for stat_name, stat_values in statistics.items():
        # Format the values to 2 decimal places if they are floats
        formatted_values = [f"{value:.2f}" if isinstance(value, float) else value for value in stat_values]
        html_output += f"""
        <tr>
            <td>{stat_name}</td>
            <td>{formatted_values[0]}</td>
            <td>{formatted_values[1]}</td>
            <td>{formatted_values[2]}</td>
        </tr>
        """

    # Close the HTML table
    html_output += "</table>"

    return html_output


def random_correlation_matrix(df):
    """
    Selects three random numerical columns from the DataFrame and computes their correlation matrix.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    list: A list containing the correlation matrix with headers.
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Check if there are at least three numerical columns
    if len(numerical_cols) < 3:
        raise ValueError("The DataFrame must contain at least three numerical columns.")

    # Randomly select three columns
    selected_columns = np.random.choice(numerical_cols, size=3, replace=False)

    # Calculate the correlation matrix for the selected columns
    correlation_matrix = df[selected_columns].corr()

    # Convert the correlation matrix to a list of lists, including headers
    result = correlation_matrix.round(2).values.tolist()  # Round values to 2 decimal places
    
    # Add headers to the result
    header = [''] + list(selected_columns)  # Create header row
    result.insert(0, header)  # Insert header at the top
    
    # Append the selected columns as labels for the rows
    for i, col in enumerate(selected_columns):
        result[i + 1].insert(0, col)  # Add column label to each row

    return result

import numpy as np

def random_correlation_matrix_html(df):
    """
    Selects three random numerical columns from the DataFrame and computes their correlation matrix,
    returning the results as an HTML string in a table format.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    str: An HTML string containing the correlation matrix with headers.
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Check if there are at least three numerical columns
    if len(numerical_cols) < 3:
        raise ValueError("The DataFrame must contain at least three numerical columns.")

    # Randomly select three columns
    selected_columns = np.random.choice(numerical_cols, size=3, replace=False)

    # Calculate the correlation matrix for the selected columns
    correlation_matrix = df[selected_columns].corr()

    # Start the HTML output with the table headers
    html_output = """
    <table>
        <tr>
            <th></th>
            <th>{col1}</th>
            <th>{col2}</th>
            <th>{col3}</th>
        </tr>
    """.format(col1=selected_columns[0], col2=selected_columns[1], col3=selected_columns[2])

    # Populate the rows of the correlation matrix in HTML
    for i, row_name in enumerate(selected_columns):
        html_output += f"<tr><td>{row_name}</td>"
        for j in range(len(selected_columns)):
            value = correlation_matrix.iloc[i, j]
            html_output += f"<td>{value:.2f}</td>"  # Round to 2 decimal places
        html_output += "</tr>"

    # Close the HTML table
    html_output += "</table>"

    return html_output



def outlier_summary(df, z_threshold=3):
    """
    Generates a summary of outliers in the DataFrame using Z-score and IQR methods.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    z_threshold (float): The Z-score threshold for determining outliers.

    Returns:
    list: A list containing sublists in the format 
          [columns, Z-score method (no. of outliers), IQR (no. of outliers)].
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Initialize the result list
    result = [['Columns', 'Z-score method (no. of outliers)', 'IQR (no. of outliers)']]

    for col in numerical_cols:
        # Z-score method
        z_scores = np.abs(stats.zscore(df[col], nan_policy='omit'))  # Calculate Z-scores
        z_outliers = np.sum(z_scores > z_threshold)  # Count outliers based on Z-score

        # IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR  # Lower bound for outliers
        upper_bound = Q3 + 1.5 * IQR  # Upper bound for outliers
        iqr_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]  # Count IQR outliers

        # Append the summary for the current column
        result.append([col, z_outliers, iqr_outliers])

    return result


from scipy import stats
import numpy as np

def outlier_summary_html(df, z_threshold=3):
    """
    Generates a summary of outliers in the DataFrame using Z-score and IQR methods
    and returns the results as an HTML string in a table format.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    z_threshold (float): The Z-score threshold for determining outliers.

    Returns:
    str: An HTML string containing the table of outlier summary.
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Start the HTML output with the table headers
    html_output = """
    <table>
        <tr>
            <th>Column Name</th>
            <th>Outlier Detection Method</th>
            <th>Number of Outliers</th>
        </tr>
    """

    # Calculate the outliers using both Z-score and IQR methods for each column
    for col in numerical_cols:
        # Z-score method
        z_scores = np.abs(stats.zscore(df[col], nan_policy='omit'))
        z_outliers = np.sum(z_scores > z_threshold)

        # IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        iqr_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]

        # Append the Z-score method row
        html_output += f"""
        <tr>
            <td>{col}</td>
            <td>Z-score</td>
            <td>{z_outliers}</td>
        </tr>
        """

        # Append the IQR method row
        html_output += f"""
        <tr>
            <td>{col}</td>
            <td>IQR Method</td>
            <td>{iqr_outliers}</td>
        </tr>
        """

    # Close the HTML table
    html_output += "</table>"

    return html_output


def duplicate_summary(df):
    """
    Generates a summary of duplicate entries in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    list: A list containing sublists in the format 
          [columns, Total Duplicates].
    """
    # Initialize the result list
    result = [['Columns', 'Total Duplicates']]

    # Iterate through each column to count duplicates
    for col in df.columns:
        total_duplicates = df[col].duplicated(keep=False).sum()  # Count duplicates for each column
        result.append([col, total_duplicates])

    return result

def duplicate_summary_html(df):
    """
    Generates a summary of duplicate entries in the DataFrame, including total duplicates and 
    the percentage of duplicates for each column, returning the results as an HTML string.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    str: An HTML string containing a table with duplicate summary.
    """
    # Calculate the total number of rows for percentage calculation
    total_rows = len(df)
    
    # Initialize the HTML output with table headers
    html_output = """
    <table>
        <tr>
            <th>Column Name</th>
            <th>Total Duplicates</th>
            <th>Percentage of Duplicates</th>
        </tr>
    """

    # Iterate through each column to count duplicates
    for col in df.columns:
        total_duplicates = df[col].duplicated(keep=False).sum()  # Count duplicates for each column
        percentage_duplicates = (total_duplicates / total_rows) * 100  # Calculate percentage

        # Append the column's duplicate summary to the HTML table
        html_output += f"""
        <tr>
            <td>{col}</td>
            <td>{total_duplicates}</td>
            <td>{percentage_duplicates:.2f}%</td>
        </tr>
        """

    # Close the HTML table
    html_output += "</table>"

    return html_output
