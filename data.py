class Config:
    BASE_URL = "https://stellarburgers.nomoreparties.site"


class Endpoints:
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    USER = "/api/auth/user"
    ORDERS = "/api/orders"
    INGREDIENTS = "/api/ingredients"


class ErrorMessages:
    MISSING_INGREDIENT_IDS = "Ingredient ids must be provided"
    USER_ALREADY_EXISTS = "User already exists"
    MISSING_REQUIRED_FIELDS = "Email, password and name are required fields"
    UNAUTHORIZED_ACCESS = "You should be authorised"
    INVALID_CREDENTIALS = "email or password are incorrect"