import sqlite3
import pathlib
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
print(PROJECT_ROOT)


def task2(database_file: pathlib.Path | str) -> None:
    query_results = None

    try:
        database_connection = sqlite3.connect(database_file)
        db_cursor = database_connection.cursor()

        # SQL query to get order_id and total_price for each order
        # Need to join orders, line_items, and products tables
        order_totals_query = """
            SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
            FROM orders o
            JOIN line_items li ON o.order_id = li.order_id
            JOIN products p ON li.product_id = p.product_id
            GROUP BY o.order_id
            ORDER BY o.order_id;
        """

        db_cursor.execute(order_totals_query)
        query_results = db_cursor.fetchall()

    except sqlite3.Error as database_error:
        print(f"Database error: {database_error}")
    except Exception as general_error:
        print(f"Unexpected error: {general_error}")
    finally:
        if database_connection:
            database_connection.close()

    if query_results:
        # Create DataFrame with order_id and total_price
        df = pd.DataFrame(query_results, columns=["order_id", "total_price"])
        
        # Method 1: Using apply() with custom cumulative function
        def cumulative(row):
            totals_above = df['total_price'][0:row.name+1]
            return totals_above.sum()
        
        df['cumulative'] = df.apply(cumulative, axis=1)
        
        # Alternative method using cumsum() (commented out since we're using apply method)
        # df['cumulative'] = df['total_price'].cumsum()
        
        # Create line plot of cumulative revenue vs order_id
        df.plot(
            x="order_id",
            y="cumulative",
            kind="line",
            color="blue",
            title="Cumulative Revenue by Order ID",
            xlabel="Order ID",
            ylabel="Cumulative Revenue ($)"
        )
        
        plt.show()


if __name__ == "__main__":
    task2(PROJECT_ROOT / "db/lesson.db")
