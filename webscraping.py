from bs4 import BeautifulSoup
import requests

def fetch_content(url):
    """Fetch the content of the URL with proper headers."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch URL. Status code: {response.status_code}")

def parse_content(html_content):
    """Parse the HTML content and extract relevant text."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n').strip()
    return text

def extract_coordinates(text):
    """Extract coordinates and characters from the text."""
    lines = text.splitlines()
    start_parsing = False
    filtered_lines = []

    for line in lines:
        if start_parsing:
            filtered_lines.append(line)
        if line.strip() == "y-coordinate":
            start_parsing = True

    # Group lines into chunks of 3 (x, char, y)
    grouped_data = [filtered_lines[i:i+3] for i in range(0, len(filtered_lines), 3)]
    return [group for group in grouped_data if len(group) == 3]

def build_array(coordinates):
    """Build a 2D array based on the extracted coordinates."""
    print(coordinates)
    max_x = max(int(coord[0]) for coord in coordinates) + 1
    max_y = max(int(coord[2]) for coord in coordinates) + 1
    array = [[" " for _ in range(max_x)] for _ in range(max_y)]

    for x, char, y in coordinates:
        array[int(y)][int(x)] = char

    return array

def display_array(array):
    """Display the 2D array."""
    for row in array:
        print("".join(row))

def main(url=None):
    """Main function to orchestrate the web scraping process."""
    if not url:
        url = input("Enter the URL: ")

    try:
        html_content = fetch_content(url)
        text_content = parse_content(html_content)
        coordinates = extract_coordinates(text_content)
        array = build_array(coordinates)
        display_array(array)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = 'https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub'
    main(url)