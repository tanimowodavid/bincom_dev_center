import random

"""
I will start by extracting all the colors and frequency in a dictionary
"""
colors = {
    'GREEN': 10,
    'YELLOW': 5,
    'BROWN': 6,
    'BLUE': 31,
    'PINK': 5,
    'ORANGE': 9,
    'CREAM': 2,
    'RED': 9,
    'WHITE':16,
    'ARSH': 1,
    'BLACK': 1,
}

color_count = len(colors)
total_frequencies = sum(value for value in colors.values())

# Question 1: find mean color (total / count)
def get_mean(total, count):
    mean = total/count
    print(f"The mean value is {mean}")

get_mean(total_frequencies, color_count) # output 8.6


# Question 2: Which color is mostly worn? (highest frequency)
def frequent_color(colors):
    highest = 0
    color_name = ''
    for color in colors:
        color_frequency = colors[color]
        if color_frequency > highest:
            highest = color_frequency
            color_name = color
    print(f"The color mostly worn throughout the week is {color_name}")

frequent_color(colors) # output BLUE


# Question 3: Which color is the median?
"""
To find the median color, i will find the midpoint of the total frequency then 
iterate through the dictionary till the value at the midpoint is gotten.
"""

midpoint = total_frequencies/2
def median_color(colors):
    current_sum = 0
    color_name = ''
    for color in colors:
        current_sum += colors[color]
        if current_sum > midpoint:
            color_name = color
            break
    print(f"The median color is {color_name}")

median_color(colors)

# Question 4: Get the variance of the colors
"""
Variance is given by the square of the standard deviation
(sum(x - xprime)^2) / color_count.

To find the variance, i will create a list containing the values of (x - xprime)^2, where x = 8.64
"""
x_xprimes = [(8.64 - value)**2 for value in colors.values()]

variance = (sum(x_xprimes) / color_count)**2
print(f"The variance is {variance}")


# Question 5: if a colour is chosen at random, what is the probability that the color is red?
probability_of_red = colors["RED"] / total_frequencies
print(f"Probability of chosing a red is {probability_of_red}")


# Question 6: Save the colours and their frequencies in postgresql database
'''
This code will break my code as its just a demo so i will comment it out

import psycopg

# Connect to your Postgres database
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

        # Convert dictionary to a list of tuples for executemany
        data_to_insert = list(colors.items())
        
        cur.executemany(insert_query, data_to_insert)'''


# Question 7: write a recursive searching algorithm to search for a number entered by user in a list of numbers.
"""
To solve this, i will assume a list of numbers will be provided and a target.
"""
def recursive_search(numbers, target):
    # Check if there are numbers in the list
    if not numbers:
        return False

    # Check if the first item is our target
    if numbers[0] == target:
        return True

    # Call the function again, but skip the first item
    return recursive_search(numbers[1:], target)


# Question 8: Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
binary = "".join(str(random.randint(0, 1)) for _ in range(4))
base_ten_val = int(binary, 2)
print(f"Generated binary is {binary} and the converted binary is {base_ten_val}")


# Question 9: Write a program to sum the first 50 fibonacci sequence.
def sum_fibonacci(n):
    if n <= 0:
        return 0
    
    fib_sum = 0
    a, b = 0, 1  # Starting numbers: 0, 1
    
    for i in range(n):
        fib_sum += a
        # Calculate next number: a becomes b, b becomes the sum of the two
        a, b = b, (a + b)
        
    return fib_sum

total = sum_fibonacci(50)
print(f"The sum of the first 50 Fibonacci numbers is: {total:,}")
