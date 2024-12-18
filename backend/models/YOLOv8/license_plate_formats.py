import re


def is_valid_liicense_plate(text, countries=['USA']):
    valid = False

    for country in countries:
        if country == 'USA':
            if us_license_plate(text):
                return True
        elif country == 'Bangladesh':
            if bengali_license_plate(text):
                return True

    return valid


def us_license_plate(plate_text):
    # length check
    if not (5 <= len(plate_text)):
        return False

    # alphanumeric check
    if not re.match(r'^[A-Z0-9]+$', plate_text, re.IGNORECASE):
        return False

    # common format patterns
    if not re.match(
        r'^[A-Z]{1,3}\d{1,4}$|^\d{1,4}[A-Z]{1,3}$|^\d[A-Z]{1,3}\d{1,3}$', plate_text
    ):
        return False

    # avoid patterns with the same character repeated (like 'AAAAAA' or '111111')
    if re.match(r'^(.)\1+$', plate_text):
        return False

    return True


def bengali_license_plate(plate_text):
    # length check
    if not (4 <= len(plate_text) <= 10):
        return False

    # Bengali characters and digits check
    if not re.match(r'^[\u0980-\u09FF\u09E6-\u09EF\s-]+$', plate_text):
        return False

    # common format patterns for Bengali plates
    # Example: "\u09A1-12345" or "\u09A1 \u09A8 1234"
    if not re.match(
        r'^([\u0980-\u09FF]+[-\s]?[\u09E6-\u09EF]+)|([\u09E6-\u09EF]+[-\s]?[\u0980-\u09FF]+)$',
        plate_text,
    ):
        return False

    return True
