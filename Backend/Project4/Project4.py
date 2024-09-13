import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
import csv
import sys  # Import sys module for exiting the application

class UserAgreementPopup:
    def __init__(self, master):
        self.master = master
        self.agreed = False

        self.top = tk.Toplevel(master)
        self.top.title("User Agreement")
        self.top.geometry("828x360")

        agreement_text = """
        Welcome to the Bug Tracking System!

        By using this software, you agree to comply with all terms and conditions outlined in the End User License Agreement (EULA).

        Terms of Use:
        
        1. You agree to use this software for tracking and managing bugs in software projects.
        2. You agree not to use this software for any illegal or unauthorized purpose.
        3. You agree to provide accurate and truthful bug reports.

        Do you agree to the terms of the EULA?

        """

        label = tk.Label(self.top, text=agreement_text, font=("Helvetica", 14), justify=tk.LEFT, padx=20, pady=20)
        label.pack(expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=20)

        agree_button = tk.Button(button_frame, text="I Agree", command=self.on_agree)
        agree_button.pack(side=tk.LEFT, padx=10)

        disagree_button = tk.Button(button_frame, text="I Disagree", command=self.on_disagree)
        disagree_button.pack(side=tk.LEFT, padx=10)

    def on_agree(self):
        self.agreed = True
        self.top.destroy()

    def on_disagree(self):
        self.top.destroy()
        sys.exit()  # Exit the application if Disagree button is clicked


class HelpFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Create help content widgets (labels, text boxes, etc.)
        self.help_label = tk.Label(
            self, text="""
        Welcome to the Bug Tracking System! This application helps you track and manage bugs in your software projects.

        To submit a bug:
            1. Enter the bug details in the designated fields.
            2. Select the appropriate status.
            3. Click the 'Submit Bug' button.

        To view and update existing bug reports (placeholder):
            1. Click the 'View All Bugs' button (not implemented yet).
            2. Select a bug from the list (not implemented yet).
            3. You can view details and add comments in the separate window (placeholder).

        For further assistance (placeholder), click the 'Help' button (not implemented yet).
        """, font=("Arial", 12)
        )
        self.help_label.pack(padx=10, pady=10)

        self.pack_forget()  # Initially hidden

class ViewBugFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        self.csv_file = 'bug_data.csv'
        self.update_window = None

        self.bug_data = self.read_bug_data()  # Fetch bug data from CSV
        self.create_bug_table()

    def read_bug_data(self):
        """
        Reads bug data from 'bug_data.csv' and returns a list of dictionaries.
        Each dictionary represents a bug with key-value pairs for details.

        Raises:
            FileNotFoundError: If the 'bug_data.csv' file is not found.
        """
        bug_data = []
        try:
            with open("bug_data.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    bug_data.append(row)
        except FileNotFoundError:
            print("Error: 'bug_data.csv' file not found.")
        return bug_data

    def create_update_button(self, bug_id):
        """
        Creates an 'Update' button for a specific bug and assigns the update_bug function
        as its command.

        Args:
            bug_id: The ID of the bug for which the update button is created.
        """
        def update_bug():
            bug_data = self.find_bug_by_id(bug_id)
            if bug_data:
                self.show_update_window(bug_data)

        update_button = tk.Button(self, text="Update", command=update_bug)
        return update_button

    def find_bug_by_id(self, bug_id):
        if self.csv_file:
            bug_data_list = self.read_bug_data()  # Read bug data (assuming returns a list of dictionaries)

            if bug_data_list:  # Check if list is not empty
                for bug_entry in bug_data_list:  # Iterate through bug data entries
                    if bug_entry['bug_id'] == str(bug_id):
                        print(f"Bug with ID {bug_id} found:")
                        print(bug_entry)  # Print the dictionary containing bug data
                        return bug_entry  # Optionally return the matching bug data
                else:
                    print(f"No bug found with ID {bug_id}.")
        else:
            print("Error: CSV file not found.")
        return None  # Optional: Return None if no bug found or error


    def show_update_window(self, bug_data):
        # Create a new window for updating bug details
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title(f"Update Bug: {bug_data['bug_id']}")

        # Create labels and entry fields for updating bug information
        update_labels = {}
        update_entries = {}
        for field_name in bug_data.keys():
            update_label = tk.Label(self.update_window, text=field_name)
            update_label.pack(anchor=tk.W)

            update_entry = tk.Entry(self.update_window, width=30)
            update_entry.insert(tk.END, bug_data[field_name])  # Pre-fill with existing data
            update_entry.pack(anchor=tk.W)

            update_labels[field_name] = update_label
            update_entries[field_name] = update_entry

        # Submit button to update the bug in the DataFrame
        submit_button = tk.Button(self.update_window, text="Update Bug", command=lambda: self.update_bug_in_csv(bug_data.copy(), update_entries))
        submit_button.pack()

    def update_bug_in_csv(self, old_data, updated_data):
        if self.csv_file:
            # Read bug data list
            bug_data_list = self.read_bug_data()

            # Find the bug index using dictionary comprehension
            bug_index = [i for i, data in enumerate(bug_data_list) if data['bug_id'] == old_data['bug_id']]

            if bug_index:  # Check if bug found (avoid potential IndexError)
                bug_index = bug_index[0]  # Get the first matching index (assuming unique bug_id)

                # Update the bug data in the list
                for field_name, update_entry in updated_data.items():
                    bug_data_list[bug_index][field_name] = update_entry.get()

                # Write the updated bug data list back to CSV using pandas
                df = pd.DataFrame(bug_data_list)  # Create DataFrame from list for writing
                df.to_csv(self.csv_file, index=False)  # Write DataFrame to CSV

                # Update the CSV file path (consider error handling)
                self.csv_file = os.path.abspath(self.csv_file)  # Get absolute path

                # Confirmation message and UI update
                if messagebox.askokcancel("Bug Update", f"Bug {old_data['bug_id']} updated successfully!"):
                    print("Bug Updated!")  # Call your actual UI update function
                    self.update_window.destroy()
                    self.bug_data = self.read_bug_data()  # Fetch bug data from CSV
                    self.create_bug_table()

            else:
                print("Bug not found!")  # Inform user if no bug found

    def create_bug_table(self):
        """
        Creates a table displaying bug details and update buttons.
        """
        # Table styling
        table_style = ttk.Style()
        table_style.configure("BugTable.Row", background="#f5f5f5")
        # Column headers
        # bug_id,date,scope,network_location,first_responder,manager,server_id,status
        header_labels = ["Bug ID", "Date", "Scope","network Location","First Responder","Manager","Server ID", "Status", "Update"]
        for i, label_text in enumerate(header_labels):
            label = tk.Label(self, text=label_text, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky=tk.W)
            table_style.configure(f"Header.{i}", foreground="black", background="#d3d3d3", sticky=tk.W)  # Header styling


        # Bug data rows
        for row_index, bug in enumerate(self.bug_data, start=1):
            for col_index, value in enumerate(bug.items()):
                label = tk.Label(self, text=value[1], font=("Arial", 12))  # Extract value from key-value pair
                label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky=tk.W)
                table_style.configure(f"Row.{row_index}.{col_index}", borderwidth=1, relief="groove")  # Cell borders


                # Update button for each bug
                update_button = self.create_update_button(bug["bug_id"])  # Pass bug ID for specific update
                update_button.grid(row=row_index, column=len(header_labels) - 1, padx=5, pady=5)
            

class BugTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Bug Tracking System")
        self.master.geometry("1000x600")
        self.show_submit_form = False 
        self.is_view_bug_frame_visible = False 
        self.is_help_frame_visible = False
        label_title = tk.Label(root, text="BUG TRACKING SYSTEM", font=("Algerian", 36), background="Darkorange3")
        label_title.pack(pady=10)

        # Variable to store the CSV file path
        self.csv_file = 'bug_data.csv'
        self.bug_data = None  # Initialize to None
        

        # Welcome message frame
        self.welcome_frame = tk.Frame(master)
        self.welcome_frame.pack(padx=10, pady=10)

        self.welcome_label = tk.Label(self.welcome_frame, text="Welcome to the Bug Tracking System!\nThis application helps you track and manage bugs in your software projects.")
        self.welcome_label.pack()

        # Instructions frame
        self.instructions_frame = tk.Frame(master)
        self.instructions_frame.pack(padx=10, pady=10)

        # Button frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(padx=10, pady=10)

        self.create_beautiful_button(self.button_frame,"Submit New Bug",self.toggle_submit_form,tk.LEFT)
        self.create_beautiful_button(self.button_frame,"View Bugs",self.toggle_view_bug_frame,tk.LEFT)
        self.create_beautiful_button(self.button_frame,"Help",self.toggle_help_frame,tk.RIGHT)

        # Submit Bug section
        self.submit_frame = tk.Frame(master, bg="dodgerblue", padx=10, pady=10)

        label_style = {"font": ("Arial", 10, "bold"), "foreground": "Orange", "anchor": tk.W}

        self.labels = {
            "bug_id": ttk.Label(self.submit_frame, text="Bug ID:", **label_style),
            "date": ttk.Label(self.submit_frame, text="Date (YYYY-MM-DD):" ,**label_style),
            "scope": ttk.Label(self.submit_frame, text="Scope:" ,**label_style),
            "network_location": ttk.Label(self.submit_frame, text="Network Location:" ,**label_style),
            "first_responder": ttk.Label(self.submit_frame, text="First Responder:" ,**label_style),
            "manager": ttk.Label(self.submit_frame, text="Manager:" ,**label_style),
            "server_id": ttk.Label(self.submit_frame, text="Server ID:" ,**label_style),
            "status": ttk.Label(self.submit_frame, text="Status:" ,**label_style),
        }
        self.entries = {
            "bug_id": tk.Entry(self.submit_frame, width=20),
            "date": tk.Entry(self.submit_frame, width=20),
            "scope": tk.Entry(self.submit_frame, width=20),
            "network_location": tk.Entry(self.submit_frame, width=20),
            "first_responder": tk.Entry(self.submit_frame, width=20),
            "manager": tk.Entry(self.submit_frame, width=20),
            "server_id": tk.Entry(self.submit_frame, width=20),
        }
        self.status_var = tk.StringVar()  # Variable for selected status
        self.status_dropdown = ttk.Combobox(
            self.submit_frame, textvariable=self.status_var, state="readonly"
        )
        self.status_dropdown["values"] = ["Open", "In Progress", "Fixed", "Closed"]

        row = 0
        for label_text, label in self.labels.items():
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            detail_entry = self.entries.get(label_text)  # Get entry from dictionary
            if label_text == "status":
                detail_entry = self.status_dropdown
            detail_entry.grid(row=row, column=1, sticky=tk.W + tk.E, pady=5)
            row += 1

        self.submit_button = tk.Button(self.submit_frame, text="Submit Bug", command=self.submit_bug, width=12)
        self.clear_button = tk.Button(self.submit_frame, text="Clear", command=self.clear_fields, width=8)

        self.submit_button.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        self.clear_button.grid(row=row+1, column=0, columnspan=2, padx=10, pady=10)
        row += 2


    def toggle_help_frame(self):
      """
      Toggles the visibility of the Help Frame.
      """
      self.is_help_frame_visible = not self.is_help_frame_visible

      if self.is_help_frame_visible:
          if self.is_view_bug_frame_visible:
              self.toggle_view_bug_frame
          if self.show_submit_form:
              self.toggle_submit_form
          # Create Help Frame instance only once (if not using a separate class)
          if not hasattr(self, 'help_frame'):
              self.help_frame = HelpFrame(self.master)

          # Center the Help Frame
          self.help_frame.pack()
          self.help_frame.lift()  # Ensure Help Frame is on top of other elements
      else:
          self.help_frame.pack_forget()


    def toggle_view_bug_frame(self):
        """
        Toggles the visibility of the ViewBugFrame.
        """
        self.is_view_bug_frame_visible = not self.is_view_bug_frame_visible

        if self.is_view_bug_frame_visible:
            if self.is_help_frame_visible:
                self.toggle_help_frame
            if self.show_submit_form:
                self.toggle_submit_form
            self.view_bug_frame = ViewBugFrame(self.master)
            self.view_bug_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.view_bug_frame.pack_forget()
            self.view_bug_frame = None 


    def create_beautiful_button(self, root, text, command,side):
        button = tk.Button(
            root,
            text=text,
            font=("Arial", 18, "bold"),  # Bold font with size 18
            padx=20,  # Padding on x-axis
            pady=10,  # Padding on y-axis
            background="#4CAF50",  # Green background
            foreground="black",  # White text
            borderwidth=5,  # Border width
            highlightthickness=0,  # Remove default border highlight
            relief="raised",  # Raised button style
            command=command
            
        )
        button.pack(side=side,padx=5,pady=5)

    def toggle_submit_form(self):
      """
      Toggles the visibility of the submit bug form.
      """
      self.show_submit_form = not self.show_submit_form  # Invert current state

      # Show or hide the submit_frame based on the variable
      if self.show_submit_form:
        if self.is_view_bug_frame_visible:
            self.toggle_view_bug_frame
        if self.is_help_frame_visible:
            self.toggle_help_frame

        self.submit_frame.pack(fill=tk.X)  # Show the submit form
      else:
          self.submit_frame.pack_forget()  # Hide the submit form

    def submit_bug(self):
        bug_data = {
            "bug_id": self.entries["bug_id"].get().strip(),
            "date": self.entries["date"].get().strip(),
            "scope": self.entries["scope"].get().strip(),
            "network_location": self.entries["network_location"].get().strip(),
            "first_responder": self.entries["first_responder"].get().strip(),
            "manager": self.entries["manager"].get().strip(),
            "server_id": self.entries["server_id"].get().strip(),
            "status": self.status_var.get(),
        }

        # Basic data validation (optional, refine based on your needs)
        validation_errors = []
        if not bug_data["bug_id"]:
            validation_errors.append("Bug ID is required.")
        # Add more validation checks as needed (e.g., date format)

        if validation_errors:
            error_message = "\n".join(validation_errors)
            error_window = tk.Tk()
            error_window.title("Bug Tracker - Error")
            error_label = tk.Label(error_window, text=error_message, wraplength=300)
            error_label.pack(padx=10, pady=10)
            error_button = tk.Button(error_window, text="OK", command=error_window.destroy)
            error_button.pack(pady=10)
            error_window.mainloop()
            return  # Don't proceed if there are validation errors

        # Open the CSV file in 'a' (append) mode. This creates the file if it doesn't exist.
        with open(self.csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            try:
                # Attempt to read the CSV file
                df = pd.read_csv(self.csv_file)
            except FileNotFoundError:
                # Create an empty DataFrame if file doesn't exist
                df = pd.DataFrame(columns=list(bug_data.keys()))
            except pd.errors.EmptyDataError:
                # Handle case of empty file with delimiter (optional)
                print("The CSV file appears to be empty. Consider adding data.")
                df = pd.DataFrame(columns=list(bug_data.keys()))  # Create empty DataFrame with columns


        # Append the new bug data as a row in the DataFrame
        df = df._append(bug_data, ignore_index=True)  # Add new row, ignoring potential index issues

        # Save the updated DataFrame back to the CSV file
        df.to_csv(self.csv_file, index=False)  # Don't write index column

        # Clear entry fields after successful submission
        self.clear_fields()

        # Confirmation message and UI update (optional)
        if messagebox.askokcancel("Bug Submitted", f"Bug {bug_data['bug_id']} submitted successfully. Update UI?"):
            print("Bug submitted!")

    def clear_fields(self):
        for entry in self.entries.values():
                entry.delete(0, tk.END)
        self.status_var.set("Open")  # Reset status to default
        self.toggle_submit_form()

if __name__ == "__main__":
    root = tk.Tk()
    user_agreement = UserAgreementPopup(root)
    bug_tracker = BugTracker(root)
    root.mainloop()

