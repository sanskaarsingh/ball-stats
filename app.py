import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def datetimeformat(value, format='%a, %b %d %H:%M'):
    if value is None:
        return ""
    try:
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime(format)
    except:
        try:
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
            return dt.strftime(format)
        except:
            return value
        
app.jinja_env.filters['datetimeformat'] = datetimeformat


# API configuration
FOOTBALL_API_KEY = os.getenv('FOOTBALL_DATA_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
FOOTBALL_API_URL = 'https://api.football-data.org/v4'
NEWS_API_URL = 'https://newsapi.org/v2/everything'

headers = {'X-Auth-Token': FOOTBALL_API_KEY}

# Supported leagues with their API codes and display names
LEAGUES = {
    # Europe
    'PL': {'name': 'Premier League', 'country': 'England'},
    'ELC': {'name': 'Championship', 'country': 'England'},
    'PD': {'name': 'La Liga', 'country': 'Spain'},
    'SD': {'name': 'Segunda División', 'country': 'Spain'},
    'BL1': {'name': 'Bundesliga', 'country': 'Germany'},
    'BL2': {'name': '2. Bundesliga', 'country': 'Germany'},
    'SA': {'name': 'Serie A', 'country': 'Italy'},
    'SB': {'name': 'Serie B', 'country': 'Italy'},
    'FL1': {'name': 'Ligue 1', 'country': 'France'},
    'FL2': {'name': 'Ligue 2', 'country': 'France'},
    'PPL': {'name': 'Primeira Liga', 'country': 'Portugal'},
    'DED': {'name': 'Eredivisie', 'country': 'Netherlands'},
    'CL': {'name': 'Champions League', 'country': 'Europe'},
    'EL': {'name': 'Europa League', 'country': 'Europe'},
    'ECL': {'name': 'Conference League', 'country': 'Europe'},
    'EC': {'name': 'European Championship', 'country': 'Europe'},
    
    # South America
    'BSA': {'name': 'Brasileirão', 'country': 'Brazil'},
    'CLI': {'name': 'Copa Libertadores', 'country': 'South America'},
    'CSA': {'name': 'Copa Sudamericana', 'country': 'South America'},
    'AG': {'name': 'Liga Profesional', 'country': 'Argentina'},
    'APD': {'name': 'Primera División', 'country': 'Peru'},
    
    # North America
    'MLS': {'name': 'Major League Soccer', 'country': 'USA/Canada'},
    'LMX': {'name': 'Liga MX', 'country': 'Mexico'},
    
    # Asia
    'AAL': {'name': 'A-League', 'country': 'Australia'},
    'JPL': {'name': 'J1 League', 'country': 'Japan'},
    'K1': {'name': 'K League 1', 'country': 'South Korea'},
    'CSL': {'name': 'Super League', 'country': 'China'},
    
    # Africa
    'ACL': {'name': 'CAF Champions League', 'country': 'Africa'},
    
    # International
    'WC': {'name': 'World Cup', 'country': 'International'},
    'FIFA': {'name': 'International Friendlies', 'country': 'International'}
}

def fetch_football_data(endpoint):
    url = f"{FOOTBALL_API_URL}/{endpoint}"
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_news():
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = {
        'q': 'football',
        'from': from_date,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': NEWS_API_KEY,
        'pageSize': 20
    }
    response = requests.get(NEWS_API_URL, params=params)
    return response.json()

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', leagues=LEAGUES)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', leagues=LEAGUES)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    try:
        # Fetch matches for the next 7 days
        date_from = datetime.now().strftime('%Y-%m-%d')
        date_to = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        matches = fetch_football_data(f'matches?dateFrom={date_from}&dateTo={date_to}')
        
        matches_by_competition = {}
        for match in matches.get('matches', []):
            comp_id = match['competition']['code']
            if comp_id in LEAGUES:
                if comp_id not in matches_by_competition:
                    matches_by_competition[comp_id] = {
                        'competition': match['competition'],
                        'matches': []
                    }
                matches_by_competition[comp_id]['matches'].append(match)
        
        # Sort competitions by country and name
        sorted_competitions = sorted(
            matches_by_competition.values(),
            key=lambda x: (LEAGUES[x['competition']['code']]['country'], 
                          LEAGUES[x['competition']['code']]['name'])
        )
        
        return render_template('index.html', 
                             competitions=sorted_competitions,
                             leagues=LEAGUES)
    except Exception as e:
        print(f"Error fetching matches: {e}")
        return render_template('index.html', 
                             competitions=[], 
                             leagues=LEAGUES)

@app.route('/standings')
@login_required
def standings():
    league_code = request.args.get('league', 'PL')  # Default to Premier League
    
    try:
        if league_code not in LEAGUES:
            league_code = 'PL'
            
        data = fetch_football_data(f'competitions/{league_code}/standings')
        standings_data = []
        
        if 'standings' in data:
            for standing in data['standings']:
                if standing['type'] == 'TOTAL':
                    standing['competition'] = data['competition']
                    standings_data.append(standing)
        
        return render_template('standings.html', 
                            standings=standings_data,
                            leagues=LEAGUES,
                            selected_league=league_code)
    except Exception as e:
        print(f"Error fetching standings: {e}")
        return render_template('standings.html', 
                            standings=[],
                            leagues=LEAGUES,
                            selected_league=league_code)

@app.route('/news')
@login_required
def news():
    try:
        news_data = fetch_news()
        articles = news_data.get('articles', [])
        return render_template('news.html', 
                             articles=articles,
                             leagues=LEAGUES)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return render_template('news.html', 
                             articles=[],
                             leagues=LEAGUES)

if __name__ == '__main__':
    app.run(debug=True)