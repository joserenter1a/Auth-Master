import tkinter as tk

import requests 
import json 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import platform as sys_pf
from tkinter import filedialog
from emailrep import EmailRep


if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")


class App(tk.Tk):
    def __init__(self, title):
        super().__init__(title)
        # Inherit from tk.Tk
        self.title(title)
        self.geometry('1200x700')
        self.resizable(False, False)
        self.configure(background="#9177c7")
        
        # Create label to display word count
        self.word_count_label = tk.Label(self, text="Start typing or ")
        self.word_count_label.place(x = 100, y = 80, relheight = 0.04)
        self.word_count_label.configure(background="#9177c7")

        self.upload_button = tk.Button(self, text="Upload File", command=self.upload_file)
        self.upload_button.place(x = 190, y = 80, relheight = 0.04)
        # Create text entry widget
        self.text_entry = tk.Text(self)
        self.text_entry.place(x = 100, y = 110, relheight=.38, relwidth=.25)
        # Create count button
        self.scan_button = tk.Button(self, text="Scan for AI", command=self.ai_scan)
        self.scan_button.place(x = 100, y = 400, relheight = 0.04)

        self.scan__aiplag_button = tk.Button(self, text="AI URL Scan", command=self.ai_plag_scan)
        self.scan__aiplag_button.place(x = 185, y = 400, relheight = 0.04)
        
        self.scan__aiurl_button = tk.Button(self, text="Email Reputation Scan", command=self.scan_email)
        self.scan__aiurl_button.place(x = 275, y = 400, relheight = 0.04)


        # Run the Tkinter event loop
        self.mainloop()

    def upload_file(self):
        # Prompt user to select a file
        filename = filedialog.askopenfilename(initialdir="/", title="Select a Text File",
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                # Open the selected file for reading
                with open(filename, 'r') as file:
                    # Read the contents of the file
                    file_contents = file.read()

                    self.text_entry.insert(tk.END, file_contents)

            except FileNotFoundError:
                print("File not found.")

    def parse_dict_string(self, dict_string):
        try:
            # Attempt to parse the string as JSON
            parsed_dict = json.loads(dict_string)
            return parsed_dict
        except json.JSONDecodeError:
            # Handle error if the string is not valid JSON
            print("Error: Invalid JSON format")
            return None
        
    def ai_scan(self):

        url = "https://api.originality.ai/api/v1/scan/ai"

        payload = json.dumps({
        "content": self.text_entry.get("1.0", "end-1c"),
        "title": "optional title",
        "aiModelVersion": "1",
        "storeScan": "false"
        })
        headers = {
        'X-OAI-API-KEY': 'xodrg2zq5987kfcsjwimlhtn1by6u3vp',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        dict_string = response.text
        score = 0
        parsed_dict = self.parse_dict_string(dict_string)

        if parsed_dict:
            score = (parsed_dict["score"])
        original_pct = round(score["original"] * 100, 2)
        ai_pct = round(score["ai"] * 100, 2)
        pcts = [original_pct, ai_pct]
        # self.word_count_label.config(text=f'AI Generation Score: Original: {original_pct}% AI: {ai_pct} %')
        labels = [ "Original", "Ai"]
        colors = [ '#50ad50','#cc2530']
        fig, ax = plt.subplots()
        ax.pie(pcts, labels=labels, colors=colors, autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=600, y=100, relheight=0.25, relwidth=0.2)
        return canvas.draw()
    
    def ai_plag_scan(self):

        url = "https://api.originality.ai/api/v1/scan/ai-plag"

        payload = json.dumps({
        "content": self.text_entry.get("1.0", "end-1c"),
        "title": "optional title",
        "aiModelVersion": "1",
        "storeScan": "false"
        })
        headers = {
        'X-OAI-API-KEY': 'xodrg2zq5987kfcsjwimlhtn1by6u3vp',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        dict_string = response.text
        score = 0
        parsed_dict = self.parse_dict_string(dict_string)

        if parsed_dict:
            score = (parsed_dict["plagiarism"])
        total_pct = score["total_text_score"]
        print(response.text)
    def scan_email(self):
        email = self.text_entry.get("1.0", "end-1c")
        url = f"https://emailrep.io/{email}?summary=true"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        parsed_dict = self.parse_dict_string(response.text)
        print(response.text)
        print(parsed_dict["summary"])
        print(parsed_dict["reputation"])

    

def UI():
    app = App('Title')
    return app

if __name__ == '__main__':
    UI()