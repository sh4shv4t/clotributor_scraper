# clotributor/issue_scraper.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_top_issues(driver, count=5):
    """
    Scrapes top N new issues from clotributor.dev.
    Returns only real GitHub issue links, plus title, metadata, and difficulty.
    """
    driver.get("https://clotributor.dev")

    # wait for cards to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[class*='Card_projectWrapper'], div[role='listitem']")
        )
    )
    cards = driver.find_elements(
        By.CSS_SELECTOR,
        "div[class*='Card_projectWrapper'], div[role='listitem']"
    )

    seen = set()
    issues = []

    for card in cards:
        if len(issues) >= count:
            break

        # must be a GitHub issue link
        try:
            link_el = card.find_element(By.CSS_SELECTOR, "a[href*='/issues/']")
            link = link_el.get_attribute("href")
        except:
            continue
        if link in seen:
            continue
        seen.add(link)

        # 1) **Issue Title** — use the Card_issueDesc element
        try:
            title_el = card.find_element(
                By.CSS_SELECTOR,
                "div[class*='Card_issueDesc'], div[class*='Card_issueDesc_']"
            )
            title = title_el.text.strip()
        except:
            # fallback: use the anchor text (repo name)
            try:
                title = link_el.text.strip()
            except:
                title = "Untitled Issue"

        # 2) **Metadata / Tags** — whatever lives in the issueContent block
        try:
            meta_el = card.find_element(
                By.CSS_SELECTOR,
                "div[class*='Card_issueContent'], p, div[class*='meta']"
            )
            metadata = meta_el.text.strip()
        except:
            metadata = ""

        # 3) **Difficulty** based on labels
        labels = metadata.upper()
        if "GOOD FIRST ISSUE" in labels:
            diff = "Beginner"
        elif any(x in labels for x in ("HARD", "DIFFICULT")):
            diff = "Advanced"
        else:
            diff = "Intermediate"

        issues.append({
            "title": title,
            "link": link,
            "metadata": metadata,
            "difficulty": diff
        })

    return issues
