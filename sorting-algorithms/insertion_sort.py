"""
Time complexity: O(n^2)
This sorts the array by iterating over itself, left 
to right. In each iteration, it checks a value from 
the unsorted part and places it at correct position 
in the sorted part.
"""

for i in range(n):
  x = num[i]
  j = i-1
  while j >= 0 and num[j] > x:
    num[j+1] = num[j]
    j -= 1
  num[j+1] = x
