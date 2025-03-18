# Astro - Your Space Companion 🔭

A beautiful and intelligent astronomy chatbot that answers questions about space, planets, stars, and the universe.

## Features

- Interactive chat interface with a cute anime-style robot mascot
- Comprehensive knowledge base covering various astronomy topics
- Beautiful space-themed UI with animated stars
- Mobile-responsive design
- Powered by advanced natural language processing

## Topics Covered

- Solar System and Planets
- Stars and Galaxies
- Space Phenomena
- Space Exploration
- Astronomical Discoveries
- Basic Astronomy Concepts

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd astronomy_chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8080`

## Deployment

This application can be deployed to various platforms:

### Heroku
1. Create a Heroku account and install Heroku CLI
2. Login to Heroku:
```bash
heroku login
```
3. Create a new Heroku app:
```bash
heroku create your-app-name
```
4. Push to Heroku:
```bash
git push heroku main
```

### Railway/Render
1. Connect your GitHub repository
2. Use the following build command:
```bash
pip install -r requirements.txt
```
3. Use the following start command:
```bash
gunicorn app:app
```

## Environment Variables
No environment variables are required for basic functionality.

## Contributing
Feel free to open issues and pull requests to improve the chatbot's knowledge base or features.

## License
MIT License
