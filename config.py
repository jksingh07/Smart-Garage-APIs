import os

SECRET_KEY = "ASEREMOTECONTROLLERsmartgarage"
TOKEN_ALGO = "HS256"

DATA_ROOT = os.path.join(os.getcwd(), "db")
GARAGE_DB = os.path.join(DATA_ROOT, "garage_db.json")
LOGIN_DB = os.path.join(DATA_ROOT, "login_db.json")
CAR_DB   = os.path.join(DATA_ROOT, "car_db.json")
GUEST_DB = os.path.join(DATA_ROOT, "guest_db.json")
NOTIFY_DB = os.path.join(DATA_ROOT, "notify_db.json")

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

KEY_CAR_ID = "CarID"
KEY_MILAGE = "Milage"
KEY_LAST_UPDATE = "LastestUpdate"
KEY_LAST_SERVICE_DATE = "LSDate"
KEY_LAST_SERVICE_MILAGE = "LSMilage"
KEY_OIL_TYPE = "OilType"
KEY_TYERS = "Tiers"
KEY_AIR_FILTER = "AirFilter"
KEY_BRAKE_OIL = "BrakeOil"


KEY_GUEST_CONJUSCTION = "+ASE#"
KEY_HEALTH = "Health"
KEY_COMPONENT = "Component"

KEY_LIGHT_ID = ["Light_Ext", "Light_L", "Light_M", "Light_R"]
KEY_DOOR_STAT = ["OPEN", "CLOSE", "STOP"]
