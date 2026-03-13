import random
from itertools import accumulate

# -------------------------------
# Color data (provided)
# -------------------------------
colors = {
    'GREEN': 10,
    'YELLOW': 5,
    'BROWN': 6,
    'BLUE': 31,
    'PINK': 5,
    'ORANGE': 9,
    'CREAM': 2,
    'RED': 9,
    'WHITE': 16,
    'ARSH': 1,
    'BLACK': 1,
}

# Total frequency and number of colors
total_frequencies = sum(colors.values())
color_count = len(colors)

# -------------------------------
# Question 1: Mean color frequency
# -------------------------------
mean_freq = total_frequencies / color_count
print(f"Mean frequency of colors: {mean_freq:.2f}")

# -------------------------------
# Question 2: Most frequently worn color
# -------------------------------
most_worn_color = max(colors, key=colors.get)
print(f"Most frequently worn color: {most_worn_color}")

# -------------------------------
# Question 3: Median color
# -------------------------------
color_items = list(colors.items())  # list of (color, frequency)
cumulative = list(accumulate(freq for color, freq in color_items))
midpoint = total_frequencies / 2
median_color = color_items[next(i for i, cum in enumerate(cumulative) if cum >= midpoint)][0]
print(f"Median color: {median_color}")

# -------------------------------
# Question 4: Variance of color frequencies
# -------------------------------
variance = sum((freq - mean_freq) ** 2 for freq in colors.values()) / color_count
print(f"Variance of color frequencies: {variance:.2f}")

# -------------------------------
# Question 5: Probability of choosing red
# -------------------------------
prob_red = colors.get("RED", 0) / total_frequencies
print(f"Probability of choosing red: {prob_red:.2f}")

# -------------------------------
# Question 6: Save colors and frequencies in PostgreSQL
# -------------------------------
# NOTE: Replace placeholders with your database credentials
'''
import psycopg

conn_info = "dbname=your_db user=your_user password=your_pass host=localhost port=5432"

with psycopg.connect(conn_info) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS color_stats (
                id SERIAL PRIMARY KEY,
                color_name VARCHAR(50) UNIQUE,
                frequency INTEGER
            )
        """)
        insert_query = """
            INSERT INTO color_stats (color_name, frequency)
            VALUES (%s, %s)
            ON CONFLICT (color_name) DO UPDATE 
            SET frequency = EXCLUDED.frequency;
        """
        data_to_insert = list(colors.items())
        cur.executemany(insert_query, data_to_insert)
'''

# -------------------------------
# Question 7: Recursive search in a list
# -------------------------------
def recursive_search(numbers, target):
    if not numbers:
        return False
    if numbers[0] == target:
        return True
    return recursive_search(numbers[1:], target)

# Example usage
sample_list = [1, 3, 5, 7, 9]
target_number = 5
print(f"Recursive search for {target_number} in {sample_list}: {recursive_search(sample_list, target_number)}")

# -------------------------------
# Question 8: Random 4-digit binary to decimal
# -------------------------------
binary_num = "".join(str(random.randint(0, 1)) for _ in range(4))
decimal_value = int(binary_num, 2)
print(f"Random 4-digit binary: {binary_num} -> Decimal: {decimal_value}")

# -------------------------------
# Question 9: Sum of first 50 Fibonacci numbers
# -------------------------------
def sum_fibonacci(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_sum_50 = sum_fibonacci(50)
print(f"Sum of first 50 Fibonacci numbers: {fib_sum_50}")