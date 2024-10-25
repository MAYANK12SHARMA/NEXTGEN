<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exploratory Data Analysis Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        h1 {
            text-align: center;
            color: #4CAF50;
        }

        h2 {
            color: #4CAF50;
            margin-top: 40px;
        }

        .container {
            width: 80%;
            margin: 0 60px 0 50px;
            padding: 20px;
            border-radius: 8px;
        }

        .Logo-container {
            width: 100%;
            margin: 50px 0;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        .logo {
            text-align: center;
            margin-bottom: 20px;
            margin-top: 20px;
        }

        .img-logo {
            width: 150px;
            height: auto;
        }

        hr {
            margin: 30px 0;
            border: 1px solid #ddd;
        }

        .table-of-contents {
            list-style-type: none;
            padding: 0;
        }

        .table-of-contents li {
            margin: 10px 0;
        }

        .table-of-contents a {
            text-decoration: none;
            color: #4CAF50;
        }

        .table-of-contents a:hover {
            text-decoration: underline;
        }

        .gap {
            margin-top: 50px;
            margin-bottom: 50px;
            height: 500px;
        }

        .developer {
            text-align: center;
            margin-top: 10px;
            font-size: 16px;
            color: #a30e0e;
        }

        .Toc-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        h1 {
            text-align: center;
            color: #8B0000;
            margin-bottom: 30px;
        }

        h2 {
            color: #8B0000;
            margin-top: 20px;
            font-size: 18px;
        }



        .table-of-contents-toc {
            list-style-type: none;
            padding: 0;
        }

        .table-of-contents-toc li {
            margin-bottom: 10px;
        }

        .Theading-toc,
        .Theading-toc-table {
            color: #8B0000;
            font-style: italic;
            font-family: 'Times New Roman', Times, serif;

        }

        .Toc {
            color: #8B0000;
            font-style: italic;
            font-family: 'Times New Roman', Times, serif;
            font-size: 18px;
        }

        table {
            width: 90%;
            border-collapse: collapse;
            margin: 20px 0;
            padding-left: 10px;
            margin-left: 15px;
        }

        th,
        td {
            border: 1px solid #675353;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }

        .table_container h2 {
            color: #333;
        }
    </style>

</head>

<body>

    <div class="container">
        <div class="gap" style="height: 100px;"></div>
        <div class="Logo-container">
            <div class="logo">
                <img src="Visualization\Images\logo.png" class="img-logo" alt="Logo">
                <h1>Exploratory Data Analysis Report</h1>
                <div class="developer">Developed by: Mayank Sharma & Garvit Kedia</div>
                <!-- Add your developer's name here -->
            </div>
        </div>
        <div class="gap" style="height:300px;"></div>
    </div>
    <div class="gap" style="height: 20px;"></div>
    <div class="Toc-container">
        <h1 class="Theading-toc">Table of Contents</h1>
        <div style="width: 100%;border-top: 3px solid black;"></div>
        <ul class="table-of-contents-toc">
            <li>
                <h2>1. <span class="Toc">Dataset
                        Overview...................................................................................................
                        Page : 1</span>
                </h2>
            </li>
            <li>
                <h2>2. <span class="Toc">Missing
                        Values......................................................................................................
                        page : 2</span>
                </h2>
            </li>
            <li>
                <h2>3. <span class="Toc">Summary Statistics for Numerical
                        Features....................................................... page : 3</span>
                </h2>
            </li>
            <li>
                <h2>4. <span class="Toc">Correlation
                        Matrix................................................................................................
                        page : 4</span>
                </h2>
            </li>
            <li>
                <h2>5. <span class="Toc">Outliers Summary
                        ................................................................................................
                        page : 5</span>
                </h2>
            </li>
            <li>
                <h2>6. <span class="Toc">Duplicates Columns
                        ............................................................................................
                        page : 6</span>
                </h2>
            </li>

        </ul>
    </div>
    <div class="gap" style="height: 400px;"></div>

    <div class="table_container">
        <h2 class="Theading-toc-table">Dataset Overview</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>
        <table>
            <tr>
                <th>Statistic</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Shape (Rows, Columns)</td>
                <td>
                    I1Shape_(rows, columns)
                    </td>
            </tr>
            <tr>
                <td>Data Types</td>
                <td>
                I2Data_Types
                </td>
            </tr>

        </table>

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Missing Values</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>


            II_Missing_Values


        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Summary Statistics for Numerical Features</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>

        III_Summary_Numerical_Statistics

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Correlation Matrix</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>

        IV_Correlation_Matrix

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Outliers Summary</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>

        V_Outlier_Summary

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Duplicates</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>

        VI_Duplicates_Summary


    </div>

</body>

</html>
