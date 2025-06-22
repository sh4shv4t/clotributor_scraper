# scraper.py

from clotributor.browser import get_browser
from clotributor.issue_scraper import get_top_issues
from clotributor.gemini_summarizer import summarize_issue
import datetime
import re

def compact_metadata(md: str) -> str:
    """Turn a multi-line metadata block into a comma-separated single line."""
    lines = [line.strip() for line in md.splitlines() if line.strip()]
    return ", ".join(lines)

def compact_text(txt: str) -> str:
    """Collapse multiple blank lines into one, trim spaces."""
    # replace sequences of 2+ newlines with exactly two (one blank line)
    return re.sub(r'\n{2,}', '\n\n', txt.strip())

def main():
    print("[*] Launching browser…")
    driver = get_browser(headless=False)

    print("[*] Scraping top 5 issues from clotributor.dev…")
    issues = get_top_issues(driver, count=5)
    driver.quit()

    if not issues:
        print("[!] No issues found.")
        return

    # Summarize
    enriched = [summarize_issue(issue) for issue in issues]

    # Timestamp header
    now    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n===== Clotributor Scrape @ {now} =====\n"

    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(header)
        print(header, end="")

        for idx, issue in enumerate(enriched, 1):
            tags = compact_metadata(issue.get('metadata', ''))
            summary = compact_text(issue.get('summary', ''))
            approach = compact_text(issue.get('suggested_solution', ''))

            block = (
                f"Issue #{idx}:\n"
                f"  Title:      {issue['title']}\n"
                f"  Link:       {issue['link']}\n"
                f"  Difficulty: {issue['difficulty']}\n"
                f"  Tags:       {tags}\n\n"
                f"  Summary:    {summary}\n\n"
                f"  Approach:   {approach}\n"
                + "-"*60 + "\n"
            )
            f.write(block)
            print(block, end="")

    print("[*] Done! Results appended to output.txt")

if __name__ == "__main__":
    main()
