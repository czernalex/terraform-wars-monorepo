# from http import HTTPStatus

# from allauth.account.models import EmailAddress
# from model_bakery import baker

# from main.apps.core.utils import ApiClientTestCase
# from main.apps.users.models import User


# class AllAuthSignUpTestCase(ApiClientTestCase):
#     def test_signup(self):
#         email = "user@email.com"
#         response = self.client.post(
#             "/allauth-api/browser/v1/auth/signup",
#             content_type="application/json",
#             data={
#                 "email": "user@email.com",
#                 "password": "KnB2eHks9mte",
#             },
#         )
#         self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
#         user = User.objects.for_email(email).first()
#         self.assertIsNotNone(user)
#         self.assertFalse(user.is_active)
#         self.assertTrue(user.has_usable_password())

#     def test_signup_with_name(self):
#         email = "user@email.com"
#         response = self.client.post(
#             "/allauth-api/browser/v1/auth/signup",
#             content_type="application/json",
#             data={
#                 "email": "user@email.com",
#                 "first_name": "John",
#                 "last_name": "Doe",
#                 "password": "KnB2eHks9mte",
#             },
#         )
#         self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
#         user = User.objects.for_email(email).first()
#         self.assertIsNotNone(user)
#         self.assertFalse(user.is_active)
#         self.assertTrue(user.has_usable_password())
#         self.assertEqual("John", user.first_name)
#         self.assertEqual("Doe", user.last_name)

#     def test_signup_with_existing_user(self):
#         user = baker.make(User, email="user@email.com", is_active=True)
#         baker.make(EmailAddress, user=user, email=user.email, verified=True, primary=True)
#         response = self.client.post(
#             "/allauth-api/browser/v1/auth/signup",
#             content_type="application/json",
#             data={
#                 "email": user.email,
#                 "password": "KnB2eHks9mte",
#             },
#         )
#         self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

#     def test_signup_with_weak_password(self):
#         response = self.client.post(
#             "/allauth-api/browser/v1/auth/signup",
#             content_type="application/json",
#             data={
#                 "email": "user@email.com",
#                 "password": "password",
#             },
#         )
#         self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
