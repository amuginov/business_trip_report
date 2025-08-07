# Business Trip Report Bot

A Telegram bot for automating the creation of business trip advance reports. The bot parses PDF files (orders and tickets), extracts necessary data, and generates ready-to-use Excel reports.

## 🚀 Features

- **Role-based system**: Unauthorized users, authorized users, and administrators
- **Automatic PDF parsing**: Extract data from orders and electronic tickets
- **Excel report generation**: Automatic filling of advance report templates
- **User management**: Registration, approval, and user management
- **Multiple ticket support**: Processing multiple tickets within a single business trip

## 📋 Functionality by Role

### Unauthorized User
- Submit registration application
- Get help information

### Authorized User
- Create advance reports
- Upload PDF files (orders and tickets)
- Receive ready Excel reports

### Administrator
- User management (view, delete)
- Approve/reject registration applications
- Create new users directly

## 🛠 Technology Stack

- **Python 3.9+**
- **aiogram** - Telegram Bot API framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database
- **pdfplumber** - PDF file parsing
- **openpyxl** - Excel file operations
- **python-dotenv** - Environment variable management

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/amuginov/business_trip_report.git
cd business_trip_report
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
# or
venv\Scripts\activate  # for Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment variables setup
Create a `.env` file in the project root directory:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

You can get the bot token from [@BotFather](https://t.me/BotFather) in Telegram.

### 5. Create first administrator
Edit the `scripts/create_admin.py` file with your data:
```python
telegram_id = "YOUR_TELEGRAM_ID"  # Your Telegram ID
surname = "Your surname"
name = "Your name"
patronymic_name = "Your patronymic"
email = "your@email.com"
employee_id = "Your employee ID"
employee_organisation = "Your organization"
employee_position = "Your position"
```

Then execute:
```bash
python scripts/create_admin.py
```

### 6. Run the bot
```bash
python -m bot.main
```

## 📁 Project Structure

```
business_trip_report/
├── bot/                          # Main bot code
│   ├── db/                      # Database
│   │   ├── crud.py             # CRUD operations
│   │   └── models.py           # Data models
│   ├── handlers/               # Message handlers
│   │   ├── admin.py           # Administrator functionality
│   │   ├── user.py            # User functionality
│   │   ├── guest.py           # Guest functionality
│   │   └── common.py          # Common handlers
│   ├── keyboards/              # Keyboards
│   ├── parsers/               # PDF file parsers
│   │   ├── order_parser.py    # Order parser
│   │   └── continent_ticket_parser.py  # Ticket parser
│   ├── services/              # Services
│   │   ├── database.py        # Database setup
│   │   ├── excel_generator.py # Excel report generation
│   │   └── user_service.py    # User services
│   ├── states/                # FSM states
│   ├── config.py              # Configuration
│   └── main.py               # Entry point
├── data/                     # Data and files
│   ├── database.db          # SQLite database
│   ├── report_template.xlsx # Report template
│   └── sample_pdfs/         # Sample PDF files
├── scripts/                 # Scripts
│   └── create_admin.py     # Administrator creation
└── requirements.txt        # Dependencies
```

## 🔧 Usage

### For Users

1. **Registration**: Start with `/start` command and submit registration application
2. **Wait for approval**: Wait for administrator approval
3. **Create report**: 
   - Click "Авансовый" button
   - Upload PDF file with order
   - Upload PDF file(s) with tickets
   - Receive ready Excel report

### For Administrators

1. **Application management**: Approve or reject registration applications
2. **User management**: View user list, delete when necessary
3. **User creation**: Create new users directly

## 📄 Supported PDF Formats

### Orders
The bot extracts from orders:
- Order number
- Order date
- Business trip duration (number of days)

### Tickets
The bot supports Continent airline tickets and extracts:
- Ticket purchase date
- Ticket number
- Ticket price

## 🗄 Database

The project uses SQLite with the following tables:
- `users` - User information
- `reports` - User reports
- `tickets` - Ticket data
- `orders` - Order data

## 🚀 Deployment

For server deployment:

1. Ensure all dependencies are installed
2. Configure environment variables
3. Create administrator
4. Run the bot using a process manager (e.g., systemd, supervisor, or PM2)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is created for internal organizational use.

## 👥 Authors

- Azat Muginov - [@amuginov](https://github.com/amuginov)

## 📞 Support

If you have questions or issues, please create an Issue in the GitHub repository.

