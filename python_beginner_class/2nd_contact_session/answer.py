import os
import re

# =========================
# Question 1:
# =========================
with open("2nd_contact_session/name.txt", "r") as file:
    full_name = file.read().strip()


parts = full_name.split()

first_name = parts[0]
middle_name = parts[1]
last_name = parts[-1]

print(first_name, middle_name, last_name)


# =========================
# Question 2:
# =========================
file_path = os.path.abspath("2nd_contact_session/name.txt")
print("File path:", file_path)


# =========================
# Question 3:
# =========================
with open("2nd_contact_session/baby2008.html", "r") as f:
    content = f.read()


pattern = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'
matches = re.findall(pattern, content)

names = []

for rank, boy, girl in matches:
    names.append((boy, int(rank)))
    names.append((girl, int(rank)))

# implement bubble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][0] > arr[j+1][0]:  # sort by name
                arr[j], arr[j+1] = arr[j+1], arr[j]

bubble_sort(names)

# implement binary search
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid][0] == target:
            return arr[mid]
        elif arr[mid][0] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None

# search for Micheal
result = binary_search(names, "Michael")

if result:
    print(f"Found: {result}")
else:
    print("Not found")