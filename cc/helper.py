from random import randint

import requests
from django.conf import settings

# from core.models import OTPGenerator
from oauth.models import BaseUser
# from user_details.models import UserSocialDetails

OTP_LENGTH = settings.OTP_LENGTH


###############################################################################
# Function to generate OTP, delete OTP and Verify OTP.
###############################################################################
def generate_otp_number():
    range_start = 10 ** (OTP_LENGTH - 1)
    range_end = (10 ** OTP_LENGTH) - 1
    return randint(range_start, range_end)


def delete_otp(verification_data):
    otp_number = verification_data['otp_number']
    if verification_data.get('phone_number'):
        phone_number = verification_data['phone_number']
        otp_obj = OTPGenerator.objects.filter(**{
            'otp_number': otp_number,
            'phone_number': phone_number
        })
    else:
        email = verification_data.get('email')
        otp_obj = OTPGenerator.objects.filter(**{
            'otp_number': otp_number,
            'email': email
        })
    [obj.delete() for obj in otp_obj]


def validate_otp_number(otp_no, otp_data):
    otp_obj = OTPGenerator.objects.filter(**{
        'otp_number': otp_no})
    if otp_obj.count() == 0:
        return otp_no
    else:
        otp_no = generate_otp_number()
        validate_otp_number(otp_no, otp_data)


###############################################################################
# Function to validate OTP
###############################################################################
def get_validate_password(password, confirm_password):
    """
    Password Rules Followed.
    a) Password should have a minimum length of 8
    b) Password must contains one Numeric Character
    c) Password must contain one alpha character
    """

    min_length = 8
    if password == confirm_password:

        # check if password length is greater than 8
        # check for digit in password
        # check for letters in password
        if len(password) >= min_length:
            # if any(char.isdigit() for char in password) \
            #         and any(char.isalpha() for char in password):
            #     return True
            # else:
            #     return False
            return True
    return False


###############################################################################
# Functions to revoke Oauth tokens
###############################################################################
def revoke_current_token(request):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'token': request.META['HTTP_AUTHORIZATION'][7:],
               'token_type_hint': 'access_token',
               'client_id': client_id,
               'client_secret': client_secret}

    host = request.get_host()
    return requests.post(
        settings.SERVER_PROTOCOLS + host + "/o/revoke_token/",
        data=payload,
        headers=headers)


###############################################################################
# Functions to generate Oauth tokens
###############################################################################
def generate_oauth_token(self, username, password):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'client_id': client_id,
               'client_secret': client_secret}

    host = self.request.get_host()
    return (requests.post(
            settings.SERVER_PROTOCOLS + host + "/o/token/",
            data=payload,
            headers=headers))


###############################################################################
# Functions to generate oAuth2 token from ReFresh tokens
###############################################################################
def generate_refresh_token(self):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    refresh_token = str(self.request.data.get('refresh_token'))

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    payload = {'grant_type': 'refresh_token', 'client_id': client_id,
               'client_secret': client_secret,
               'token type': 'Bearer', 'refresh_token': refresh_token}

    host = self.request.get_host()
    return (requests.post(
            settings.SERVER_PROTOCOLS + host + "/o/token/",
            data=payload,
            headers=headers))


###############################################################################
# Functions to Add Agent Details
###############################################################################
# def add_social_details(user, provider, provider_id):
#     """
#     Add Social Detail For Newly Created User
#     """
#     usersocialdetails = UserSocialDetails(
#         user=user,
#         email=user.email,
#         provider='collegecampus',
#         provider_id=user.id,
#         is_primary=True
#     )
#     usersocialdetails.save()


###############################################################################
# Function will generate chat text to export
###############################################################################
def export_ticket_chat(ticket_messages, ticket_id):
    """
    This function saves all the private chat of a ticket
    into a text file with name as its id.
    """

    export_chat = []
    deletd_status = ""
    for message in ticket_messages:
        if message.from_user_delete or message.to_user_delete:
            deletd_status = "(Deleted)"
        export_chat.append(deletd_status + ' ' +
                           str(message.created_at.strftime("%Y-%m-%d %H:%M"))
                           + " " + str(message.sender) + " : " +
                           message.message_text.encode('ascii', 'ignore') + " \n ")
    ticket_chat = "".join(export_chat)

    with open(settings.BASE_DIR + "/private_messages/private-message/" +
              str(ticket_id) + ".txt", "w+") as text_file:
        text_file.write(ticket_chat)

    return True


###############################################################################
# Function will generate chat text to export
###############################################################################
def export_ticket_comments(ticket_messages, ticket_id):
    """
    This function saves all the private chat of a ticket
    into a text file with name as its id.
    """

    export_chat = []
    deletd_status = ""
    for message in ticket_messages:
        if message.is_active:
            deletd_status = "(Deleted)"
        export_chat.append(deletd_status + ' ' +
                           str(message.date.strftime("%Y-%m-%d %H:%M"))
                           + " " + str(message.user) + " : " +
                           message.comment_text.encode('ascii', 'ignore') + " \n ")
    ticket_chat = "".join(export_chat)

    with open(settings.BASE_DIR + "/knowledgebase/public-message/" +
              str(ticket_id) + ".txt", "w+") as text_file:
        text_file.write(ticket_chat)

    return True


###############################################################################
# Function gets ticket based on similarity count
###############################################################################
# def get_ticket_by_similarity_count(tickets, search_query,
#                                    search_query_list,
#                                    similarity_threshold=settings.DEFAULT_SIMILARITY_THRESHOLD):
#     data_sort = {}
#     for ticket in tickets:
#         similarity_count = nlp_helper.cosine_sim(
#             search_query, " ".join(ticket.tags.split(',')))
#         ticket_word_list = ticket.tags.split(',')
#         query_list_len = len(search_query_list)
#         ticket_word_list_len = len(ticket_word_list)
#         if query_list_len:
#             coun = (ticket_word_list_len * similarity_count) / \
#                 query_list_len
#             if similarity_count > similarity_threshold or coun > 0.9:
#                 data_sort[ticket] = similarity_count
#             sorted(data_sort, key=data_sort.get, reverse=True)
#     return data_sort.keys()


###############################################################################
# Function extracts account category product list
###############################################################################
# def extract_account_category_product_list(account_list=None,
#                                           category_list=None,
#                                           product_list=None, kwargs=None):
#     if account_list:
#         account_list = [Account.objects.get(
#             name__iexact=account_name) for account_name in account_list]
#         kwargs['account_affiliated__in'] = [
#             account.id for account in account_list]
#
#     if category_list:
#         category_list = [Category.objects.get(
#             name__iexact=category_name) for category_name in category_list]
#         kwargs['category__in'] = [
#             category.id for category in category_list]
#
#     if product_list:
#         product_list = [Product.objects.get(name__iexact=product_name)
#                         for product_name in product_list]
#         kwargs['product__in'] = [product.id for product in product_list]
#
#     return kwargs


###############################################################################
# Function will generate search result
###############################################################################
# def search_ticket(request, search_query=None, source=None,
#                   ticket=None,
#                   similarity_threshold=settings.DEFAULT_SIMILARITY_THRESHOLD):
#     """
#     This function retives all the ticket based on the
#     searched keyworkds.
#     """
#     kwargs = {}
#     kwargs['is_active'] = True
#     kwargs['is_incident'] = True
#
#     if request.user.role == User.UserTypes.AGENT.value and \
#             request.user.agent:
#         kwargs['account'] = request.user.agent.account
#     if source == "autosuggest":
#         kwargs['ticket_status'] = Ticket.TicketStatus.CLOSED.value
#
#     # If the request is coming for similar incident then
#     # do not generate category_list etc for the same
#     if source != "similar_incident":
#         search_query_list = search_query.split(' ')
#         account_list, category_list, product_list = \
#             nlp_helper.account_category_product_extractor(search_query_list)
#         kwargs = extract_account_category_product_list(account_list,
#                                                        category_list,
#                                                        product_list, kwargs)
#     else:
#         kwargs['product'] = ticket.product.all()
#         kwargs['category'] = ticket.category.all()
#         kwargs['account_affiliated'] = ticket.account_affiliated.all()
#         if ticket.tags:
#             search_query = " ".join(ticket.tags.split(','))
#             search_query_list = ticket.tags.split(',')
#         else:
#             search_query = ""
#             search_query_list = ""
#
#     kwargs['heat_index__gte'] = settings.MIN_HEAT_INDEX_VALUE_FOR_SEARCH
#     # tickets = Ticket.objects.filter(**kwargs)
#     #
#     # if ticket:
#     #     tickets = tickets.exclude(id=int(ticket.id))
#     #
#     # # If the request is coming for recommended tab
#     # # do not perform similarity check.
#     # if source == "recommendation_tab":
#     #     return tickets
#     #
#     # if search_query.isdigit():
#     #     result = []
#     #     result = tickets.filter(incident_number=int(search_query))
#     # else:
#     #     # Calling the similarity count of tickets
#     #     result = get_ticket_by_similarity_count(tickets, search_query,
#     #                                             search_query_list,
#     #                                             similarity_threshold=similarity_threshold)
#     return result


###############################################################################
# Function will format the data accordingly for chart
###############################################################################
def get_chart_format(data=None):
    result_data = []
    counter = -1

    for entity in data:

        counter += 1
        if counter == 0:
            agent_name = {"v": "Top Agent"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v":0}

        elif counter == 1:
            agent_name = {"v": "You"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v":1}

        else:
            agent_name = {"v": "Average"}
            agent_average_score = {
                "v": int(entity.get('average_heat_index', 0)) if entity.get('average_heat_index') else 0}
            agent_color = {"v":2}

        agent_total_ticket_count = {
            "v": entity.get('total_count', 0) if entity.get('total_count') else 0}

        agent_performance = {
            "c": [agent_name, agent_total_ticket_count,
                  agent_average_score, agent_color]}
        result_data.append(agent_performance)
    return result_data


###############################################################################
# Function will format the data accordingly for Support Rating chart
###############################################################################
def get_support_rating_chart_format(data=None):
    result_data = []

    for entity in data:
        product_name = {"v": entity.get('product_name', "")}
        product_id = {"id": entity.get('product_id', "")}
        product_total_ticket_count = {
            "v": entity.get('total_count', 0) if entity.get('total_count') else 0}
        product_total_score = {
            "v": entity.get('support_rating', 0) if entity.get('support_rating') else 0}
        colour = {'v': entity.get('colour', 0) if entity.get('colour') else 0}
        support_rating = {
            'c': [product_name, product_total_ticket_count,
                  product_total_score, colour, product_id]
        }
        result_data.append(support_rating)
    return result_data


###############################################################################
# Function will get xaxis and yaxis data for representing graph
###############################################################################
def get_xaxis_yaxis_data(xaxis_data=0, yaxis_data=0):
    if xaxis_data:
        xaxis_data += (xaxis_data * 25) / 100
    else:
        xaxis_data = 0
    if yaxis_data:
        yaxis_data += (yaxis_data * 25) / 100
    else:
        yaxis_data = 0
    return (xaxis_data, yaxis_data)
