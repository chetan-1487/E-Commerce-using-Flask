import random
import re

def generateOtp():
  return "otp"

def is_valid_username(username: str) -> bool:
   
   pattern = r"""
        ^(?=.*[A-Z])
        ^(?=.*[a-z])
        ^(?=.*\d)
    """

   return bool(re.match(pattern,username, re.VERBOSE))


def is_valid_password(password: str) -> bool:
    pattern = r"""
        ^
        (?=.*[a-z])            
        (?=.*[A-Z])             
        (?=.*\d)                
        (?=.*[@$!%*?&^#()_\-])  
        .{8,}
        $
    """
    return bool(re.match(pattern, password, re.VERBOSE))