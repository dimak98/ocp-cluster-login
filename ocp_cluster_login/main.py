# ocp_cluster_login/main.py

import argparse
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse, urlunparse

# Output colors
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

# Hosts
DEFAULT_API_SERVER = 'https://api.ocp.domain.com:6443'

# Supported web drivers
SUPPORTED_DRIVERS = ["chrome", "firefox"]

# Function to check if user is already logged in to the OPC server
def is_user_logged_in(api_server, tls_verify):
    try:
        whoami_command = ["oc", "whoami", "--server", api_server] + tls_verify
        result = subprocess.run(whoami_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"{COLOR_RED}Error checking login status: {str(e)}{COLOR_RESET}")
        return False

# Function to get auth server from SERVER_MAPPING
def get_oauth_server(api_server):
    return SERVER_MAPPING.get(api_server, SERVER_MAPPING.get(DEFAULT_API_SERVER))

# Function to construct login url and token display pattern
def construct_urls(api_server, oauth_server):
    login_url = f'{oauth_server}/oauth/authorize?client_id=openshift-browser-client&redirect_uri={oauth_server}%2Foauth%2Ftoken%2Fdisplay&response_type=code'
    token_display_pattern = rf'{re.escape(oauth_server)}/oauth/token/display\?code=sha256~[A-Za-z0-9_-]+&state='
    return login_url, token_display_pattern

# Function to construct the OAuth server URL from the API server URL
def construct_oauth_server_url(api_server):
    parsed_url = urlparse(api_server)
    subdomain = 'oauth-openshift.apps'
    netloc = parsed_url.netloc.replace('api', subdomain, 1).split(':')[0]
    return urlunparse(parsed_url._replace(netloc=netloc))

# Initialize the selected web driver
def initialize_driver(driver_name):
    try:
        if driver_name == "chrome":
            return webdriver.Chrome()
        elif driver_name == "firefox":
            return webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported driver: {driver_name}")
    except WebDriverException as e:
        print(f"{COLOR_RED}Error initializing the {driver_name} web driver: {e}{COLOR_RESET}")
        exit(1)
    except Exception as e:
        print(f"{COLOR_RED}An unexpected error occurred while initializing the {driver_name} driver: {e}{COLOR_RESET}")
        exit(1)

# Main function to handle login logic
def main():
    parser = argparse.ArgumentParser(description='Login to OpenShift.')
    parser.add_argument('-s', '--server', default=DEFAULT_API_SERVER, help='API server URL')
    parser.add_argument('-k', '--insecure-skip-tls-verify', dest='insecure', action='store_true', help='Skip TLS verification')
    parser.add_argument('-t', '--timeout', type=int, default=60, help='Timeout for waiting for login')
    parser.add_argument('-d', '--driver', default='chrome', choices=SUPPORTED_DRIVERS, help='Select the web driver')
    args = parser.parse_args()

    api_server = args.server
    insecure = args.insecure
    timeout = args.timeout
    driver_name = args.driver

    print(f"API Server: {api_server}, Insecure: {insecure}, Timeout: {timeout}, Driver: {driver_name}")  # Debug print

    oauth_server = construct_oauth_server_url(api_server)
    if not oauth_server:
        print(f"{COLOR_RED}Couldn't construct OAUTH Server URL.{COLOR_RESET}")
        return

    tls_verify = ["--insecure-skip-tls-verify"] if insecure else []

    if is_user_logged_in(api_server, tls_verify):
        print(f"{COLOR_GREEN}User is already logged in to {api_server}.{COLOR_RESET}")
        return

    login_url, token_display_pattern = construct_urls(api_server, oauth_server)
    driver = initialize_driver(driver_name)

    try:
        driver.get(login_url)
        print(f"{COLOR_YELLOW}Please log in through the opened browser window...{COLOR_RESET}")

        WebDriverWait(driver, timeout).until(
            lambda d: re.match(token_display_pattern, d.current_url)
        )

        display_token_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        display_token_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'code'))
        )
        token_element = driver.find_element(By.TAG_NAME, 'code')
        token = token_element.text if token_element else None

        if token:
            driver.quit()
            login_command = ["oc", "login", "--token", token, "--server", api_server] + tls_verify

            result = subprocess.run(login_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"{COLOR_GREEN}Logged in successfully.{COLOR_RESET}")
                print(result.stdout)
            else:
                print(f"{COLOR_RED}Login failed: {result.stderr}{COLOR_RESET}")
                print(f"{COLOR_RED}An error occurred: Login failed.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}Failed to retrieve the token.{COLOR_RESET}")
            print(f"{COLOR_RED}An error occurred: Failed to retrieve the token.{COLOR_RESET}")

    except KeyboardInterrupt:
        print(f"{COLOR_YELLOW}\nOperation cancelled by user.{COLOR_RESET}")
        exit(1)
    except Exception as e:
        error_message = str(e)
        print(f"{COLOR_RED}An error occurred: {error_message}{COLOR_RESET}")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()