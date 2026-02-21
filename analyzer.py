import json
from playwright.sync_api import sync_playwright

def analyze_website(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        # wait for visible content instead of network silence
        page.wait_for_timeout(5000)

        # Screenshot
        screenshot_path = "page.png"
        page.screenshot(path=screenshot_path, full_page=True)

        # ---- NEW ACCESSIBILITY EXTRACTION ----
        client = page.context.new_cdp_session(page)
        ax_tree = client.send("Accessibility.getFullAXTree")

        # simplify it for the LLM
        def simplify_ax(nodes):
            result = []
            for n in nodes[:120]:   # limit size (VERY IMPORTANT)
                role = n.get("role", {}).get("value")
                name = n.get("name", {}).get("value")

                if role and name:
                    result.append({
                        "role": role,
                        "name": name
                    })
            return result

        accessibility_tree = simplify_ax(ax_tree["nodes"])

        # Simplify it so LLM doesn't choke
        # ---- ACCESSIBILITY TREE VIA CDP ----
        client = page.context.new_cdp_session(page)
        ax_tree = client.send("Accessibility.getFullAXTree")

        def simplify_ax(nodes):
            important_roles = {
                "button", "link", "textbox", "searchbox",
                "heading", "checkbox", "radio", "combobox",
                "menuitem", "tab", "dialog"
            }

            results = []

            for node in nodes:
                role = node.get("role", {}).get("value")
                name = node.get("name", {}).get("value")

                if role in important_roles and name:
                    results.append({
                        "role": role,
                        "name": name
                    })

                # limit size so OpenAI doesn't reject
                if len(results) > 120:
                    break

            return results

        accessibility_tree = simplify_ax(ax_tree["nodes"])

        browser.close()

        return screenshot_path, json.dumps(accessibility_tree, indent=2)