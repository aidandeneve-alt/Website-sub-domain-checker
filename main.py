#!/usr/bin/env python3

"""

Admin Path Scanner - A desktop application for discovering admin panels and sensitive paths

Author: Nexus_tech

Platform: Linux and Windows

"""


import tkinter as tk

from tkinter import ttk, filedialog, messagebox, scrolledtext

import requests

import threading

import csv

import datetime

import random

import time

import os

from urllib.parse import urljoin, urlparse



class AdminPathScanner:

def __init__(self, root):

self.root = root

self.root.title("Admin Path Scanner")

self.root.geometry("1000x700")

self.root.resizable(True, True)

# Scanner state

self.is_scanning = False

self.scan_thread = None

self.results = []

self.current_wordlist = []

# Default wordlist of common admin/sensitive paths

self.default_wordlist = [

"/admin", "/administrator", "/login", "/dashboard", "/wp-admin", 

"/cpanel", "/manager", "/control", "/panel", "/backend", "/staff", 

"/moderator", "/config", "/setup", "/phpmyadmin", "/portal", "/manage", 

"/api", "/api/v1", "/api/v2", "/console", "/secret", "/hidden", 

"/internal", "/dev", "/test", "/staging", "/backup", "/old", "/new", "/beta",

"/admin.php", "/admin.html", "/admin.asp", "/admin.jsp", "/admin.cgi",

"/login.php", "/login.html", "/login.asp", "/login.jsp", "/login.cgi",

"/wp-login.php", "/administrator/index.php", "/admin/index.php",

"/admin/panel", "/admin/dashboard", "/admin/login", "/admin/cp",

"/controlpanel", "/admin_area", "/admin_area/", "/adminarea/",

"/admin_login", "/adminlogin/", "/admin-home/", "/admin_panel/",

"/adminarea.html", "/adminarea.php", "/adminarea.asp", "/adminarea.jsp",

"/adminpage.html", "/adminpage.php", "/adminpage.asp", "/adminpage.jsp",

"/admin-login.html", "/admin-login.php", "/admin-login.asp", "/admin-login.jsp",

"/adminpanel.html", "/adminpanel.php", "/adminpanel.asp", "/adminpanel.jsp",

"/admin1.html", "/admin1.php", "/admin1.asp", "/admin1.jsp",

"/admin2.html", "/admin2.php", "/admin2.asp", "/admin2.jsp",

"/admin3.html", "/admin3.php", "/admin3.asp", "/admin3.jsp",

"/admin4.html", "/admin4.php", "/admin4.asp", "/admin4.jsp",

"/admin5.html", "/admin5.php", "/admin5.asp", "/admin5.jsp",

"/administrator.html", "/administrator.php", "/administrator.asp", "/administrator.jsp",

"/moderator.html", "/moderator.php", "/moderator.asp", "/moderator.jsp",

"/webadmin.html", "/webadmin.php", "/webadmin.asp", "/webadmin.jsp",

"/adminarea.html", "/adminarea.php", "/adminarea.asp", "/adminarea.jsp",

"/bb-admin.html", "/bb-admin.php", "/bb-admin.asp", "/bb-admin.jsp",

"/adminLogin.html", "/adminLogin.php", "/adminLogin.asp", "/adminLogin.jsp",

"/panel.html", "/panel.php", "/panel.asp", "/panel.jsp",

"/cpanel.html", "/cpanel.php", "/cpanel.asp", "/cpanel.jsp",

"/admin1/", "/admin2/", "/admin3/", "/admin4/", "/admin5/",

"/administr8/", "/administrative/", "/administrator/", "/administrador/",

"/administratie/", "/admins/", "/administer/", "/adminpanel/",

"/user/", "/users/", "/accounts/", "/account/", "/member/", "/members/",

"/login.html", "/login.php", "/login.asp", "/login.jsp",

"/signin.html", "/signin.php", "/signin.asp", "/signin.jsp",

"/signup.html", "/signup.php", "/signup.asp", "/signup.jsp",

"/register.html", "/register.php", "/register.asp", "/register.jsp",

"/utilities.html", "/utilities.php", "/utilities.asp", "/utilities.jsp",

"/webmaster.html", "/webmaster.php", "/webmaster.asp", "/webmaster.jsp",

"/database/", "/database administration/", "/database admin/",

"/sysadmin.html", "/sysadmin.php", "/sysadmin.asp", "/sysadmin.jsp",

"/ur-admin.html", "/ur-admin.php", "/ur-admin.asp", "/ur-admin.jsp",

"/Server.html", "/Server.php", "/Server.asp", "/Server.jsp",

"/Server_admin.html", "/Server_admin.php", "/Server_admin.asp", "/Server_admin.jsp",

"/wp-admin/", "/wp-login.php", "/typo3/", "/typo3/",

"/admin.html", "/admin.php", "/admin.asp", "/admin.jsp",

"/admin.cfm", "/admin.pl", "/admin/", "/administrator/",

"/moderator.html", "/moderator.php", "/moderator.asp", "/moderator.jsp",

"/moderator/", "/moderator/", "/fileadmin/", "/fileadmin/",

"/administrator.html", "/administrator.php", "/administrator.asp", "/administrator.jsp",

"/administrator/", "/superuser/", "/superuser.html", "/superuser.php",

"/superuser.asp", "/superuser.jsp", "/superuser/", "/access/",

"/sysadmin/", "/sysadmin.html", "/sysadmin.php", "/sysadmin.asp",

"/sysadmin.jsp", "/admin1.html", "/admin1.php", "/admin1.asp",

"/admin1.jsp", "/admin2.html", "/admin2.php", "/admin2.asp",

"/admin2.jsp", "/admin3.html", "/admin3.php", "/admin3.asp",

"/admin3.jsp", "/admin4.html", "/admin4.php", "/admin4.asp",

"/admin4.jsp", "/admin5.html", "/admin5.php", "/admin5.asp",

"/admin5.jsp", "/administrators/", "/administrators.html", "/administrators.php",

"/administrators.asp", "/administrators.jsp", "/manager/", "/manager.html",

"/manager.php", "/manager.asp", "/manager.jsp", "/configuration/",

"/configuration.html", "/configuration.php", "/configuration.asp", "/configuration.jsp",

"/configure/", "/configure.html", "/configure.php", "/configure.asp",

"/configure.jsp", "/websvn/", "/administrator/", "/administrator.html",

"/administrator.php", "/administrator.asp", "/administrator.jsp",

"/administer/", "/administer.html", "/administer.php", "/administer.asp",

"/administer.jsp", "/useradmin/", "/useradmin.html", "/useradmin.php",

"/useradmin.asp", "/useradmin.jsp", "/sysadmins/", "/sysadmins.html",

"/sysadmins.php", "/sysadmins.asp", "/sysadmins.jsp", "/admin1/",

"/admin2/", "/admin3/", "/admin4/", "/admin5/", "/moderator/",

"/moderator.html", "/moderator.php", "/moderator.asp", "/moderator.jsp",

"/moderator/", "/webadmin/", "/webadmin.html", "/webadmin.php",

"/webadmin.asp", "/webadmin.jsp", "/administratie/", "/administrators/",

"/administrators.html", "/administrators.php", "/administrators.asp", "/administrators.jsp",

"/adminarea/", "/adminarea.html", "/adminarea.php", "/adminarea.asp",

"/adminarea.jsp", "/bb-admin/", "/bb-admin.html", "/bb-admin.php",

"/bb-admin.asp", "/bb-admin.jsp", "/adminLogin/", "/adminLogin.html",

"/adminLogin.php", "/adminLogin.asp", "/adminLogin.jsp", "/panel-admin/",

"/panel-admin.html", "/panel-admin.php", "/panel-admin.asp", "/panel-admin.jsp",

"/panel.html", "/panel.php", "/panel.asp", "/panel.jsp",

"/cpanel/", "/cpanel.html", "/cpanel.php", "/cpanel.asp",

"/cpanel.jsp", "/cpanel_file/", "/admin_login.html", "/admin_login.php",

"/admin_login.asp", "/admin_login.jsp", "/panel_login/", "/panel_login.html",

"/panel_login.php", "/panel_login.asp", "/panel_login.jsp", "/wp-admin/",

"/wp-login.php", "/adminarea.html", "/adminarea.php", "/adminarea.asp",

"/adminarea.jsp", "/database.html", "/database.php", "/database.asp",

"/database.jsp", "/database/", "/database administration/", "/database admin/",

"/database_administration/", "/database_admin/", "/dbadmin/", "/dbadmin.html",

"/dbadmin.php", "/dbadmin.asp", "/dbadmin.jsp", "/webmaster.html",

"/webmaster.php", "/webmaster.asp", "/webmaster.jsp", "/webmaster/",

"/ur-admin.html", "/ur-admin.php", "/ur-admin.asp", "/ur-admin.jsp",

"/ur-admin/", "/Server.html", "/Server.php", "/Server.asp",

"/Server.jsp", "/Server/", "/Server_admin.html", "/Server_admin.php",

"/Server_admin.asp", "/Server_admin.jsp", "/Server_admin/", "/wp/",

"/wordpress/", "/wp/wp-admin/", "/wp-admin/", "/typo3/",

"/typo3/", "/admin.html", "/admin.php", "/admin.asp", "/admin.jsp",

"/admin.cfm", "/admin.pl", "/admin/", "/administrator.html",

"/administrator.php", "/administrator.asp", "/administrator.jsp",

"/administrator/", "/moderator.html", "/moderator.php", "/moderator.asp",

"/moderator.jsp", "/moderator/", "/fileadmin/", "/fileadmin.html",

"/fileadmin.php", "/fileadmin.asp", "/fileadmin.jsp", "/administrator.html",

"/administrator.php", "/administrator.asp", "/administrator.jsp", "/administrator/",

"/superuser.html", "/superuser.php", "/superuser.asp", "/superuser.jsp",

"/superuser/", "/access.html", "/access.php", "/access.asp",

"/access.jsp", "/access/", "/sysadmin.html", "/sysadmin.php",

"/sysadmin.asp", "/sysadmin.jsp", "/sysadmin/", "/admin1.html",

"/admin1.php", "/admin1.asp", "/admin1.jsp", "/admin2.html",

"/admin2.php", "/admin2.asp", "/admin2.jsp", "/admin3.html",

"/admin3.php", "/admin3.asp", "/admin3.jsp", "/admin4.html",

"/admin4.php", "/admin4.asp", "/admin4.jsp", "/admin5.html",

"/admin5.php", "/admin5.asp", "/admin5.jsp", "/administrators.html",

"/administrators.php", "/administrators.asp", "/administrators.jsp", "/administrators/",

"/manager.html", "/manager.php", "/manager.asp", "/manager.jsp",

"/manager/", "/configuration.html", "/configuration.php", "/configuration.asp",

"/configuration.jsp", "/configuration/", "/configure.html", "/configure.php",

"/configure.asp", "/configure.jsp", "/configure/", "/websvn/",

"/admin/", "/admin.php", "/admin.html", "/admin.cfm",

"/admin.asp", "/admin.jsp", "/administrator/", "/administrator.php",

"/administrator.html", "/administrator.cfm", "/administrator.asp", "/administrator.jsp",

"/moderator/", "/moderator.php", "/moderator.html", "/moderator.cfm",

"/moderator.asp", "/moderator.jsp", "/webadmin/", "/webadmin.php",

"/webadmin.html", "/webadmin.cfm", "/webadmin.asp", "/webadmin.jsp",

"/adminarea/", "/adminarea.php", "/adminarea.html", "/adminarea.cfm",

"/adminarea.asp", "/adminarea.jsp", "/bb-admin/", "/bb-admin.php",

"/bb-admin.html", "/bb-admin.cfm", "/bb-admin.asp", "/bb-admin.jsp",

"/adminLogin/", "/adminLogin.php", "/adminLogin.html", "/adminLogin.cfm",

"/adminLogin.asp", "/adminLogin.jsp", "/panel-admin/", "/panel-admin.php",

"/panel-admin.html", "/panel-admin.cfm", "/panel-admin.asp", "/panel-admin.jsp",

"/panel/", "/panel.php", "/panel.html", "/panel.cfm",

"/panel.asp", "/panel.jsp", "/user/", "/user.php", "/user.html",

"/user.cfm", "/user.asp", "/user.jsp", "/users/", "/users.php",

"/users.html", "/users.cfm", "/users.asp", "/users.jsp",

"/account/", "/account.php", "/account.html", "/account.cfm",

"/account.asp", "/account.jsp", "/accounts/", "/accounts.php",

"/accounts.html", "/accounts.cfm", "/accounts.asp", "/accounts.jsp",

"/client/", "/client.php", "/client.html", "/client.cfm",

"/client.asp", "/client.jsp", "/clients/", "/clients.php",

"/clients.html", "/clients.cfm", "/clients.asp", "/clients.jsp",

"/member/", "/member.php", "/member.html", "/member.cfm",

"/member.asp", "/member.jsp", "/members/", "/members.php",

"/members.html", "/members.cfm", "/members.asp", "/members.jsp",

"/login/", "/login.php", "/login.html", "/login.cfm",

"/login.asp", "/login.jsp", "/wp-login.php", "/security/",

"/security.php", "/security.html", "/security.cfm", "/security.asp",

"/security.jsp", "/secure/", "/secure.php", "/secure.html",

"/secure.cfm", "/secure.asp", "/secure.jsp", "/auth/",

"/auth.php", "/auth.html", "/auth.cfm", "/auth.asp",

"/auth.jsp", "/authenticate/", "/authenticate.php", "/authenticate.html",

"/authenticate.cfm", "/authenticate.asp", "/authenticate.jsp",

"/authentication/", "/authentication.php", "/authentication.html",

"/authentication.cfm", "/authentication.asp", "/authentication.jsp"

]

self.current_wordlist = self.default_wordlist.copy()

# User agent rotation list

self.user_agents = [

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",

"Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"

]

self.setup_gui()

def setup_gui(self):

"""Create the main GUI layout"""

# Main container

main_frame = ttk.Frame(self.root, padding="10")

main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid weights for resizing

self.root.columnconfigure(0, weight=1)

self.root.rowconfigure(0, weight=1)

main_frame.columnconfigure(0, weight=1)

main_frame.rowconfigure(1, weight=1)

# Top section - Input controls

self.create_input_section(main_frame)

# Middle section - Results table

self.create_results_section(main_frame)

# Bottom section - Progress and status

self.create_progress_section(main_frame)

def create_input_section(self, parent):

"""Create the input controls section"""

input_frame = ttk.LabelFrame(parent, text="Scan Configuration", padding="10")

input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

input_frame.columnconfigure(1, weight=1)

# Domain input

ttk.Label(input_frame, text="Target Domain:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

self.domain_var = tk.StringVar()

self.domain_entry = ttk.Entry(input_frame, textvariable=self.domain_var, width=40)

self.domain_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

# Delay setting

ttk.Label(input_frame, text="Delay (seconds):").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))

self.delay_var = tk.StringVar(value="1.0")

delay_spinbox = ttk.Spinbox(input_frame, from_=0.1, to=10.0, increment=0.1, 

textvariable=self.delay_var, width=8)

delay_spinbox.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))

# Control buttons

button_frame = ttk.Frame(input_frame)

button_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))

self.start_button = ttk.Button(button_frame, text="Start Scan", command=self.start_scan)

self.start_button.pack(side=tk.LEFT, padx=(0, 5))

self.stop_button = ttk.Button(button_frame, text="Stop Scan", command=self.stop_scan, state=tk.DISABLED)

self.stop_button.pack(side=tk.LEFT, padx=(0, 5))

ttk.Button(button_frame, text="Import Wordlist", command=self.import_wordlist).pack(side=tk.LEFT, padx=(0, 5))

ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))

ttk.Button(button_frame, text="Save Report", command=self.save_report).pack(side=tk.LEFT)

def create_results_section(self, parent):

"""Create the results table section"""

results_frame = ttk.LabelFrame(parent, text="Scan Results", padding="10")

results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

results_frame.columnconfigure(0, weight=1)

results_frame.rowconfigure(0, weight=1)

# Create Treeview for results

columns = ("URL", "Status Code", "Response Time", "Notes")

self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)

# Define column headings and widths

self.results_tree.heading("URL", text="URL")

self.results_tree.heading("Status Code", text="Status")

self.results_tree.heading("Response Time", text="Time (ms)")

self.results_tree.heading("Notes", text="Notes")

self.results_tree.column("URL", width=400)

self.results_tree.column("Status Code", width=80)

self.results_tree.column("Response Time", width=100)

self.results_tree.column("Notes", width=200)

# Add scrollbar

scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)

self.results_tree.configure(yscrollcommand=scrollbar.set)

# Grid layout

self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

# Configure tags for color coding

self.results_tree.tag_configure("200", background="#d4edda") # Green

self.results_tree.tag_configure("301", background="#fff3cd") # Yellow

self.results_tree.tag_configure("302", background="#fff3cd") # Yellow

self.results_tree.tag_configure("403", background="#f8d7da") # Orange/Red

self.results_tree.tag_configure("404", background="#f8f9fa") # Grey

self.results_tree.tag_configure("default", background="#ffffff") # White

def create_progress_section(self, parent):

"""Create the progress and status section"""

progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")

progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

progress_frame.columnconfigure(0, weight=1)

# Progress bar

self.progress_var = tk.DoubleVar()

self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 

maximum=100, length=400)

self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

# Status label

self.status_var = tk.StringVar(value="Ready to scan")

self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)

self.status_label.grid(row=1, column=0, sticky=tk.W)

def import_wordlist(self):

"""Import custom wordlist from file"""

file_path = filedialog.askopenfilename(

title="Select Wordlist File",

filetypes=[("Text files", "*.txt"), ("All files", "*.*")]

)

if file_path:

try:

with open(file_path, 'r') as file:

custom_wordlist = [line.strip() for line in file if line.strip()]

if custom_wordlist:

self.current_wordlist = custom_wordlist

messagebox.showinfo("Success", f"Loaded {len(custom_wordlist)} paths from wordlist")

else:

messagebox.showwarning("Warning", "No valid paths found in the wordlist")

except Exception as e:

messagebox.showerror("Error", f"Failed to load wordlist: {str(e)}")

def clear_results(self):

"""Clear all results from the table"""

for item in self.results_tree.get_children():

self.results_tree.delete(item)

self.results = []

self.progress_var.set(0)

self.status_var.set("Results cleared")

def start_scan(self):

"""Start the scanning process"""

domain = self.domain_var.get().strip()

if not domain:

messagebox.showerror("Error", "Please enter a target domain")

return

# Validate and format domain

if not domain.startswith(('http://', 'https://')):

domain = 'https://' + domain

try:

parsed = urlparse(domain)

if not parsed.netloc:

raise ValueError("Invalid domain format")

except Exception:

messagebox.showerror("Error", "Invalid domain format")

return

self.is_scanning = True

self.start_button.config(state=tk.DISABLED)

self.stop_button.config(state=tk.NORMAL)

self.domain_entry.config(state=tk.DISABLED)

# Start scanning in background thread

self.scan_thread = threading.Thread(target=self.scan_paths, args=(domain,))

self.scan_thread.daemon = True

self.scan_thread.start()

def stop_scan(self):

"""Stop the scanning process"""

self.is_scanning = False

self.start_button.config(state=tk.NORMAL)

self.stop_button.config(state=tk.DISABLED)

self.domain_entry.config(state=tk.NORMAL)

self.status_var.set("Scan stopped by user")

def scan_paths(self, domain):

"""Scan all paths in the wordlist"""

total_paths = len(self.current_wordlist)

scanned_count = 0

try:

delay = float(self.delay_var.get())

except ValueError:

delay = 1.0

for path in self.current_wordlist:

if not self.is_scanning:

break

# Construct full URL

full_url = urljoin(domain, path)

try:

# Random user agent

headers = {'User-Agent': random.choice(self.user_agents)}

# Make request with timeout

start_time = time.time()

response = requests.get(full_url, headers=headers, timeout=10, allow_redirects=False)

response_time = (time.time() - start_time) * 1000 # Convert to milliseconds

# Determine significance and notes

notes = self.get_status_notes(response.status_code)

# Add result to table (must be done in main thread)

result_data = {

'url': full_url,

'status_code': response.status_code,

'response_time': round(response_time, 2),

'notes': notes

}

self.root.after(0, self.add_result, result_data)

except requests.exceptions.Timeout:

self.root.after(0, self.add_result, {

'url': full_url,

'status_code': 'Timeout',

'response_time': 0,

'notes': 'Request timed out'

})

except requests.exceptions.ConnectionError:

self.root.after(0, self.add_result, {

'url': full_url,

'status_code': 'Error',

'response_time': 0,

'notes': 'Connection failed'

})

except Exception as e:

self.root.after(0, self.add_result, {

'url': full_url,

'status_code': 'Error',

'response_time': 0,

'notes': f'Error: {str(e)[:50]}'

})

scanned_count += 1

progress = (scanned_count / total_paths) * 100

# Update progress

self.root.after(0, self.update_progress, progress, scanned_count, total_paths)

# Delay between requests

if delay > 0 and self.is_scanning:

time.sleep(delay)

# Scan completed

self.root.after(0, self.scan_completed)

def get_status_notes(self, status_code):

"""Get explanatory notes for HTTP status codes"""

status_notes = {

200: "OK - Path exists and accessible",

201: "Created - Resource created successfully",

301: "Moved Permanently - Path redirected",

302: "Found - Path temporarily redirected",

303: "See Other - Path redirected",

307: "Temporary Redirect - Path redirected",

308: "Permanent Redirect - Path redirected",

400: "Bad Request - Invalid request",

401: "Unauthorized - Authentication required",

403: "Forbidden - Access denied (path exists)",

404: "Not Found - Path does not exist",

405: "Method Not Allowed",

500: "Internal Server Error",

502: "Bad Gateway",

503: "Service Unavailable"

}

return status_notes.get(status_code, f"HTTP {status_code}")

def add_result(self, result_data):

"""Add a result to the table (called from main thread)"""

self.results.append(result_data)

# Determine tag for color coding

status_str = str(result_data['status_code'])

if status_str.startswith('2'):

tag = "200"

elif status_str.startswith('3'):

tag = status_str # 301 or 302

elif status_str == "403":

tag = "403"

elif status_str == "404":

tag = "404"

else:

tag = "default"

# Insert into treeview

self.results_tree.insert('', 'end', values=(

result_data['url'],

result_data['status_code'],

f"{result_data['response_time']:.2f}",

result_data['notes']

), tags=(tag,))

# Auto-scroll to latest result

self.results_tree.see(self.results_tree.get_children()[-1])

def update_progress(self, progress, current, total):

"""Update progress bar and status"""

self.progress_var.set(progress)

self.status_var.set(f"Scanning {current}/{total} paths...")

def scan_completed(self):

"""Called when scan is completed"""

self.is_scanning = False

self.start_button.config(state=tk.NORMAL)

self.stop_button.config(state=tk.DISABLED)

self.domain_entry.config(state=tk.NORMAL)

# Count results by status

status_counts = {}

for result in self.results:

status = result['status_code']

status_counts[status] = status_counts.get(status, 0) + 1

# Generate summary

summary_parts = []

for status, count in sorted(status_counts.items()):

summary_parts.append(f"{status}: {count}")

summary = f"Scan completed - {len(self.results)} results found"

if summary_parts:

summary += f" ({', '.join(summary_parts)})"

self.status_var.set(summary)

# Auto-generate report

if self.results:

self.root.after(1000, self.save_report)

def save_report(self):

"""Save scan results to files"""

if not self.results:

messagebox.showwarning("Warning", "No results to save")

return

# Ask user to choose save location

save_dir = filedialog.askdirectory(title="Choose folder to save reports")

if not save_dir:

return

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

domain = self.domain_var.get().strip()

if not domain.startswith(('http://', 'https://')):

domain = 'https://' + domain

base_filename = f"admin_scan_{domain.replace('://', '_').replace('/', '_')}_{timestamp}"

try:

# Generate TXT report

txt_path = os.path.join(save_dir, f"{base_filename}.txt")

self.generate_txt_report(txt_path, domain)

# Generate CSV report

csv_path = os.path.join(save_dir, f"{base_filename}.csv")

self.generate_csv_report(csv_path)

messagebox.showinfo("Success", f"Reports saved to:\n{txt_path}\n{csv_path}")

except Exception as e:

messagebox.showerror("Error", f"Failed to save reports: {str(e)}")

def generate_txt_report(self, filepath, domain):

"""Generate detailed text report"""

with open(filepath, 'w', encoding='utf-8') as f:

f.write("=" * 60 + "\n")

f.write("ADMIN PATH SCANNER REPORT\n")

f.write("=" * 60 + "\n\n")

f.write(f"Target Domain: {domain}\n")

f.write(f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

f.write(f"Total Paths Tested: {len(self.current_wordlist)}\n")

f.write(f"Total Results Found: {len(self.results)}\n\n")

# Status code summary

status_counts = {}

for result in self.results:

status = result['status_code']

status_counts[status] = status_counts.get(status, 0) + 1

f.write("STATUS CODE SUMMARY:\n")

f.write("-" * 30 + "\n")

for status, count in sorted(status_counts.items()):

f.write(f"{status}: {count} paths\n")

f.write("\n")

# Detailed results

f.write("DETAILED RESULTS:\n")

f.write("-" * 30 + "\n\n")

# Group results by status code

results_by_status = {}

for result in self.results:

status = result['status_code']

if status not in results_by_status:

results_by_status[status] = []

results_by_status[status].append(result)

for status in sorted(results_by_status.keys()):

f.write(f"\n{status} RESPONSES:\n")

f.write("~" * 20 + "\n")

for result in results_by_status[status]:

f.write(f"URL: {result['url']}\n")

f.write(f"Response Time: {result['response_time']:.2f}ms\n")

f.write(f"Notes: {result['notes']}\n")

f.write("-" * 40 + "\n")

f.write("\n" + "=" * 60 + "\n")

f.write("END OF REPORT\n")

f.write("=" * 60 + "\n")

def generate_csv_report(self, filepath):

"""Generate CSV report"""

with open(filepath, 'w', newline='', encoding='utf-8') as f:

writer = csv.writer(f)

# Write header

writer.writerow(['URL', 'Status Code', 'Response Time (ms)', 'Notes'])

# Write results

for result in self.results:

writer.writerow([

result['url'],

result['status_code'],

f"{result['response_time']:.2f}",

result['notes']

])



def main():

"""Main entry point"""

root = tk.Tk()

app = AdminPathScanner(root)

root.mainloop()



if __name__ == "__main__":

main()
