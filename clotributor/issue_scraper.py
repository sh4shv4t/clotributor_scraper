# clotributor/issue_scraper.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_top_issues(driver, count=5):
    """
    Scrapes top N new issues from clotributor.dev.
    Returns only real GitHub issue links, plus title, tags, and difficulty.
    """
    driver.get("https://clotributor.dev")

    # wait for cards
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

        # try precise selectors first
        try:
            link_el = card.find_element(By.CSS_SELECTOR, "a[href*='/issues/']")
            link = link_el.get_attribute("href")
        except:
            # skip any card without an /issues/ link
            continue

        if link in seen:
            continue
        seen.add(link)

        # title
        try:
            title_el = card.find_element(
                By.CSS_SELECTOR,
                "div[class*='truncateWrapper'], h3, span[class*='Card_name']"
            )
            title = title_el.text.strip()
        except:
            title = link.split("/")[-1]  # fallback: use the issue number

        # tags/metadata
        try:
            desc_el = card.find_element(
                By.CSS_SELECTOR,
                "div[class*='Card_issueContent'], p, div[class*='meta']"
            )
            description = desc_el.text.strip()
        except:
            description = ""

        # difficulty
        labels = description.upper()
        if "GOOD FIRST ISSUE" in labels:
            diff = "Beginner"
        elif any(x in labels for x in ("HARD", "DIFFICULT")):
            diff = "Advanced"
        else:
            diff = "Intermediate"

        issues.append({
            "title": title,
            "link": link,
            "description": description,
            "difficulty": diff
        })

    return issues
