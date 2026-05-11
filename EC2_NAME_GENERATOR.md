# EC2 Random Name Generator

A Python command-line tool that generates unique EC2 instance names for teams sharing an AWS environment. Built as my first hands-on Python project.

## What It Does

Several departments often share a single AWS account. Without a clear naming convention, EC2 instances become hard to attribute to the right team. This script generates unique, department-tagged names in the format `Department-XXXXXX`, where the last six characters are random letters and digits.

With 36 possible characters across 6 positions, there are over **2 billion possible combinations** — duplicates are practically impossible.

## Features

- Prompts the user for their department
- Restricts use to allowed departments only (Marketing, Accounting, FinOps)
- Case-insensitive input — `accounting`, `Accounting`, and `ACCOUNTING` all work
- Lets the user specify how many names they need
- Generates unique alphanumeric suffixes for every name
- Politely rejects users from non-allowed departments

## Requirements

- Python 3.x
- The `random` library (built into Python — no install needed)

## How to Run

From the repo root:

    python EC2_Name_Generator.py

Then follow the prompts.

## Example Output

    Welcome to EC2 Name Generator
    Enter your department (Marketing, Accounting, FinOps): Accounting
    How many names would your department like? 3
    Accounting-A4F7B2
    Accounting-X9Q1KM
    Accounting-7BT3LP

If a non-allowed department is entered:

    Welcome to EC2 Name Generator
    Enter your department (Marketing, Accounting, FinOps): Engineering
    Sorry, this Name Generator is only for the Marketing, Accounting, and FinOps departments.

