
# Enhanced Python Logging with Colorized Output and File Rotation

This Python code provides a robust and enhanced logging solution with colorized console output, emoji removal, special character replacement, and time-based file rotation. It leverages the `logging` module, `colorama`, and regular expressions for improved functionality.

## Features

*   **Colorized Console Output:** Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) are displayed in distinct colors for easy identification in the console.
*   **Emoji and Special Character Handling:** Emojis and certain special characters are removed or replaced from log messages to ensure compatibility and readability.
*   **Time-Based File Rotation:** Log files are rotated daily (at midnight) to prevent them from growing indefinitely.  A backup count is maintained, discarding the oldest logs when the limit is reached.
*   **Customizable Log Format:** The log message format, including timestamp and log level, can be easily customized.
*   **Clear Handler Management:** Ensures no duplicate handlers are attached, preventing redundant log entries.
*   **TTY Detection:** Color output is only enabled when running in a terminal (TTY), or can be forced via configuration.
*   **Safe Character Filtering:** Cleans up filenames for log files, replacing unsafe characters with underscores.

## Installation

1.  **Clone the repository (optional):** If you've downloaded the code as a zip, extract it. If it's in a git repo, clone it:

    ```bash
    git clone https://github.com/ByteScrape/logging.git  # Replace with your repo URL
    cd logging
    ```

2.  **Install dependencies:** This code requires `colorama`. Install it using pip:

    ```bash
    pip install colorama
    ```

## Usage

1.  **Import the `configure_logging` function:**

    ```python
    from your_module import configure_logging  # Replace your_module
    ```

2.  **Configure and get the logger:**

    ```python
    logger = configure_logging(name="my_app", path="my_logs", level=logging.INFO, save=True)
    ```

    *   `name`: The name of your logger (e.g., "my_app", "main").
    *   `path`: The directory where log files will be stored (e.g., "logs", "my_logs"). This directory will be created if it doesn't exist.
    *   `level`: The minimum logging level to capture (e.g., `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`).
    *   `save`: A boolean value that controls whether logs are saved to a file.  Set to `True` to enable file saving.

3.  **Use the logger:**

    ```python
	logger = configure_logging(name="my_app", path="my_logs", level=logging.INFO, save=True)
	
	logger.getLogger("my_app")
	
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    ```
