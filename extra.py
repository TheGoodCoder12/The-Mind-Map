# Checks for strong password
def isStrong(password):
  spChars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
  a, b, c, d = 0, 0, 0, 0
  for char in password:
    # Checking for lowercase
    if (97 <= ord(char) <= 122):
      a = 1
    # Checking for uppercase
    elif (65 <= ord(char) <= 90):
      b = 1
    # Checking for numeric characters
    elif (48 <= ord(char) <= 57):
      c = 1
    # Checking for special characters
    elif char in spChars:
      d = 1
    # Break the loop if all conditions have been satisfied
    if a == 1 and b == 1 and c == 1 and d == 1:
      break

  if a == 1 and b == 1 and c == 1 and d == 1:
    return True
  else:
    return False