# Crew Brief

Add user-friendly Excel file for user events from JSON.

## Python 3

### Reshaping and Filtering

- Some dicts with keys that should be values are reshaped.
- Fix integers and floats stored as strings in JSON.
- `eventDetails` transformed into header and values rows to avoid excessive width.
- Empty container values in `eventDetails` are filtered out.
- Status field color highlighted.
- Sorting `eventDetails` keys.
- Bulleted lists for cells.
- Original JSON in right-aligned column.
- Number and datetime formatting.
- Styling headers and values.

### Problems

- Some resizing doesn't look good, usually for rows and columns that are hard to resize in Excel itself.
