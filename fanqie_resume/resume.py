from playwright.sync_api import sync_playwright
from PIL import Image
import img2pdf
import os


url = "https://www.fanqiecv.com/resume/edit/I3WiK6QFSBduPul7"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="fanqie_state.json",
        device_scale_factor=4,
        viewport={"width": 1800, "height": 1200}
    )

    page = context.new_page()
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)

    canvases = page.locator("#pdfContainer canvas")
    count = canvases.count()
    print("📄 发现 canvas 页数:", count)

    image_files = []

    for i in range(count):
        canvas = canvases.nth(i)
        canvas.wait_for(state="visible")

        path = f"resume_page_{i+1}.png"
        canvas.screenshot(path=path)

        print("✅ 保存:", path)
        image_files.append(path)

    browser.close()


# ========= 合成 PDF =========

images = []
for img_path in image_files:
    img = Image.open(img_path).convert("RGB")
    images.append(img)

pdf_path = "resume_ultra_multi.pdf"
images[0].save(pdf_path, save_all=True, append_images=images[1:])

print("🎉 完成导出:", pdf_path)
