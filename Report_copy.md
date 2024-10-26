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
                <img src="logo.png" class="img-logo" alt="Logo">
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
(483, 28)                    </td>
            </tr>
            <tr>
                <td>Data Types</td>
                <td>
['int64', 'float64']                </td>
            </tr>

        </table>

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Missing Values</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>



    <table>
        <tr>
            <th>Column Name</th>
            <th>Total Missing Values</th>
            <th>Percentage Missing</th>
        </tr>
    
        <tr>
            <td>Well</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>BHP</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>RP</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>LFR</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>TS</td>
            <td>1</td>
            <td>0.2%</td>
        </tr>
        
        <tr>
            <td>GF</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>SP</td>
            <td>7</td>
            <td>1.4%</td>
        </tr>
        
        <tr>
            <td>WC</td>
            <td>7</td>
            <td>1.4%</td>
        </tr>
        
        <tr>
            <td>Po</td>
            <td>7</td>
            <td>1.4%</td>
        </tr>
        
        <tr>
            <td>PermR</td>
            <td>7</td>
            <td>1.4%</td>
        </tr>
        
        <tr>
            <td>PI</td>
            <td>7</td>
            <td>1.4%</td>
        </tr>
        
        <tr>
            <td>BC</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>ER</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>DT</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td> NWBZ</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td> FZ, </td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>PiezC</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>FD</td>
            <td>1</td>
            <td>0.2%</td>
        </tr>
        
        <tr>
            <td>PipDT</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>BP</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>OV</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>OCF</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>VC</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>THA</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>FR</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>WR</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>DOP</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        
        <tr>
            <td>Permeability</td>
            <td>0</td>
            <td>0.0%</td>
        </tr>
        </table>

        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Summary Statistics for Numerical Features</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>


    <table>
        <tr>
            <th>Statistic</th>
            <th>FD</th>
            <th>PipDT</th>
            <th>BP</th>
        </tr>
    
        <tr>
            <td>Count</td>
            <td>482</td>
            <td>483</td>
            <td>483</td>
        </tr>
        
        <tr>
            <td>Mean</td>
            <td>0.86</td>
            <td>1973.42</td>
            <td>3.52</td>
        </tr>
        
        <tr>
            <td>Standard Deviation</td>
            <td>0.12</td>
            <td>183.51</td>
            <td>0.87</td>
        </tr>
        
        <tr>
            <td>Minimum</td>
            <td>0.68</td>
            <td>1486.00</td>
            <td>1.78</td>
        </tr>
        
        <tr>
            <td>Q1</td>
            <td>0.76</td>
            <td>1835.00</td>
            <td>2.68</td>
        </tr>
        
        <tr>
            <td>Median (Q2)</td>
            <td>0.82</td>
            <td>2000.00</td>
            <td>3.20</td>
        </tr>
        
        <tr>
            <td>Q3</td>
            <td>0.97</td>
            <td>2124.00</td>
            <td>4.40</td>
        </tr>
        
        <tr>
            <td>Maximum</td>
            <td>1.18</td>
            <td>2457.00</td>
            <td>4.60</td>
        </tr>
        </table>
        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Correlation Matrix</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>


    <table>
        <tr>
            <th></th>
            <th>PermR</th>
            <th>GF</th>
            <th>BHP</th>
        </tr>
    <tr><td>PermR</td><td>1.00</td><td>-0.02</td><td>0.07</td></tr><tr><td>GF</td><td>-0.02</td><td>1.00</td><td>0.35</td></tr><tr><td>BHP</td><td>0.07</td><td>0.35</td><td>1.00</td></tr></table>
        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Outliers Summary</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>


    <table>
        <tr>
            <th>Column Name</th>
            <th>Outlier Detection Method</th>
            <th>Number of Outliers</th>
        </tr>
    
        <tr>
            <td>Well</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>Well</td>
            <td>IQR Method</td>
            <td>14</td>
        </tr>
        
        <tr>
            <td>BHP</td>
            <td>Z-score</td>
            <td>7</td>
        </tr>
        
        <tr>
            <td>BHP</td>
            <td>IQR Method</td>
            <td>54</td>
        </tr>
        
        <tr>
            <td>RP</td>
            <td>Z-score</td>
            <td>3</td>
        </tr>
        
        <tr>
            <td>RP</td>
            <td>IQR Method</td>
            <td>44</td>
        </tr>
        
        <tr>
            <td>LFR</td>
            <td>Z-score</td>
            <td>3</td>
        </tr>
        
        <tr>
            <td>LFR</td>
            <td>IQR Method</td>
            <td>12</td>
        </tr>
        
        <tr>
            <td>TS</td>
            <td>Z-score</td>
            <td>4</td>
        </tr>
        
        <tr>
            <td>TS</td>
            <td>IQR Method</td>
            <td>4</td>
        </tr>
        
        <tr>
            <td>GF</td>
            <td>Z-score</td>
            <td>4</td>
        </tr>
        
        <tr>
            <td>GF</td>
            <td>IQR Method</td>
            <td>12</td>
        </tr>
        
        <tr>
            <td>SP</td>
            <td>Z-score</td>
            <td>1</td>
        </tr>
        
        <tr>
            <td>SP</td>
            <td>IQR Method</td>
            <td>2</td>
        </tr>
        
        <tr>
            <td>WC</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>WC</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>Po</td>
            <td>Z-score</td>
            <td>6</td>
        </tr>
        
        <tr>
            <td>Po</td>
            <td>IQR Method</td>
            <td>22</td>
        </tr>
        
        <tr>
            <td>PermR</td>
            <td>Z-score</td>
            <td>8</td>
        </tr>
        
        <tr>
            <td>PermR</td>
            <td>IQR Method</td>
            <td>68</td>
        </tr>
        
        <tr>
            <td>PI</td>
            <td>Z-score</td>
            <td>13</td>
        </tr>
        
        <tr>
            <td>PI</td>
            <td>IQR Method</td>
            <td>65</td>
        </tr>
        
        <tr>
            <td>BC</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>BC</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>ER</td>
            <td>Z-score</td>
            <td>11</td>
        </tr>
        
        <tr>
            <td>ER</td>
            <td>IQR Method</td>
            <td>83</td>
        </tr>
        
        <tr>
            <td>DT</td>
            <td>Z-score</td>
            <td>1</td>
        </tr>
        
        <tr>
            <td>DT</td>
            <td>IQR Method</td>
            <td>1</td>
        </tr>
        
        <tr>
            <td> NWBZ</td>
            <td>Z-score</td>
            <td>10</td>
        </tr>
        
        <tr>
            <td> NWBZ</td>
            <td>IQR Method</td>
            <td>60</td>
        </tr>
        
        <tr>
            <td> FZ, </td>
            <td>Z-score</td>
            <td>23</td>
        </tr>
        
        <tr>
            <td> FZ, </td>
            <td>IQR Method</td>
            <td>55</td>
        </tr>
        
        <tr>
            <td>PiezC</td>
            <td>Z-score</td>
            <td>11</td>
        </tr>
        
        <tr>
            <td>PiezC</td>
            <td>IQR Method</td>
            <td>70</td>
        </tr>
        
        <tr>
            <td>FD</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>FD</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>PipDT</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>PipDT</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>BP</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>BP</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>OV</td>
            <td>Z-score</td>
            <td>29</td>
        </tr>
        
        <tr>
            <td>OV</td>
            <td>IQR Method</td>
            <td>189</td>
        </tr>
        
        <tr>
            <td>OCF</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>OCF</td>
            <td>IQR Method</td>
            <td>69</td>
        </tr>
        
        <tr>
            <td>VC</td>
            <td>Z-score</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>VC</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>THA</td>
            <td>Z-score</td>
            <td>4</td>
        </tr>
        
        <tr>
            <td>THA</td>
            <td>IQR Method</td>
            <td>4</td>
        </tr>
        
        <tr>
            <td>FR</td>
            <td>Z-score</td>
            <td>9</td>
        </tr>
        
        <tr>
            <td>FR</td>
            <td>IQR Method</td>
            <td>59</td>
        </tr>
        
        <tr>
            <td>WR</td>
            <td>Z-score</td>
            <td>7</td>
        </tr>
        
        <tr>
            <td>WR</td>
            <td>IQR Method</td>
            <td>0</td>
        </tr>
        
        <tr>
            <td>DOP</td>
            <td>Z-score</td>
            <td>14</td>
        </tr>
        
        <tr>
            <td>DOP</td>
            <td>IQR Method</td>
            <td>49</td>
        </tr>
        
        <tr>
            <td>Permeability</td>
            <td>Z-score</td>
            <td>8</td>
        </tr>
        
        <tr>
            <td>Permeability</td>
            <td>IQR Method</td>
            <td>58</td>
        </tr>
        </table>
        <div class="gap" style="height: 30px;"></div>
        <h2 class="Theading-toc-table">Duplicates</h2>
        <div style="width: 100%;border-top: 2px solid black;"></div>


    <table>
        <tr>
            <th>Column Name</th>
            <th>Total Duplicates</th>
            <th>Percentage of Duplicates</th>
        </tr>
    
        <tr>
            <td>Well</td>
            <td>441</td>
            <td>91.30%</td>
        </tr>
        
        <tr>
            <td>BHP</td>
            <td>209</td>
            <td>43.27%</td>
        </tr>
        
        <tr>
            <td>RP</td>
            <td>198</td>
            <td>40.99%</td>
        </tr>
        
        <tr>
            <td>LFR</td>
            <td>197</td>
            <td>40.79%</td>
        </tr>
        
        <tr>
            <td>TS</td>
            <td>459</td>
            <td>95.03%</td>
        </tr>
        
        <tr>
            <td>GF</td>
            <td>469</td>
            <td>97.10%</td>
        </tr>
        
        <tr>
            <td>SP</td>
            <td>472</td>
            <td>97.72%</td>
        </tr>
        
        <tr>
            <td>WC</td>
            <td>303</td>
            <td>62.73%</td>
        </tr>
        
        <tr>
            <td>Po</td>
            <td>463</td>
            <td>95.86%</td>
        </tr>
        
        <tr>
            <td>PermR</td>
            <td>166</td>
            <td>34.37%</td>
        </tr>
        
        <tr>
            <td>PI</td>
            <td>118</td>
            <td>24.43%</td>
        </tr>
        
        <tr>
            <td>BC</td>
            <td>476</td>
            <td>98.55%</td>
        </tr>
        
        <tr>
            <td>ER</td>
            <td>114</td>
            <td>23.60%</td>
        </tr>
        
        <tr>
            <td>DT</td>
            <td>397</td>
            <td>82.19%</td>
        </tr>
        
        <tr>
            <td> NWBZ</td>
            <td>90</td>
            <td>18.63%</td>
        </tr>
        
        <tr>
            <td> FZ, </td>
            <td>76</td>
            <td>15.73%</td>
        </tr>
        
        <tr>
            <td>PiezC</td>
            <td>56</td>
            <td>11.59%</td>
        </tr>
        
        <tr>
            <td>FD</td>
            <td>347</td>
            <td>71.84%</td>
        </tr>
        
        <tr>
            <td>PipDT</td>
            <td>398</td>
            <td>82.40%</td>
        </tr>
        
        <tr>
            <td>BP</td>
            <td>478</td>
            <td>98.96%</td>
        </tr>
        
        <tr>
            <td>OV</td>
            <td>473</td>
            <td>97.93%</td>
        </tr>
        
        <tr>
            <td>OCF</td>
            <td>464</td>
            <td>96.07%</td>
        </tr>
        
        <tr>
            <td>VC</td>
            <td>468</td>
            <td>96.89%</td>
        </tr>
        
        <tr>
            <td>THA</td>
            <td>463</td>
            <td>95.86%</td>
        </tr>
        
        <tr>
            <td>FR</td>
            <td>259</td>
            <td>53.62%</td>
        </tr>
        
        <tr>
            <td>WR</td>
            <td>483</td>
            <td>100.00%</td>
        </tr>
        
        <tr>
            <td>DOP</td>
            <td>424</td>
            <td>87.78%</td>
        </tr>
        
        <tr>
            <td>Permeability</td>
            <td>168</td>
            <td>34.78%</td>
        </tr>
        </table>

    </div>

</body>

</html>
