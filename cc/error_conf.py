## Login ERROR MESSAGES

NO_INPUT_DATA = {
    "msg": "No data is provided in request",
    "error_code": 0
}
GENERIC_API_FALIURE = {
    "msg": "Server is not reponding at the moment. Please contact site Admin",
    "error_code": 0
}
EMAIL_NOT_PROVIDED = {
    "msg": "Please provide your email",
    "error_code": 1
}
PASSWORD_NOT_PROVIDED = {
    "msg": "Please provide your password",
    "error_code": 2
}
SOURCE_NOT_PROVIDED = {
    "msg": "Please specify specific input resource",
    "error_code": 3
}

INVALID_EMAIL = {
    "msg": "Please provide an valid email",
    "error_code": 4
}
INSUFFICIENT_PASSWORD_LENGTH = {
    "msg": "Password should be minimum 8 in length",
    "error_code": 5
}
USER_DOES_NOT_EXIST = {
    "msg": "User Does not exist",
    "error_code": 6
}
EMAIL_NOT_VERIFIED = {
    "msg": "Your email is not yet verified",
    "error_code": 7
}
USER_IS_INACTIVE = {
    "msg": "User account is inactive. Please contact Admin",
    "error_code": 8
}

INVALID_PASSWORD = {
    "msg": "UserName and Password does not match",
    "error_code": 9
}
USER_REGISTERED_THROUGH_SOCIAL_ACCOUNT = {
    "msg": "You registered through social account",
    "error_code": 10
}
##Login ERROR MESSAGES END

## Registration ERROR MESSAGES
CONFIRM_PASSWORD_NOT_PROVIDED = {
    "msg": "Please provide your confirm-password",
    "error_code": 101
}
USER_ALREADY_EXISTS_collegecampus = {
    "msg": "User account already exists please use forgot password to reset your password.",
    "error_code": 102
}
USER_ALREADY_EXISTS_SOCIAL = {
    "msg": "User account already exists with social registration.",
    "error_code": 103
}
INVALID_SOURCE_PROVIDED = {
    "msg": "Invalid source provided.",
    "error_code": 104
}
PASSWORDS_DOES_NOT_MATCH = {
    "msg": "Password and Confirm-Password does not match.",
    "error_code": 105
}

## Registration ERROR MESSAGES END

# Update Password
OLD_PASSWORD_NOT_PROVIDED = {
    "msg": "Old Password is required to update password",
    "error_code": 201
}
OLD_PASSWORD_INCORRECT = {
    "msg": "Old Password provided is incorrect",
    "error_code": 202
}
USER_CREATED_THROUGH_SOCIAL_LOGIN = {
    "msg": "Password can't be reset as user is created through social login",
    "error_code": 203
}
## Update Password

## Social - Registration ERROR MESSAGES
FULLNAME_NOT_PROVIDED = {
    "msg": "Please provide Full Name",
    "error_code": 204
}
ACCESS_TOKEN_NOT_PROVIDED = {
    "msg": "Please provide access token",
    "error_code": 205
}
PROVIDER_NOT_PROVIDED = {
    "msg": "Please provide provider name",
    "error_code": 206
}
PROVIDER_ID_NOT_PROVIDED = {
    "msg": "Please provide provide id",
    "error_code": 207
}
INVALID_INPUT_DATA = {
    "msg": "Invalid data is provided in request",
    "error_code": 208
}
USER_REGISTRATION_FAILED = {
    "msg": "Invalid data, User Registration Failed",
    "error_code": 209
}

##Social - Registration ERROR MESSAGES END


## Ticket Create ERROR MESSAGES END
NORMAL_USER_REQUIRED = {
    "msg": "Only Normal User can access this feature.",
    "error_code": 301
}
INVALID_INPUT_DATA = {
    "msg": "Invalid input data provided.",
    "error_code": 302
}
## Ticket Create ERROR MESSAGES END

## Ticket Patch ERROR MESSAGES END
UNAUTHORIZED_ACCESS = {
    "msg": "Unauthorized access",
    "error_code": 304
}

TICKET_NOT_FOUND = {
    "msg": "Ticket with provided id not found",
    "error_code": 305
}
TICKET_DESCRIPTION_FREEZED = {
    "msg": "Ticket's description can not be modified",
    "error_code": 306
}
AGENT_NOT_FOUND = {
    "msg": "Provided id is not relate to any Agent.",
    "error_code": 307
}
AGENT_ID_NOT_FOUND = {
    "msg": "Agent Id Not Found.",
    "error_code": 308
}
## Ticket Patch ERROR MESSAGES END

# Private Message Error Message
TICKET_NOT_PROVIDED = {
    "msg": "Please Provide Ticket ID to Post a Message",
    "error_code": 1001
}
TICKET_DOES_NOT_EXIST = {
    "msg": "Ticket with provided ID Does Not Exist",
    "error_code": 1002
}
AGENT_IS_NOT_ASSIGNED_YET = {
    "msg": "Agent is Not Assigned Yet",
    "error_code": 1003
}
CANNOT_POST_EMPTY_MESSAGE = {
    "msg": "Cannot Post an Empty Message",
    "error_code": 1004
}
MESSAGE_ON_TICKET_CLOSED = {
    "msg": "Messages can't be send on closed Ticket",
    "error_code": 1005
}
# Private Message Error Message

## Public Message Error Handling
COMMENT_WITH_NO_ATTACHMENT_DISCRIPTION = {
    "msg": "Cannot post with empty message or attachment",
    "error_code": 1006
}
## Public Message Error Handling


## Register Product Error
INDUSTRY_NOT_FOUND = {
    "msg": "Provided Industry not found.",
    "error_code": 1101
}
CATEGORY_NOT_FOUND = {
    "msg": "Provided Category not found.",
    "error_code": 1102
}
PRODUCT_NOT_FOUND = {
    "msg": "Provided Product not found.",
    "error_code": 1103
}
## Register Product Error Ends

REGISTER_PRODUCT_NOT_FOUND = {
    "msg": "Provided Registered Product not found.",
    "error_code": 1104
}


## Admin Login
ADMIN_NOT_FOUND = {
    "msg": "Only Admin can consume this API.",
    "error_code": 1105
}
ADMIN_REQUIRED = {
    "msg": "Only Admin can access this feature.",
    "error_code": 1106
}
AGENTS_ACCOUNT_DO_NOT_MATCH = {
    "msg": "Admin can Delete Agent Belonging to same Account.",
    "error_code": 1107
}

CATEGORY_NOT_PROVIDED = {
    "msg": "Categoris not provided.",
    "error_code": 1108
}

DURATION_NOT_PROVIDED = {
    "msg": "Duration not provided.",
    "error_code": 1109
}

SEARCH_STRING_NOT_FOUND = {
    "msg": "Search String not provided.",
    "error_code": 1110
}
