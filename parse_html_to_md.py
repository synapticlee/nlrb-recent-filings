from bs4 import BeautifulSoup
import os

def extract_case_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    cases = []

    for rer in soup.select("div.rer-content"):
        company = rer.select_one("div.rer-head h3").text.strip()

        fields = {
            "Company": company,
            "Case Number": "",
            "Date Filed": "",
            "Status": "",
            "No Employees": "",
            "Location": "",
            "Region Assigned": ""
        }

        for item in rer.select("div.rer-style-1"):
            b = item.find("b")
            if not b:
                continue
            key = b.text.strip().rstrip(":")
            value = item.get_text().split(":")[-1].strip()

            if key == "Case Number":
                a = item.find("a")
                if a:
                    value = f"[{a.text.strip()}]({a['href']})"
            fields[key] = value

        cases.append(fields)

    return cases

def to_markdown_table(data):
    headers = ["Company", "Case Number", "Date Filed", "Status", "No Employees", "Location", "Region Assigned"]
    md = "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join("---" for _ in headers) + " |\n"

    for row in data:
        md += "| " + " | ".join(row.get(h, "") for h in headers) + " |\n"

    return md

def main():
    html_path = "nlrb.gov-reports-graphs-data-recent-filings-date_filed-desc-100%3Fpage%3D1.html"
    output_path = "new-filings.md"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    data = extract_case_data(html_content)
    md_table = to_markdown_table(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_table)

    print(f"✅ Markdown table written to {output_path}")

if __name__ == "__main__":
    main()
