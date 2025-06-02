# BotGuard - Twitter Bot Detection

BotGuard is a web application that uses machine learning to detect bot accounts on Twitter. It analyzes various features of Twitter accounts to determine the likelihood of them being automated or human-operated.

## Features

- Real-time Twitter account analysis
- Machine learning-based bot detection
- Detailed account metrics and statistics
- Modern, responsive UI
- RESTful API backend

## Tech Stack

- **Frontend**: React.js
- **Backend**: Django + Django REST Framework
- **Machine Learning**: XGBoost
- **API**: Twitter API v2

## Prerequisites

- Python 3.8+
- Node.js 14+
- Twitter API Bearer Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/botguard.git
cd botguard
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the root directory with your Twitter API credentials:
```
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## Running the Application

1. Start the Django backend:
```bash
python manage.py migrate
python manage.py runserver
```

2. In a new terminal, start the React frontend:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a Twitter username (without the @ symbol)
3. Click "Analyze" to check if the account is a bot
4. View the detailed analysis results

## Model Features

The bot detection model analyzes various account features including:
- Account age
- Follower/Following ratios
- Tweet frequency
- Description analysis
- Account verification status
- And more

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Twitter API for providing the data
- XGBoost for the machine learning framework
- Django and React communities for their excellent documentation
