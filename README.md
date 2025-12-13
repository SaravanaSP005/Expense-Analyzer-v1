**Expense Analyzer v1**

Expense Analyzer v1 is a simple tool to manage shared expenses among users. It allows you to add users, upload expenses via Excel, and automatically calculate how expenses should be split. Additionally, it supports real-time expense tracking and email notifications for users.

**Features**

User Management: Add and manage users in the database.

Excel Upload: Prepare and upload expenses in an Excel file.

Expense Splitting: Automatically calculates how expenses are split among users.

Real-Time Updates: Users in the database receive updates as new expenses are added.

Email Notifications: Send emails to users with expense summaries.

Example Excel Format
Date	Description	Amount	Paid By	Shared With
2025-12-01	Groceries	100	Alice	Alice, Bob, Carol
2025-12-02	Dinner	60	Bob	Bob, Alice
2025-12-03	Utilities	150	Carol	Alice, Bob, Carol

Date: Date of the expense.

Description: Short description of the expense.

Amount: Total amount of the expense.

Paid By: User who paid the expense.

Shared With: Users sharing the expense (comma-separated).

Getting Started
Prerequisites

Python 3.x

pip (Python package manager)

SMTP server credentials for email notifications

Database setup (e.g., SQLite, MySQL, or PostgreSQL)

Installation
using git clone and branch Dev

Navigate to the project directory:

cd expense-analyzer-

**
Install dependencies:
**
pip install -r requirements.txt

Usage

Add users to the database.

Prepare your expense Excel file following the required format.

Upload the Excel file via the system interface.

View calculated splits for each user.

Users receive real-time updates and emails when new expenses are added.

**Contributing**

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

**License**

This project is licensed under the MIT License.
