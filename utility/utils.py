import re

def checkadmin(user):
    if user.find("sakthicomputers.com") != -1:
        return False
    else:  
        return True