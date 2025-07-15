
# ⚽ Ball Stats - Live Football Stats & News

A modern, responsive football statistics dashboard with live matches, league standings, and news.

![Dashboard Screenshot](static/images/screenshot-5.png)
![Dashboard Screenshot](static/images/screenshot-4.png)
![Dashboard Screenshot](static/images/screenshot-3.png)
![Dashboard Screenshot](static/images/screenshot-2.png)
![Dashboard Screenshot](static/images/screenshot-1.png)

## Features

- 📅 Upcoming matches (next 7 days)
- 📊 League standings with team statistics
- 📰 Latest football news from NewsAPI
- 🔐 User authentication (login/register)
- 🎨 Dark theme with glass morphism effects
- 📱 Fully responsive design

## Technologies

- Python 3.10+
- Flask (Backend)
- SQLAlchemy (Database)
- Tailwind CSS (Styling)
- Football Data API (Match data)
- NewsAPI (News articles)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ball-stats.git
   cd ball-stats
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:
   ```bash
   cp .env.example .env
   ```

5. Then add your API keys:
   ```text
   FOOTBALL_DATA_API_KEY=your_api_key_here
   NEWS_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

6. Run the application:
   ```bash
   python app.py
   ```

Access the dashboard at: [http://localhost:5000](http://localhost:5000)

## API Keys

You'll need to obtain:

- Football Data API Key
- NewsAPI Key

## Project Structure

```
ball-stats/
├── app.py                # Main application
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── static/               # Static files
│   └── images/           # Logo and screenshots
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Matches view
│   ├── standings.html    # Standings view
│   ├── news.html         # News view
│   ├── login.html        # Login page
│   └── register.html     # Registration page
└── README.md             # This file
```

## Deployment

For production deployment, consider using:

- Render
- PythonAnywhere
- Heroku

Example for Render:
```bash
# Create a Procfile
echo "web: gunicorn app:app" > Procfile
```

## License

MIT License - See LICENSE for details.

---

### Additional Notes:

1. Make sure to:
   - Create a `static/images/` directory and add your logo there
   - Create an `.env.example` file with placeholder values
   - Add a screenshot to `static/images/` for your README

2. For production:
   - Consider adding rate limiting
   - Implement proper error handling
   - Set up database backups

3. The `.gitignore` file will:
   - Exclude sensitive data
   - Ignore Python cache files
   - Skip virtual environment files
   - Exclude local databases
