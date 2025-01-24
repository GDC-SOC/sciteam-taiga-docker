import boto3
import os
import json
import sys

def format_env_content(secret_dict):
    """
    Converts a dictionary of secrets into .env-style content.
    
    :param secret_dict: Dictionary of key-value pairs from Secrets Manager
    :return: Formatted .env-style string
    """
    lines = []
    for key, value in secret_dict.items():
        if value == "":
            lines.append(f'{key}=""')
        elif isinstance(value, str) and " " in value:
            lines.append(f'{key}="{value}"')
        else:
            lines.append(f"{key}={value}")
    return "\n".join(lines)

def fetch_secret(secret_name, region_name, output_path):
    """
    Fetches a secret from AWS Secrets Manager and writes it as a formatted .env file.
    
    :param secret_name: Name of the secret in AWS Secrets Manager
    :param region_name: AWS region where the secret is stored
    :param output_path: Path to save the .env file
    """
    try:
        # Create a Secrets Manager client
        client = boto3.client("secretsmanager", region_name=region_name)
        
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret = response.get("SecretString", "{}")
        secret_dict = json.loads(secret)
        
        # Format the secret as .env content
        formatted_env = format_env_content(secret_dict)
        
        # Write the formatted content to the output file
        with open(output_path, "w") as f:
            f.write(formatted_env)
        
        print(f"Secret written to {output_path} successfully.")
    except Exception as e:
        print(f"Error retrieving or formatting secret: {e}")

if __name__ == "__main__":
    # Ensure environment variables are set
    SECRET_NAME = os.environ.get("SECRET_NAME")
    REGION_NAME = os.environ.get("REGION_NAME")
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH")
    
    # Check for missing environment variables
    if not SECRET_NAME:
        sys.exit("Error: SECRET_NAME environment variable is required.")
    if not REGION_NAME:
        sys.exit("Error: REGION_NAME environment variable is required.")
    if not OUTPUT_PATH:
        sys.exit("Error: OUTPUT_PATH environment variable is required.")
    
    # Fetch the secret
    fetch_secret(SECRET_NAME, REGION_NAME, OUTPUT_PATH)
