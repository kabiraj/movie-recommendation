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
    movie_name = ""
    recommendations = []

    #when user submits a movie title
    if request.method == 'POST':
        movie_name = request.form['movie']

        url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        response = requests.get(url)

        if response.status_code == 200:  # Check if the API request was successful
            data = response.json()  # Get the response data as a JSON object
            if data['results']:
                movie_id = data['results'][0]['id']  # Get the ID of the first result

                # Step 2: Get similar movies based on the movie ID (API call)
                recommendations_url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
                recommendations_response = requests.get(recommendations_url)
                
                if recommendations_response.status_code == 200:
                    recommendations_data = recommendations_response.json()
                    # Extract the movie titles from the response
                    recommendations = []
                    for movie in recommendations_data.get("results", []) [:2]:
                        title = movie["title"]
                        poster_path = movie.get("poster_path")
                        poster_url =  poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                        recommendations.append({"title":title, "poster_url":poster_url})

    # Step 3: Render the HTML template with the movie name and recommendations
    return render_template("recommendations.html", movie_name=movie_name, recommendations=recommendations)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)