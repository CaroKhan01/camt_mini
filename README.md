# CAMT Text Generator: User Guide
## What This Program Does
Instead of manually typing out citation statistics and comparing them against ESI baselines, this tool takes raw copied text and transforms it into paragraphs.

### Key Features
* **Automatic Title Formatting:** It reads raw article titles and automatically applies proper title-casing using natural language processing, preserving acronyms and proper nouns.
* **Instant Data Comparison:** It compares an article's citation count against the average citations and top percentiles (ranging from the top 20% to the top 0.01%) for its specific research field and publication year.
* **Ready-to-Paste Text:** The program generates the final summary text with all necessary formatting (like **bolding** for citation counts and *italics* for venue names) built-in.
* **Percentile Summary:** A quick-reference table tracks exactly how many of the pasted articles fall into the top citation tiers.

## How to Use It

1. **Select the Field:** Choose the relevant research field from the dropdown menu at the top of the window.
2. **Add a Client Name:** If you enter a client's name, the program will personalize the output sentences.
3. **Paste Your Data:** Copy your raw publication data and paste it into the top text box labeled "1. Paste Google Scholar Data Here".
4. **Generate the Text:** Click the **Generate CAMT Text** button.
5. **Copy the Result:** Click the **Copy Formatted Output** button. This copies the generated paragraphs directly to your clipboard.

### Example Output
Depending on the article's performance, the tool generates standardized sentences that look like this:

> [Client Name]'s article, "Properly Capitalized Article Title," published in [Year] in *[Venue Name]*, has received **[X] citations** to date. For all articles published in the category of [Research Field] in [Year], the average number of citations is only [Y]. This article is thus one of the **<u>top [Z]%</u> most cited articles published in [Year]** in [Research Field].