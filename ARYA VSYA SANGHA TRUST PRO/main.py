import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import os
import threading

# Database Setup
def create_tables():
    conn = sqlite3.connect('arya_vasya.db')
    c = conn.cursor()
    
    # Household Table
    c.execute('''CREATE TABLE IF NOT EXISTS households
                 (address_id TEXT PRIMARY KEY,
                  owner_name TEXT,
                  owner_age INTEGER,
                  owner_occupation TEXT,
                  owner_designation TEXT,
                  mobile TEXT,
                  address TEXT,
                  owner_photo BLOB)''')
                  
    # Family Members Table
    c.execute('''CREATE TABLE IF NOT EXISTS family_members
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  address_id TEXT,
                  name TEXT,
                  age INTEGER,
                  relation TEXT,
                  occupation TEXT,
                  designation TEXT,
                  mobile TEXT,
                  photo BLOB,
                  FOREIGN KEY(address_id) REFERENCES households(address_id))''')
    conn.commit()
    conn.close()

# Main Application Class
class AryaVasyaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arya Vasya Sangha Trust")
        self.root.geometry("1200x800")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Colors and Fonts
        self.bg_color = "#f0f0f0"
        self.primary_color = "#800000"  # Maroon
        self.secondary_color = "#FFD700"  # Gold
        self.font = ("Helvetica", 12)

        # Set Application Icon
        self.set_icon("E:\ARYA VSYA SANGHA TRUST PRO\LOGO\icon1.ico")  # Replace with your icon file path
        
        # Add Logo
        self.add_logo()
        
        # Create a main frame to hold all widgets
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create widgets
        self.create_widgets()
        create_tables()

    def set_icon(self, icon_path):
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"Icon file not found at {icon_path}")

    def add_logo(self):
        try:
            logo_path = "images.png"  # Replace with your logo file path
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(logo_image)
                logo_label = tk.Label(self.root, image=self.logo)
                logo_label.pack(pady=10)
            else:
                print(f"Logo file not found at {logo_path}")
        except Exception as e:
            print(f"Error loading logo: {e}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Add Member Tab
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Member")
        self.create_add_tab()

        # Search/Edit Tab
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text="Search/Edit")
        self.create_search_tab()

        # Footer
        self.create_footer()

    def create_add_tab(self):
        hh_frame = ttk.LabelFrame(self.add_tab, text="Household Details", style='Custom.TLabelframe')
        hh_frame.pack(pady=10, padx=20, fill="x")

        labels = ["Address ID:", "Owner Name:", "Owner Age:", "Occupation:", 
                 "Designation:", "Mobile:", "Address:"]
        self.entries = {}
        
        for i, text in enumerate(labels):
            lbl = ttk.Label(hh_frame, text=text, width=15, font=self.font)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(hh_frame, width=40, font=self.font)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            key = text.replace(" ", "_").lower().rstrip(':')
            self.entries[key] = entry

        # Upload Owner Photo Button
        self.owner_photo_path = None
        upload_photo_btn = ttk.Button(hh_frame, text="Owner Photo", 
                                    command=self.upload_owner_photo, style='Primary.TButton')
        upload_photo_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

        hh_frame.grid_columnconfigure(1, weight=1)

        # Family Members Frame
        family_frame = ttk.LabelFrame(self.add_tab, text="Family Members", style='Custom.TLabelframe')
        family_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.family_tree = ttk.Treeview(family_frame, columns=("Name", "Age", "Relation", 
                                      "Occupation", "Designation", "Mobile", "Photo"), show='headings')
        for col in ("Name", "Age", "Relation", "Occupation", "Designation", "Mobile", "Photo"):
            self.family_tree.heading(col, text=col)
            self.family_tree.column(col, width=120, stretch=True)
        self.family_tree.pack(fill="both", expand=True)

        add_member_btn = ttk.Button(self.add_tab, text="Add Family Member", 
                                  command=self.open_member_dialog, style='Primary.TButton')
        add_member_btn.pack(pady=10)

        submit_btn = ttk.Button(self.add_tab, text="Submit Household", 
                              command=self.save_household, style='Success.TButton')
        submit_btn.pack(pady=20)

        clear_btn = ttk.Button(self.add_tab, text="Clear", 
                              command=self.clear_add_tab, style='Danger.TButton')
        clear_btn.pack(pady=10)

    def upload_owner_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.owner_photo_path = file_path

    def clear_add_tab(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for row in self.family_tree.get_children():
            self.family_tree.delete(row)
        self.owner_photo_path = None

    def open_member_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Family Member")
        dialog.geometry("400x400")

        fields = ["Name:", "Age:", "Relation:", "Occupation:", "Designation:", "Mobile:"]
        self.member_entries = {}
        
        for i, text in enumerate(fields):
            lbl = ttk.Label(dialog, text=text, font=self.font)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(dialog, width=30, font=self.font)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.member_entries[text.split(':')[0].lower()] = entry

        self.member_photo_path = None
        upload_photo_btn = ttk.Button(dialog, text="Upload Photo", 
                                    command=lambda: self.upload_member_photo(dialog), style='Primary.TButton')
        upload_photo_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(dialog, text="Save", 
                            command=lambda: self.save_family_member(dialog), style='Primary.TButton')
        save_btn.grid(row=len(fields) + 1, column=1, pady=10)

    def upload_member_photo(self, dialog):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.member_photo_path = file_path

    def save_family_member(self, dialog):
        data = [self.member_entries[field].get() for field in ["name", "age", "relation", "occupation", "designation", "mobile"]]
        
        # Validate Age
        try:
            int(data[1])
        except ValueError:
            messagebox.showerror("Error", "Age must be a valid number!")
            return
        
        if all(data):
            self.family_tree.insert('', 'end', values=(*data, self.member_photo_path))
            for entry in self.member_entries.values():
                entry.delete(0, tk.END)
            dialog.destroy()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    def save_household(self):
        # Validate Household Fields
        household_data = {k: v.get() for k, v in self.entries.items()}
        required_fields = ["address_id", "owner_name", "owner_age", "mobile", "address"]
        
        # Check empty fields
        for field in required_fields:
            if not household_data.get(field):
                messagebox.showerror("Error", f"Field '{field.replace('_', ' ').title()}' is required!")
                return
        
        # Validate Age
        try:
            owner_age = int(household_data["owner_age"])
        except ValueError:
            messagebox.showerror("Error", "Owner Age must be a valid number!")
            return

        try:
            conn = sqlite3.connect('arya_vasya.db')
            c = conn.cursor()
            
            # Read owner photo
            owner_photo = None
            if self.owner_photo_path:
                with open(self.owner_photo_path, "rb") as f:
                    owner_photo = f.read()
            
            # Insert household
            c.execute('''INSERT INTO households 
                         (address_id, owner_name, owner_age, owner_occupation, owner_designation, mobile, address, owner_photo)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                     (household_data["address_id"], household_data["owner_name"], owner_age,
                      household_data.get("occupation", ""), household_data.get("designation", ""),
                      household_data["mobile"], household_data["address"], owner_photo))
            
            # Insert family members
            family_members = [self.family_tree.item(child)['values'] 
                            for child in self.family_tree.get_children()]
            for member in family_members:
                # Validate member age
                try:
                    member_age = int(member[1])
                except ValueError:
                    messagebox.showerror("Error", f"Invalid age for {member[0]}!")
                    return
                
                # Read member photo
                member_photo = None
                if member[6]:
                    with open(member[6], "rb") as f:
                        member_photo = f.read()
                
                c.execute('''INSERT INTO family_members 
                            (address_id, name, age, relation, occupation, designation, mobile, photo)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (household_data["address_id"], member[0], member_age, member[2], 
                          member[3], member[4], member[5], member_photo))
            
            conn.commit()
            messagebox.showinfo("Success", "Data saved successfully!")
            self.clear_add_tab()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Address ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def create_search_tab(self):
        search_frame = ttk.LabelFrame(self.search_tab, text="Search Household", style='Custom.TLabelframe')
        search_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ttk.Entry(search_frame, width=40, font=self.font)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        search_btn = ttk.Button(search_frame, text="Search", 
                              command=self.search_household, style='Primary.TButton')
        search_btn.grid(row=0, column=1, padx=5, pady=5)

        self.search_tree = ttk.Treeview(self.search_tab, columns=("Address ID", "Owner Name", 
                                      "Age", "Occupation", "Designation", "Mobile", "Address", "Photo"), show='headings')
        for col in ("Address ID", "Owner Name", "Age", "Occupation", "Designation", "Mobile", "Address", "Photo"):
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120, stretch=True)
        self.search_tree.pack(pady=10, padx=20, fill="both", expand=True)

        delete_btn = ttk.Button(self.search_tab, text="Delete Selected", 
                               command=self.delete_household, style='Danger.TButton')
        delete_btn.pack(pady=10)

        clear_btn = ttk.Button(self.search_tab, text="Clear", 
                              command=self.clear_search_tab, style='Danger.TButton')
        clear_btn.pack(pady=10)

    def clear_search_tab(self):
        self.search_entry.delete(0, tk.END)
        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

    def search_household(self):
        address_id = self.search_entry.get().strip()
        if not address_id:
            messagebox.showwarning("Error", "Please enter an Address ID!")
            return

        def search():
            try:
                conn = sqlite3.connect('arya_vasya.db')
                c = conn.cursor()
                
                c.execute('''SELECT * FROM households WHERE address_id = ?''', (address_id,))
                household = c.fetchone()
                
                if household:
                    for row in self.search_tree.get_children():
                        self.search_tree.delete(row)
                    
                    self.search_tree.insert('', 'end', values=household)
                    
                    c.execute('''SELECT name, age, relation, occupation, designation, mobile, photo 
                                 FROM family_members WHERE address_id = ?''', (address_id,))
                    family_members = c.fetchall()
                    
                    for member in family_members:
                        self.search_tree.insert('', 'end', values=("", *member))
                else:
                    messagebox.showinfo("Not Found", "No household found with this Address ID!")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

        # Run the search in a separate thread to avoid freezing the UI
        threading.Thread(target=search).start()

    def delete_household(self):
        selected = self.search_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Please select a household to delete!")
            return

        address_id = self.search_tree.item(selected[0])['values'][0]
        try:
            conn = sqlite3.connect('arya_vasya.db')
            c = conn.cursor()
            
            c.execute('''DELETE FROM family_members WHERE address_id = ?''', (address_id,))
            c.execute('''DELETE FROM households WHERE address_id = ?''', (address_id,))
            conn.commit()
            messagebox.showinfo("Success", "Household deleted successfully!")
            self.clear_search_tab()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def create_footer(self):
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill="x", pady=10)
        footer_label = ttk.Label(footer_frame, text="2025 Arya Vyas Sangha Trust - Privacy Protected", 
                                 font=("Helvetica", 10), foreground="gray")
        footer_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AryaVasyaApp(root)
    root.mainloop()