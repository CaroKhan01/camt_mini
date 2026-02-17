import sys
import os
import re
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import spacy

# --- 1. Resource Helper (Crucial for .exe) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- 2. Load Spacy Model ---
# We try to load it safely. If running as exe, we expect it to be bundled.
try:
    # Note: We rely on the model being bundled correctly in the build step
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback/Debug for dev environment
    print("Spacy model not found. Attempting simple download...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- 3. Your Original Logic (Refactored for GUI) ---

def format_title(title):
    if not title: return title
    is_shouty = title.isupper()
    preserve_map = {} 
    doc_original = nlp(title)
    
    if not is_shouty:
        for t in doc_original:
            text = t.text
            if text != text.title() and text != text.lower():
                 preserve_map[t.idx] = (t.idx + len(text), text)
            elif text.isupper():
                 if len(text) > 1:
                     preserve_map[t.idx] = (t.idx + len(text), text)
                 elif len(text) == 1:
                     if text == "A" and t.pos_ == "DET": continue
                     preserve_map[t.idx] = (t.idx + len(text), text)

    title_lower = title.lower()
    doc_lower = nlp(title_lower)
    propn_ranges = []
    for t in doc_lower:
        if t.pos_ == "PROPN":
            propn_ranges.append((t.idx, t.idx + len(t.text)))

    title_chars = list(title_lower)
    if title_chars: title_chars[0] = title_chars[0].upper()

    def repl(m): return m.group(0).upper()
    temp_title = "".join(title_chars)
    temp_title = re.sub(r'([;?!:])(\s+)([a-z])', repl, temp_title)
    title_chars = list(temp_title)

    for start, end in propn_ranges:
        if end <= len(title_chars):
             segment = "".join(title_chars[start:end])
             title_chars[start:end] = list(segment.title())

    for start, (end, original_text) in preserve_map.items():
        if end <= len(title_chars):
            title_chars[start:end] = list(original_text)

    return "".join(title_chars)

def process_data(raw_text, research_field, averages_data, percentiles_data):
    # Split text into lines instead of reading file
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    # Preprocessing: Header removal
    for i, line in enumerate(lines):
        if line.lower() == "year":
            lines = lines[i+1:]
            break

    publications = []
    i = 0
    while i < len(lines):
        if i + 2 >= len(lines): break

        title = lines[i]
        formatted_title = format_title(title)
        line_3 = lines[i+2]
        
        has_letters = any(c.isalpha() for c in line_3)
        
        if not has_letters:
            venue = "Unknown Venue"
            citation_year_line = line_3
            i += 3
        else:
            venue = line_3
            if i + 3 < len(lines):
                citation_year_line = lines[i+3]
                i += 4
            else:
                break
        
        venue_chars = list(venue)
        while venue_chars and not venue_chars[-1].isalpha():
            venue_chars.pop()
        venue = "".join(venue_chars)

        parts = citation_year_line.split()
        if len(parts) >= 2:
            citations = parts[0]
            year = parts[-1]
        elif len(parts) == 1:
            citations = "0"
            year = parts[0]
        else:
            citations = "0"
            year = "Unknown"

        citations_clean = re.sub(r'\D', '', citations)
        try:
            citation_count = int(citations_clean)
        except ValueError:
            citation_count = 0
            citations_clean = "0"

        year = re.sub(r'\D', '', year)
        if not year: year = "Unknown"

        field_averages = averages_data.get(research_field, {})
        average_citations = field_averages.get(year, "N/A")

        percentiles_to_check = ["0.01%", "0.10%", "1.00%", "10.00%", "20.00%", "50.00%"]
        top_percentile = None
        field_percentiles = percentiles_data.get(research_field, {})
        
        for p in percentiles_to_check:
            if p in field_percentiles:
                p_data = field_percentiles[p]
                if year in p_data:
                    threshold = p_data[year]
                    try:
                        threshold_val = float(threshold)
                        if citation_count >= threshold_val:
                            top_percentile = p
                            break
                    except (ValueError, TypeError):
                        continue

        publications.append({
            'title': formatted_title, 'venue': venue, 'year': year,
            'citations': citations_clean, 'average': average_citations,
            'top_percentile': top_percentile
        })

    # Generate Output String (CAMT style only)
    output_lines = []
    research_field_title = research_field.title()

    for pub in publications:
        line = f"The article, \"{pub['title']},\" published in {pub['year']} in {pub['venue']}, has received {pub['citations']} citations to date. For all articles published in the category of {research_field_title} in {pub['year']}, the average number of citations is only {pub['average']}."
        
        if pub['top_percentile']:
            line += f" This article is thus one of the top {pub['top_percentile']} most cited articles published in {pub['year']} in {research_field_title}."
            
            # Filter for Top 20% or better
            if pub['top_percentile'] in ["0.01%", "0.10%", "1.00%", "10.00%", "20.00%"]:
                 output_lines.append(line)
    
    return "\n".join(output_lines)

# --- 4. The GUI Class ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scholar Data Processor (Emergency Backup)")
        self.geometry("800x600")

        # Load Data
        self.averages_data = {}
        self.percentiles_data = {}
        self.load_data()

        # Layout
        # Top Frame: Controls
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(top_frame, text="Select Research Field:").pack(side=tk.LEFT)
        
        # Dropdown
        self.fields = sorted(list(self.averages_data.keys()))
        self.combo = ttk.Combobox(top_frame, values=self.fields, width=40)
        if self.fields: self.combo.current(0)
        self.combo.pack(side=tk.LEFT, padx=10)

        # Run Button
        self.btn_run = tk.Button(top_frame, text="Generate CAMT Text", command=self.run_process, bg="#dddddd")
        self.btn_run.pack(side=tk.LEFT, padx=10)

        # Main Content
        content_frame = tk.Frame(self)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # Left: Input
        tk.Label(content_frame, text="1. Paste Google Scholar Data Here:").pack(anchor="w")
        self.txt_input = scrolledtext.ScrolledText(content_frame, height=10)
        self.txt_input.pack(expand=True, fill=tk.BOTH, pady=(0, 10))

        # Right: Output
        tk.Label(content_frame, text="2. Result (Copy from here):").pack(anchor="w")
        self.txt_output = scrolledtext.ScrolledText(content_frame, height=10, bg="#f0f0f0")
        self.txt_output.pack(expand=True, fill=tk.BOTH)

    def load_data(self):
        try:
            # Use resource_path to find JSONs inside the .exe
            p1 = resource_path('citation_averages.json')
            p2 = resource_path('citation_percentiles.json')
            
            with open(p1, 'r', encoding='utf-8') as f:
                self.averages_data = json.load(f)
            with open(p2, 'r', encoding='utf-8') as f:
                self.percentiles_data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load JSON data files:\n{e}")

    def run_process(self):
        raw_text = self.txt_input.get("1.0", tk.END).strip()
        field = self.combo.get()

        if not raw_text:
            messagebox.showwarning("Warning", "Please paste data into the input box.")
            return
        if not field:
            messagebox.showwarning("Warning", "Please select a research field.")
            return

        try:
            result = process_data(raw_text, field, self.averages_data, self.percentiles_data)
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing:\n{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()