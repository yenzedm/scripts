import bcrypt

# User password to be hashed
password = b"ubuntu"

# 1. Generate salt
# Bcrypt automatically includes salt in the resulting hash
salt = bcrypt.gensalt()

# 2. Hash the password using the salt
hashed_password = bcrypt.hashpw(password, salt)

# Print the resulting hash
print(f"Hashed password: {hashed_password}")

# Password verification
# When user logs in, compare their entered password with the hash
user_password_to_check = b"ubuntu"

if bcrypt.checkpw(user_password_to_check, hashed_password):
    print("Password is correct!")
else:
    print("Password is incorrect!")