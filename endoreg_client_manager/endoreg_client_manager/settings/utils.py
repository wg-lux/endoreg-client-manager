import os

# Function to convert environment variable string to a list of extensions
def env_var_to_list(env_var):
    """
    Converts a comma-separated environment variable string to a list of extensions.

    Parameters:
    env_var (str): The environment variable containing the file extensions.

    Returns:
    list: A list of file extensions.
    """
    # Use os.getenv to safely get the environment variable value, defaulting to an empty string if not found
    extensions_str = os.getenv(env_var, "")
    # Split the string by commas into a list, strip spaces
    extensions_list = [ext.strip() for ext in extensions_str.split(",") if ext]
    return extensions_list

# Function to create a glob expression from a list of extensions
def create_glob_expression(extensions_list):
    """
    Creates a glob expression to match files of the specified extensions.

    Parameters:
    extensions_list (list): A list of file extensions.

    Returns:
    str: A glob expression string.
    """
    # Join the extensions with the OR operator '|' and wrap them in curly braces for glob's format
    return ["*." + ext for ext in extensions_list]


