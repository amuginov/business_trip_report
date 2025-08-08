# Data Directory

This directory contains data files for the Business Trip Report Bot.

## Files included in repository:
- `report_template.xlsx` - Excel template for generating reports
- `order.pdf` - Sample order document for testing
- `sample_pdfs/` - Directory with sample PDF files for testing

## Files created at runtime (ignored by Git):
- `database.db` - SQLite database file (created automatically)
- `generated_report.xlsx` - Generated reports (created by bot)
- `*.pdf` - User-uploaded documents (except samples)

## Note:
The database file (`database.db`) will be created automatically when the bot starts for the first time. Personal documents should not be committed to the repository.
