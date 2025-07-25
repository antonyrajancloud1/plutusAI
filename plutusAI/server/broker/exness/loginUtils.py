from playwright.sync_api import sync_playwright
import requests
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True to hide browser
    context = browser.new_context()
    page = context.new_page()

    # Go to the sign-in page (let Cloudflare JS challenge pass)
    page.goto("https://my.exness.com/v4/wta-api/signin?captchaVersion=3")

    # Wait for JS challenge to complete (auto-redirect)
    page.wait_for_timeout(5000)  # 5 seconds; adjust if needed

    # Now you can send POST request from within page context
    response = page.evaluate("""async () => {
        const res = await fetch("https://my.exness.com/v4/wta-api/signin?captchaVersion=3", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"login":"vijayamary.daniel10@gmail.com","password":"Antony@12","action":"LOGIN"})
        });
        return await res.json();
    }""")

    print(response)
    browser.close()
    access_token =response["token"]
    print(access_token)
    url = "https://rtapi-sg.eccweb.mobi/rtapi/mt5/trial17/v1/accounts/269445156/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"order":{"instrument":"XAUUSDm","price":3428.2,"type":0,"volume":0.02,"sl":0,"tp":0,"deviation":0,"oneClick":True}}
    response = requests.post(url, headers=headers, json=payload)

    # Print the response
    print(response.status_code)
    print(response.json())