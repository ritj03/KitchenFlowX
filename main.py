import mysql.connector
from tkinter import *
from tkinter import messagebox

# Function to execute query and display result in a messagebox
def execute_query(query, query_type=None):
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cloudKitchen',
            port='3307'
        )
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Format the results based on the query type
        if query_type == "Customer Order History":
            formatted_result = "Food Item\t\tFrequency\n"
            for row in results:
                formatted_result += f"{row[0]:<30}{row[1]}\n"
        elif query_type == "Display Menu":
            formatted_result = "Food Item\t\tPrice\t\tAverage Review\n"
            for row in results:
                formatted_result += f"{row[0]:<30}{row[1]:<15}{row[2]}\n"
        else:
            formatted_result = ""
            for row in results:
                formatted_result += ", ".join(map(str, row)) + "\n"

        # Display messagebox with formatted result
        if formatted_result.strip():
            messagebox.showinfo(title="Query Result", message=formatted_result)
        else:
            messagebox.showinfo(title="Query Result", message="No records found.")

    except mysql.connector.Error as e:
        messagebox.showerror(title="Error", message=f"Error executing query: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Function to create GUI and execute queries
def create_gui():
    root = Tk()
    root.title("Cloud Kitchen Management System")
    root.geometry("480x350")

    # Define functions for each query
    def query_orders_between_dates():
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        query = f"SELECT COUNT(*) FROM orders WHERE date_time BETWEEN '{start_date}' AND '{end_date}'"
        execute_query(query)

    def query_display_menu():
        query = """SELECT f.fname, f.price, AVG(o.cust_review) AS avg_review
                   FROM foodItems f
                   LEFT JOIN orderDetails od ON f.foodId = od.foodId
                   LEFT JOIN orders o ON od.oid = o.oid
                   GROUP BY f.fname, f.price"""
        execute_query(query, query_type="Display Menu")

    def query_delivery_count_by_boy():
        query = """SELECT d.did, d.dName, COUNT(*) AS delivery_count
                   FROM deBoy_delivery dd
                   INNER JOIN delivery_boy d ON dd.did = d.did
                   GROUP BY d.did, d.dName"""
        execute_query(query)

    def query_food_items_by_chef():
        ch_id = entry_chef_id.get()
        query = f"SELECT fname FROM foodChef WHERE chid = {ch_id}"
        execute_query(query)

    def query_customer_order_history():
        cust_id = entry_cust_id.get()
        query = f"""SELECT fi.fname, COUNT(*) AS frequency
                    FROM orders o
                    INNER JOIN orderDetails od ON o.oid = od.oid
                    INNER JOIN foodItems fi ON od.foodId = fi.foodId
                    WHERE o.cid = {cust_id}
                    GROUP BY fi.fname"""
        execute_query(query, query_type="Customer Order History")

    # Create labels and entry fields for user input
    lbl_start_date = Label(root, text="Start Date (YYYY-MM-DD):")
    lbl_start_date.pack()
    entry_start_date = Entry(root)
    entry_start_date.pack()

    lbl_end_date = Label(root, text="End Date (YYYY-MM-DD):")
    lbl_end_date.pack()
    entry_end_date = Entry(root)
    entry_end_date.pack()

    lbl_chef_id = Label(root, text="Chef ID:")
    lbl_chef_id.pack()
    entry_chef_id = Entry(root)
    entry_chef_id.pack()

    lbl_cust_id = Label(root, text="Customer ID:")
    lbl_cust_id.pack()
    entry_cust_id = Entry(root)
    entry_cust_id.pack()

    # Create buttons for each query
    btn_orders_between_dates = Button(root, text="Orders Between Dates", command=query_orders_between_dates)
    btn_orders_between_dates.pack()

    btn_display_menu = Button(root, text="Display Menu", command=query_display_menu)
    btn_display_menu.pack()

    btn_delivery_count_by_boy = Button(root, text="Delivery Count by Boy", command=query_delivery_count_by_boy)
    btn_delivery_count_by_boy.pack()

    btn_food_items_by_chef = Button(root, text="Food Items by Chef", command=query_food_items_by_chef)
    btn_food_items_by_chef.pack()

    btn_customer_order_history = Button(root, text="Customer Order History", command=query_customer_order_history)
    btn_customer_order_history.pack()

    root.mainloop()

# Call the function to create GUI and execute queries
create_gui()
