# Bike Sharing Systems

This project allows you to explore data related to bike share systems for three major cities in the United States: **Chicago**, **New York City**, and **Washington**.

## Installation

### Prerequisite:
- You need Python installed on your system to run the scripts.

### Steps to Install:

1. Clone the repository: `git clone https://github.com/leaaumagy/Bike_share_systems.git`
2. Navigate to the project directory: `cd Bike_share_systems`
3. Unzip the folder Bike_raw_data, which contains the necessary data files.
4. Run the analysis script to investigate the datasets: `python bike_investigator.py`
5. Run the test script to test functions in the analysis file: `python test_bike_investigator.py`
6. Follow the instructions in the terminal to explore the datasets.

## Project Overview
In this project, you'll investigate bike share usage in Chicago, New York City, and Washington by computing various descriptive statistics.

### The Analysis Includes:

1. Popular Times of Travel:
  - Most common month
  - Most common day of the week
  - Most common hour of the day

2. Popular Stations and Trips:
  - Most common start station
  - Most common end station
  - Most common trip from start to end

3. Trip Duration:
  - Total travel time
  - Average travel time

4. User Information:
  - Counts of each user type (Subscriber, Customer)
  - Counts of gender (available only for NYC and Chicago)
  - Earliest, most recent, and most common birth year (available only for NYC and Chicago)

5. Null Values:
  - Count of null values for each variable in the datasets.

## Guidelines
To answer these questions using Python, the project contains a Python script, bike_investigator.py, with helper code and comments, to process the datasets. Additionally, there is a test_bike_investigator.py file, which evaluates the performance of the script. This ensures that the analysis can be adapted to other datasets with similar variables and the same units, or to continue analyzing the database as it evolves.

### Data Files:
You will need three dataset files located in the ZIP folder Bike_raw_data:

- **chicago.csv**
- **new_york_city.csv**
- **washington.csv**

### Data Sets
The datasets were sourced from Capital Bikeshare and cover the first six months of 2017. All data files contain the same six core columns:

- **Start Time** (e.g., 23/06/2017 15:09:32)
- **End Time** (e.g., 23/06/2017 15:14:53)
- **Trip Duration** (in seconds)
- **Start Station** (e.g., Wood St & Hubbard St)
- **End Station** (e.g., Damen Ave & Chicago Ave)
- **User Type** (Subscriber or Customer)
