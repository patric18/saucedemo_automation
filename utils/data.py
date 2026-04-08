USER = "standard_user"
PASSWORD = "secret_sauce"


INVALID_USERS = [
    ("","", "Username is required"),
    ("standard_user","", "Password is required"),
    ("","secret_sauce", "Username is required"),
    ("standard_user","wrong", "Username and password do not match"),
    ("wrong", "wrong", "Username and password do not match"),
    ("wrong", "secret_sauce", "Username and password do not match"),
]

PROBLEM_USERS = [
    "problem_user",
    "error_user",
    "visual_user",
]

PERFORMANCE_USER = "performance_glitch_user"

LOCKED_USER = "locked_out_user"

INVALID_CHECKOUT = [
    ("","Test","00-001", "Error: First Name is required"),
    ("Jan","","00-001", "Error: Last Name is required"),
    ("Jan","Test","", "Error: Postal Code is required"),
    ("","","", "Error: First Name is required"),
]

VALID_CHECKOUT = ("Jan", "Test", "00-001")
