import pandas as pd

def process_expenses(file_path):
    # Read Excel or CSV
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Detailed Table construction
    detailed_rows = []
    person_totals = {}

    for _, row in df.iterrows():
        sno = row["SNo"]
        date = row["Date"]
        expense = row["Expences"]
        amount = float(row["Amount"])
        persons = [p.strip() for p in row["PersonList"].split(",")]
        count = int(row["Person Count"])
        share = round(amount / count, 2)

        # Store for detailed table
        detailed_rows.append([
            sno, date, expense, amount,
            ",".join(persons), count, share
        ])

        # Add to each person’s total
        for p in persons:
            person_totals[p] = person_totals.get(p, 0) + share

    # Convert to DataFrame for pretty table
    detailed_df = pd.DataFrame(detailed_rows, columns=[
        "SNo", "Date", "Expences", "Amount",
        "PersonList", "Person Count", "Individual Share"
    ])

    # Total Expenses
    total_expenses = detailed_df["Amount"].sum()

    # Expense Breakdown
    breakdown_lines = []
    for _, row in df.iterrows():
        amount = float(row["Amount"])
        persons = [p.strip() for p in row["PersonList"].split(",")]
        count = len(persons)
        share = round(amount / count, 2)
        shares_str = ", ".join([f"{p}={share:.2f}" for p in persons])
        breakdown_lines.append(f"{count} [{','.join(persons)}] → {shares_str}")

    # Validation and Counting
    mismatch_rows = []
    total_person_count = 0
    total_person_list_count = 0

    for index, row in df.iterrows():
        person_list = [p.strip() for p in row["PersonList"].split(",")]
        declared_count = int(row["Person Count"])
        actual_count = len(person_list)

        total_person_count += declared_count
        total_person_list_count += actual_count

        if declared_count != actual_count:
            mismatch_rows.append(f"Row {index + 1}: Declared={declared_count}, Actual={actual_count}, List={person_list}")

    # Build Output
    output = []
    output.append("Detailed Table:\n")
    output.append(detailed_df.to_string(index=False))
    output.append(f"\n\nTotal Expenses: {total_expenses:.2f}\n")
    output.append("Expense Breakdown:")
    output.extend(breakdown_lines)

    output.append(f"\n\nTotal 'Person Count' sum: {total_person_count}")
    output.append(f"Total 'PersonList' count: {total_person_list_count}")

    if mismatch_rows:
        output.append("\ Mismatched Rows:")
        output.extend(mismatch_rows)
    else:
        output.append("\n All 'Person Count' values match 'PersonList' counts.")

    output.append("\n\nTotal per Person:")
    for person, total in person_totals.items():
        output.append(f"{person}: {total:.2f}")

    return "\n".join(output)