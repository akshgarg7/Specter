import requests

url = "http://localhost:8080/upload"
filepath = "sample_pdf.pdf"

with open(f"pdf/{filepath}", 'rb') as file:
    files = {'pdf_file': (filepath, file, 'application/pdf')}  # 'pdf_file' must match the parameter in the FastAPI function
    response = requests.post(url, files=files)

# Check if the request was successful
if response.status_code == 200:
    print("Success:", response.text)
else:
    print("Failed with status code:", response.status_code)
