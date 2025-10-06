import plotly.express as px
import plotly.data as pldata
import pandas as pd
import re


def task3():
    df = pldata.wind(return_type='pandas')
    
    print("First 10 lines of the DataFrame:")
    print(df.head(10))
    print("\nLast 10 lines of the DataFrame:")
    print(df.tail(10))
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nDataFrame columns: {df.columns.tolist()}")
    print(f"\nData types before cleaning:")
    print(df.dtypes)
    
    print(f"\nSample 'strength' values before cleaning:")
    print(df['strength'].head(10))
    
    # Clean the data - convert 'strength' column to float
    # The strength column contains ranges like "0-1", "2-3", "4-5", "6+"
    # We'll convert these to their midpoint values or representative values
    def convert_strength(strength_str):
        strength_str = str(strength_str).strip()
        if '-' in strength_str:
            # Handle ranges like "0-1", "2-3", "4-5"
            parts = strength_str.split('-')
            if len(parts) == 2:
                try:
                    start = float(parts[0])
                    end = float(parts[1])
                    return (start + end) / 2  # Return midpoint
                except ValueError:
                    return None
        elif '+' in strength_str:
            # Handle "6+" case
            try:
                base = float(strength_str.replace('+', ''))
                return base + 1  # Use base + 1 as representative value
            except ValueError:
                return None
        else:
            # Try to convert directly to float
            try:
                return float(strength_str)
            except ValueError:
                return None
    
    df['strength'] = df['strength'].apply(convert_strength)
    
    print(f"\nSample 'strength' values after cleaning:")
    print(df['strength'].head(10))
    print(f"\nData types after cleaning:")
    print(df.dtypes)
    
    # Check for any NaN values after conversion
    nan_count = df['strength'].isna().sum()
    if nan_count > 0:
        print(f"\nWarning: {nan_count} NaN values found in 'strength' column after conversion")
        # Remove rows with NaN values
        df = df.dropna(subset=['strength'])
        print(f"Removed NaN values. New DataFrame shape: {df.shape}")
    
    # Create an interactive scatter plot
    fig = px.scatter(
        df,
        x='strength',
        y='frequency',
        color='direction',
        title='Wind Data: Strength vs Frequency by Direction',
        labels={
            'strength': 'Wind Strength',
            'frequency': 'Frequency',
            'direction': 'Wind Direction'
        },
        hover_data=['direction', 'strength', 'frequency']
    )
    
    # Update layout for better appearance
    fig.update_layout(
        width=800,
        height=600,
        showlegend=True
    )
    
    # Save the plot as HTML file
    html_filename = 'wind.html'
    fig.write_html(html_filename)
    print(f"\nInteractive plot saved as '{html_filename}'")
    
    # Show the plot
    fig.show()
    
    # Verify the HTML file was created
    import pathlib
    html_path = pathlib.Path(html_filename)
    if html_path.exists():
        print(f"✓ HTML file '{html_filename}' successfully created")
        print(f"  File size: {html_path.stat().st_size} bytes")
    else:
        print(f"✗ Error: HTML file '{html_filename}' was not created")


if __name__ == "__main__":
    task3()
