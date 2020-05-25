import json

# Python program to convert a list
# to string using join() function
# Function to convert
def list_to_string(s):
    # initialize an empty string
    str1 = " "
    # return string
    return str1.join(s)


# Python code to demonstrate
# to convert dictionary into string
# using str()
def dict_to_string(d):
    result = json.dumps(d)
    return result


# Python3 code to demonstrate
# convert dictionary string to dictionary
# using json.loads()
def str_to_dict(string):
    result = json.loads(string)
    return result


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
