# Advance Report Bot

This project is a chat bot designed to generate advance reports based on travel orders and ticket information. The bot interacts with users to collect necessary data and produces reports in Excel format.

## Features

- User registration and role management (Admin, Authorized User, Unauthorized User).
- PDF parsing for travel orders and tickets.
- Excel report generation based on parsed data.
- User-friendly interaction through a chat interface.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd advance-report-bot
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the bot, execute the following command:
```
python -m bot.main
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.