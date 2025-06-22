# scraper.py

from clotributor.browser import get_browser
from clotributor.issue_scraper import get_top_issues
from clotributor.gemini_summarizer import summarize_issue
import datetime

def main():
    print("[*] Launching browser…")
    driver = get_browser(headless=False)

    print("[*] Scraping top 5 issues from clotributor.dev…")
    issues = get_top_issues(driver, count=5)
    driver.quit()

    if not issues:
        print("[!] No issues found.")
        return

    # summarize with Gemini
    enriched = []
    for issue in issues:
        enriched.append(summarize_issue(issue))

    # prepare timestamped header
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n===== Clotributor Scrape @ {now} =====\n"

    # append to output.txt and print
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(header)
        print(header, end="")

        for idx, issue in enumerate(enriched, 1):
            block = (
                f"Issue #{idx}:\n"
                f"  Title:      {issue['title']}\n"
                f"  Link:       {issue['link']}\n"
                f"  Difficulty: {issue['difficulty']}\n\n"
                f"  Tags:       {issue['description']}\n\n"
                f"  Summary:    {issue['summary']}\n\n"
                f"  Approach:   {issue['suggested_solution']}\n"
                + "-"*60 + "\n"
            )
            f.write(block)
            print(block, end="")

    print("[*] Done! Results appended to output.txt")

if __name__ == "__main__":
    main()
