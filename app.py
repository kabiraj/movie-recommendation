from flask import Flask, render_template, request
import requests

# Create a Flask app instance
app = Flask(__name__)

# Correct TMDb API key variable name
TMDB_API_KEY = "3a49045f17420275dfc335d386b01962"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for search and recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the movie query from the form
    movie_query = request.form.get('movie')

    # API call to TMDb to search for movies
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_query,
        "language": "en-US"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse the API response
        data = response.json()
        # Get the top 10 movie titles
        recommendations = [movie["title"] for movie in data.get("results", [])[:20]]
        return render_template('recommendations.html', movie_name=movie_query, recommendations=recommendations)
    else:
        return f"Error: Unable to fetch data from TMDb. Status code: {response.status_code}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
