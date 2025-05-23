import requests
import shlex
import argparse

def parse_curl(curl_command):
    # Remove backslashes and combine lines into a single command
    curl_command = curl_command.replace("\\\n", " ").strip()
    parts = shlex.split(curl_command)

    url = None
    method = None
    headers = {}
    data = {}

    i = 0
    while i < len(parts):
        if parts[i] in ['-X', '--request']:
            method = parts[i+1].upper()
            i += 2
        elif parts[i] in ['-H', '--header']:
            header = parts[i+1].split(':', 1)  # Split only on first colon
            headers[header[0].strip()] = header[1].strip()
            i += 2
        elif parts[i] in ['-d', '--data', '--data-urlencode']:
            key_value = parts[i+1].split('=', 1)
            if len(key_value) == 2:
                data[key_value[0]] = key_value[1]
            i += 2
        elif parts[i].startswith("http"):
            url = parts[i]
            i += 1
        else:
            i += 1

    if method is None:
        method = "GET" if not data else "POST"  # Infer method if not explicitly defined

    return {
        "url": url,
        "method": method,
        "headers": headers,
        "data": data
    }

def call_api(url, method, headers, data):
    if method == "POST":
        response = requests.post(url, headers=headers, data=data)
    elif method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, data=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    print("\nRaw API Response:")
    print(response.text)  # Print raw response

    try:
        return response.json()  # Attempt to parse JSON
    except requests.exceptions.JSONDecodeError:
        return {"error": "Response is not JSON", "content": response.text}


def main():
    parser = argparse.ArgumentParser(description="Parse cURL and send HTTP request")
    parser.add_argument("curl_file", type=str, help="Path to the .sh file containing cURL commands")
    args = parser.parse_args()

    with open(args.curl_file, 'r') as file:
        curl_commands = file.read().splitlines()

    # Combine lines with backslashes into a single command
    combined_commands = []
    current_command = ""
    for line in curl_commands:
        if line.strip().endswith("\\"):
            current_command += line.strip()[:-1] + " "  # Remove backslash and add space
        else:
            current_command += line.strip()
            combined_commands.append(current_command)
            current_command = ""

    for curl_command in combined_commands:
        if curl_command.startswith('curl'):
            print(f"\nProcessing cURL command: {curl_command}")
            parsed = parse_curl(curl_command)

            print("\nParsed Information:")
            print(f"URL: {parsed['url']}")
            print(f"Method: {parsed['method']}")
            print(f"Headers: {parsed['headers']}")
            print(f"Form Data: {parsed['data']}")

            print("\nCalling API...")
            try:
                response = call_api(parsed["url"], parsed["method"], parsed["headers"], parsed["data"])
                print("\nAPI Response:")
                print(response)
            except Exception as e:
                print(f"Error calling API: {e}")

if __name__ == "__main__":
    main()
