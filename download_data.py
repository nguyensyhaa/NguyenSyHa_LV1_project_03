import requests
import os

url = "https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv"
output_path = "tmdb-movies.csv"

def download_file(url, output_path):
    print(f"Downloading {url} to {output_path}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    if not os.path.exists(output_path):
        download_file(url, output_path)
    else:
        print(f"{output_path} already exists. Skipping download.")
