"""
totp.py

Created on 2020-10-14
Updated on 2020-10-15

Copyright Ryan Kan 2020

Description: Handles the generation of the Time-based One Time Passwords (TOTPs)
"""

# IMPORTS
import binascii
import hashlib
import hmac
import time


# FUNCTIONS
def pad_left(string, length, padding_character):
    """
    Pads the left of `string` using the `padding_character` so as to make the final string have a length of `length`.

    Args:
        string (str):               The string that needs padding.
        length (int):               The length of the final string.
        padding_character (str):    The character that will be used to pad the left of the string.

    Returns:
        str:    The padded string.
    """

    return string.rjust(length, padding_character)


def base32_to_hexadecimal(base32):
    """
    Converts a base32 string to a hexadecimal string.

    Args:
        base32 (str): The base32 string.

    Returns:
        str: The hexadecimal string.
    """

    base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

    bits = ""
    for i in range(len(base32)):
        val = base32chars.index(base32[i].upper())
        bits += pad_left(bin(val)[2:], 5, "0")

    hexadecimal = ""
    for i in range(0, len(bits) - 3, 4):
        chunk = bits[i:i + 4]
        hexadecimal += hex(int(chunk, 2))[2:]

    return hexadecimal


def generate_otp(secret, epoch=int(time.time()), interval=30):
    """
    Generates a time-based one time password (TOTP).

    Args:
        secret (str):   The secret key that will be used to keep the OTPs secure.
                        The secret must be in base32, and its length must be a multiple of 8.

        epoch (int):    The current unix time.
                        (Default = int(time.time()))

        interval (int): How long the current OTP will be valid for, in seconds.
                        (Default = 30)

    Returns:
        str:    The TOTP.
    """

    try:
        curr_time = pad_left(hex(epoch // interval)[2:], 16, "0")

        hmac_obj = hmac.new(binascii.unhexlify(base32_to_hexadecimal(secret)), curr_time.encode("utf-8"), hashlib.sha1)
        hmac_str = hmac_obj.hexdigest()

        offset = int(hmac_str[-1], 16)

        otp = str(int(hmac_str[offset * 2: offset * 2 + 8], 16) & (2 ** 31 - 1))
        otp = otp[len(otp) - 6:len(otp)]

    except Exception as e:
        raise e

    return otp


def verify_otp(given_otp, secret, interval=5, time_window=1):
    """
    Verifies a given OTP.

    Args:
        given_otp (str):    The OTP to be checked and verified.

        secret (str):       The secret key that will be used to keep the OTPs secure.
                            The secret must be in base32, and its length must be a multiple of 8.

        interval (int):     How long the current OTP will be valid for, in seconds.
                            (Default = 30)

        time_window (int):  To prevent "on-the-edge" OTP submissions, this parameter defines how many intervals to
                            fully check the OTP. For example, for `time_window = 1`, the OTPs 30 seconds before and
                            after will be checked to see if any of them matches the provided OTP.
                            (Default = 1)

    Returns:
        bool:   Whether or not the OTP is valid. (True = Valid; False = Invalid)
    """

    current_epoch = int(time.time())

    valid_set_of_otp = []
    for epoch in range(current_epoch - time_window * interval, current_epoch + time_window * interval + 1):
        valid_set_of_otp.append(generate_otp(secret, epoch=epoch, interval=interval))

    if given_otp in valid_set_of_otp:
        return True
    else:
        return False


# DEBUG CODE
if __name__ == "__main__":
    print(generate_otp("TESTABLE", interval=10))
    print("The OTP is", "valid" if verify_otp(input("Enter the OTP: "), "TESTABLE", interval=10) else "invalid")
