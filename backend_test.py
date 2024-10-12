import requests

url = "http://localhost:8080/ping"
filepath = "sample_pdf.pdf"

with open(filepath, 'rb') as file:
    response = requests.post(url, pdf_file=file)

# Check if the request was successful
if response.status_code == 200:
    print("Success:", response.text)
else:
    print("Failed with status code:", response.status_code)
