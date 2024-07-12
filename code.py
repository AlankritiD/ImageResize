from PIL import Image
from cryptography.fernet import Fernet
from github import Github
import os

# Constants
IMAGE_PATH = 'sampleimg.jpg'
RESIZED_IMAGE_PATH = 'resized_image.jpg'
ENCRYPTION_KEY_FILE = 'encryption_key.key'
GITHUB_REPO_NAME = 'AlankritiD/ImageResize'
GITHUB_ACCESS_TOKEN = 'ACCESSTOKEN'

def resize_image(image_path, resized_image_path, size=(800, 800)):
    # Open an image file
    with Image.open(image_path) as img:
        # Resize image
        img = img.resize(size)
        # Save resized image
        img.save(resized_image_path)
        print(f"Image resized and saved to {resized_image_path}")

def generate_encryption_key(key_file_path):
    # Generate a key
    key = Fernet.generate_key()
    # Save the key to a file
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to {key_file_path}")
    return key

def upload_to_github(file_path, repo_name, access_token):
    # Authenticate to GitHub
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    
    with open(file_path, 'rb') as file:
        content = file.read()
    
    file_name = os.path.basename(file_path)
    
    try:
        repo.create_file(file_name, f"Add {file_name}", content)
        print(f"{file_name} uploaded to GitHub repository {repo_name}")
    except Exception as e:
        print(f"Failed to upload {file_name} to GitHub: {e}")

if __name__ == "__main__":
    # Resize the image
    resize_image(IMAGE_PATH, RESIZED_IMAGE_PATH)
    
    # Generate the encryption key
    encryption_key = generate_encryption_key(ENCRYPTION_KEY_FILE)
    
    # Upload the resized image and encryption key to GitHub
    upload_to_github(RESIZED_IMAGE_PATH, GITHUB_REPO_NAME, GITHUB_ACCESS_TOKEN)
    upload_to_github(ENCRYPTION_KEY_FILE, GITHUB_REPO_NAME, GITHUB_ACCESS_TOKEN)
