import sqlite3
import pathlib
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
print(PROJECT_ROOT)


def task1(database_file: pathlib.Path | str) -> None:
    query_results = None

    try:
        database_connection = sqlite3.connect(database_file)
        db_cursor = database_connection.cursor()

        # Alternative query approach for reference
        reference_query = """
            SELECT last_name, SUM(price * quantity) AS revenue
            FROM employees e 
            JOIN orders o ON e.employee_id = o.employee_id 
            JOIN line_items l ON o.order_id = l.order_id 
            JOIN products p ON l.product_id = p.product_id 
            GROUP BY e.employee_id;
        """

        revenue_query = """
            SELECT emp.last_name, SUM(prod.price * items.quantity) AS total_revenue
            FROM employees emp
            JOIN orders ord
                ON emp.employee_id = ord.employee_id 
            JOIN line_items items
                ON items.order_id = ord.order_id
            JOIN products prod
                ON prod.product_id = items.product_id
            GROUP BY emp.employee_id;
        """

        db_cursor.execute(revenue_query)
        query_results = db_cursor.fetchall()

    except sqlite3.Error as database_error:
        print(f"Database error: {database_error}")
    except Exception as general_error:
        print(f"Unexpected error: {general_error}")
    finally:
        if database_connection:
            database_connection.close()

    if query_results:
        revenue_dataframe = pd.DataFrame(query_results, columns=["employee_name", "total_revenue"])
        revenue_dataframe.plot(
            x="employee_name",
            y="total_revenue",
            kind="bar",
            color="purple",
            title="Employee Revenue Analysis",
        )

        plt.show()


if __name__ == "__main__":
    task1(PROJECT_ROOT / "db/lesson.db")