Expense Analyzer v1

Expense Analyzer v1 is a simple tool to manage shared expenses among users. It allows you to add users, upload expenses via Excel, and automatically calculate how expenses should be split. Additionally, it supports sending email notifications with expense summaries.

Features

User Management: Add and manage users locally (currently not connected to a database).

Excel Upload: Prepare and upload expenses using an Excel file.

Expense Splitting: Automatically calculates how expenses are split among users.

Email Notifications: Send emails to users with expense summaries.

Note: Database connection and real-time updates are not implemented in this version.

Example Excel Format
Date	Description	Amount	Paid By	Shared With
2025-12-01	Groceries	100	Alice	Alice, Bob, Carol
2025-12-02	Dinner	60	Bob	Bob, Alice
2025-12-03	Utilities	150	Carol	Alice, Bob, Carol

Columns:

Date: Date of the expense

Description: Short description of the expense

Amount: Total amount of the expense

Paid By: User who paid the expense

Shared With: Users sharing the expense (comma-separated)

Getting Started
Prerequisites

Python 3.x

pip (Python package manager)

SMTP server credentials for email notifications

Installation

Clone the repository:

git clone https://github.com/SaravanaSP005/Expense-Analyzer-v1.git
cd Expense-Analyzer-v1


Install dependencies:

pip install -r requirements.txt

Usage

Add users to the system (locally, no database).

Prepare your expense Excel file following the required format.

Upload the Excel file via the system interface.

View calculated splits for each user.

Users receive email notifications with expense summaries.

Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

License

This project is licensed under the MIT License.