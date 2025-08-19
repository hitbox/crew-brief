# Crew Brief

## JSON to User-Friendly Excel

A user-friendly Excel file for user events derived from JSON.

This tool updates ZIP files with a new user-friendly Excel file, which flattens the original JSON data.

### Features

- Reshapes dictionaries where keys should be values.
- Converts integers and floats stored as strings in the JSON to their proper types.
- Transforms the `eventDetails` field into header and value rows to avoid excessive width.
- Filters out empty container values in `eventDetails`.
- Highlights the status field with color.
- Sorts the keys in `eventDetails`.
- Adds bulleted lists to relevant cells.
- Places the original JSON in a right-aligned column.
- Applies number and datetime formatting.
- Styles headers and values for clarity and readability.
- Retains original ZIP file metadata and updates the access time (atime) and modification time (mtime).

### Problems

- Sometimes fields like "status" are missing from `userEvent`.
- Excel does not support microseconds, so they are lost during writing.
- Row and column resizing in Excel may not look great, particularly for those that are hard to resize manually.

## File Processing

- Track files in directories.
- Parse filenames and contents for leg identifier information.
- Group files by subset of leg identifier information. Some files have more complete info.
- Append all non-zip files to all the zip files.


### Notes

- Careful synchronization between regexes with capture groups and Marshmallow schemas.
