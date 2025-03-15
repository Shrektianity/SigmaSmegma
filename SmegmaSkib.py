import gdown
file_id = "1sLsSQbMHrXnlGdEoXSvpwzye0SStu8z8"
output_file = "sigmaskib.py"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
gdown.download(url, output_file, quiet=True)