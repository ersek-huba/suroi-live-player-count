import tkinter as tk
import requests
import json
import threading

REGION_NAMES = {"na": "North America", "eu": "Europe", "sa": "South America", "as": "Asia"}
MAX_WIDTH = max(len(s) for s in REGION_NAMES.values())

root = tk.Tk()
root.geometry("200x100")
root.resizable(width=False, height=False)

def get_player_count(region):
    try:
        response = requests.get(f"https://{region}.suroi.io/api/serverInfo")
    except Exception as e:
        return "-"
    if response.ok:
        return str(json.loads(response.text)["playerCount"])
    return "-"

def callback(region):
    region_labels[region].config(text=get_player_count(region))
    root.after(1000, lambda: callback(region))

region_labels = {}
threads = []

for idx, (region, name) in enumerate(REGION_NAMES.items()):
    name_label = tk.Label(text=name, width=MAX_WIDTH)
    name_label.grid(row=idx, column=0, sticky=tk.W)
    plr_cnt_label = tk.Label(text="-")
    plr_cnt_label.grid(row=idx, column=1, sticky=tk.E, padx=50)
    region_labels[region] = plr_cnt_label

for region in REGION_NAMES:
    threads.append(threading.Thread(target=callback, args=(region,), daemon=True))

for thread in threads:
    thread.run()

root.mainloop()
