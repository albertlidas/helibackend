def jwt_response_payload_handler(token, user=None, request=None):
    try:
        return {
            'token': token,
            'username': str(user.username),
            'email': str(user.email),
            'lastname': str(user.regularuser.lastname),
            'phone': str(user.regularuser.phone),
        }
    except:
        return {
            'token': token,
            'username': str(user.username),
            'email': str(user.email),
            'country': str(user.helipadowner.country),
            'city': str(user.helipadowner.city),
            'address': str(user.helipadowner.address),
            'phone': str(user.helipadowner.phone),
            'contact_name': str(user.helipadowner.contact_name),
        }

