# Password Generator Using Python

## Project Overview

This mini project is a Python-based password generator designed to help users
create strong, secure, and customizable passwords. The project focuses on
improving online security by reducing the use of weak, predictable, or repeated
passwords.

Passwords protect personal, financial, academic, and professional accounts.
When users choose simple passwords or reuse the same password across multiple
websites, they increase the risk of unauthorized access. This project addresses
that problem by generating random passwords based on user-selected options such
as length, uppercase letters, lowercase letters, digits, and special characters.

## Problem Statement

Weak and predictable passwords are a common cause of security breaches. Many
users choose passwords that are easy to remember, but those passwords are often
easy for attackers to guess. At the same time, complex passwords can be hard to
create manually.

The goal of this project is to provide a simple tool that generates secure and
memorable passwords using customizable settings. The generator allows users to
choose password length and character types so they can create passwords suitable
for different websites, applications, and security requirements.

## Objectives

- Generate strong random passwords.
- Allow users to select the required password length.
- Support different character sets such as letters, digits, and punctuation.
- Reduce password reuse by making it easy to create new passwords.
- Improve protection for personal and professional accounts.
- Keep the tool simple enough to run from the command line.

## Tools And Technologies

- Python: Main programming language used for the project.
- `string`: Provides predefined character groups such as lowercase letters,
  uppercase letters, digits, and punctuation.
- `secrets`: Provides cryptographically secure random selection and is preferred
  for password generation.
- Command-line interface: Used to accept user input and display the generated
  password.

## Architecture

The project can be organized into four main parts:

1. User Input Layer

   This layer collects password requirements from the user. It asks for the
   desired password length and which character types should be included.

2. Character Set Builder

   This layer builds the pool of allowed characters. For example, if the user
   selects uppercase letters, lowercase letters, digits, and special characters,
   the program combines all of those character sets into one available pool.

3. Password Generation Logic

   This layer randomly selects characters from the allowed character pool. The
   selected characters are joined together to form the final password. The
   `secrets` module should be used here because it is better suited for security
   use cases than basic pseudo-random generators.

4. Output Layer

   This layer displays the generated password to the user. In a command-line
   version, the password is printed in the terminal.

## Working Principle

The password generator works by taking user-defined input, building a character
pool, and randomly selecting characters from that pool.

Basic flow:

1. Ask the user for the password length.
2. Ask which character types should be included.
3. Combine the selected character sets.
4. Validate that at least one character set was selected.
5. Generate the password using secure random choices.
6. Display the generated password.

## Implementation Details

A simple implementation can follow this structure:

```text
password-generator/
  README.md
  password_generator.py
```

Suggested logic for `password_generator.py`:

```python
import secrets
import string


def build_character_pool(include_uppercase, include_lowercase, include_digits, include_special):
    characters = ""

    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    return characters


def generate_password(length, characters):
    return "".join(secrets.choice(characters) for _ in range(length))
```

The final program should validate user input before generating the password. For
example, the password length should be a positive number, and the user should
select at least one character type. Without validation, the program may fail or
generate passwords that do not meet the user's security needs.

## Expected Input

- Password length.
- Whether to include uppercase letters.
- Whether to include lowercase letters.
- Whether to include numbers.
- Whether to include special characters.

## Expected Output

The program displays a randomly generated password based on the user's selected
options.

Example:

```text
Generated password: F7$dqP!2zL9@
```

## Challenges Faced

- Choosing a secure random generation method.
- Handling cases where the user excludes all character types.
- Making sure the password length is valid.
- Keeping the command-line interface simple and understandable.
- Balancing password strength with memorability.

## Future Enhancements

- Add a graphical user interface using Tkinter or PyQt.
- Add a password strength checker based on length and character diversity.
- Add an option to generate multiple passwords at once.
- Add secure encrypted password storage.
- Integrate with password manager tools.
- Add user profiles for different password rules and preferences.

## Conclusion

This Python password generator is a simple but useful security tool. It helps
users create stronger passwords with custom settings and supports better online
security habits. By using Python's standard libraries and secure random
generation, the project provides a practical introduction to password security,
input validation, and command-line application design.

## Repository Note

The current workspace also contains `sound.py` and `wp.py`, which appear to be
YOLO/OpenCV weapon-detection scripts. They do not currently match the password
generator project described in the PDF.
