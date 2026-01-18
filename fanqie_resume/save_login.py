from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.fanqiecv.com")

    print("👉 请在打开的浏览器中手动登录，完成后等待...")
    page.wait_for_timeout(60000)

    context.storage_state(path="fanqie_state.json")
    print("✅ 登录态已保存 fanqie_state.json")

    browser.close()