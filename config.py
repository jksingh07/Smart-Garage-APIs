import os

SECRET_KEY = "ASEREMOTECONTROLLERsmartgarage"
TOKEN_ALGO = "HS256"

DATA_ROOT = os.path.join(os.getcwd(), "db")
GARAGE_DB = os.path.join(DATA_ROOT, "garage_db.json")
LOGIN_DB = os.path.join(DATA_ROOT, "login_db.json")

KEY_LIGHT = "Light"
KEY_DOOR = "Door"
KEY_CO = "Co"
KEY_COMMAND = "Command"
KEY_VALID = "Valid"
KEY_TOKEN = "token"
KEY_VALUE = "Value"
KEY_DEVICE = "Device"

KEY_EMAIL = "email"
KEY_PASSWORD = "password"
KEY_FIRST_N = "first_name"
KEY_LAST_N = "last_name"
KEY_ROLE = "role"


KEY_LIGHT_ID = ["Light_Ext", "Light_L", "Light_M", "Light_R"]
KEY_DOOR_STAT = ["OPEN", "CLOSE", "STOP"]
