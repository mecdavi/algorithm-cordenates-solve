from bs4 import BeautifulSoup;import requests
def main(url=None):
    if not url:
        url = input("url: ")
    response = requests.get(url)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text(separator='\n').strip()
    start = False
    extracted_data = []
    for line in content.splitlines():
        if line.strip() == "y-coordinate":
            start = True
            continue
        if start:
            extracted_data.append(line)
    grouped_data = [extracted_data[i:i + 3] for i in range(0, len(extracted_data), 3)]
    max_x = max_y = 0
    for item in grouped_data:
        if len(item) == 3:
            try:
                x, char, y = int(item[0]), item[1], int(item[2])
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            except ValueError:
                continue
    canvas = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for item in grouped_data:
        if len(item) == 3:
            try:
                x, char, y = int(item[0]), item[1], int(item[2])
                canvas[y][x] = char
            except ValueError:
                continue
    for row in canvas:
        print("".join(row))

url = 'https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub'
main(url)
