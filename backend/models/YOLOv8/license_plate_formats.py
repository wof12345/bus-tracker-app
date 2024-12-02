import re


def is_valid_liicense_plate(text, countries=['USA']):
    valid = True

    for country in countries:
        if country == 'USA':
            if not us_license_plate(text):
                return False

    return valid


def us_license_plate(plate_text):
    # length check
    if not (5 <= len(plate_text) <= 8):
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
