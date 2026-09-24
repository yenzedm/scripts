#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets
import string
import sys


# Characters chosen to be safe in bash/cmd/powershell:
# excludes ! (history expansion), [ ] (globbing), and $ ` " ' \ (escaping/substitution)
SAFE_SYMBOLS = "@#%^&*-_=+?~"


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def ask_length() -> int:
    while True:
        raw = input("Password length: ").strip()
        try:
            n = int(raw)
        except ValueError:
            print("Please enter an integer.")
            continue
        if n < 4:
            print("Too short - minimum is 4.")
            continue
        if n > 256:
            print("Too long - maximum is 256.")
            continue
        return n


def build_alphabet(lower: bool, upper: bool, digits: bool, symbols: bool) -> str:
    alphabet = ""
    if lower:
        alphabet += string.ascii_lowercase
    if upper:
        alphabet += string.ascii_uppercase
    if digits:
        alphabet += string.digits
    if symbols:
        alphabet += SAFE_SYMBOLS
    return alphabet


def generate_password(length: int, alphabet: str, required_groups: list[str]) -> str:
    # Ensure each selected group appears at least once
    password_chars: list[str] = []
    for group in required_groups:
        password_chars.append(secrets.choice(group))

    # Fill the rest with random characters from the combined alphabet
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(alphabet))

    # Cryptographically secure shuffle
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def main() -> None:
    print("=== Password Generator ===")
    print(f"Safe symbols: {SAFE_SYMBOLS}\n")

    length = ask_length()
    use_lower = ask_yes_no("Include lowercase letters (a-z)?")
    use_upper = ask_yes_no("Include uppercase letters (A-Z)?")
    use_digits = ask_yes_no("Include digits (0-9)?")
    use_symbols = ask_yes_no(f"Include symbols ({SAFE_SYMBOLS})?")

    groups: list[str] = []
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append(SAFE_SYMBOLS)

    if not groups:
        print("No character groups selected. Exiting.", file=sys.stderr)
        sys.exit(1)

    if length < len(groups):
        print(
            f"Length {length} is too small to include all selected groups "
            f"({len(groups)} groups). Increase the length.",
            file=sys.stderr,
        )
        sys.exit(1)

    alphabet = "".join(groups)

    while True:
        password = generate_password(length, alphabet, groups)
        print(f"\nGenerated password: {password}")
        if not ask_yes_no("Generate another one?"):
            print("Done.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted.")
        sys.exit(0)
