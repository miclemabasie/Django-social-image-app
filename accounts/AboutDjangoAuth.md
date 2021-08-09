LoginView:
    -> Handles a login form and logs in a user

LogoutView:
    -> Logs out a user

PasswordChangeView:
    -> Handles a form to change the user's password

PasswordChangeDoneView:
    -> The success view that the user is redirected to after a successful password change

PasswordResetView:
    -> Allows Users to reset their passwords. It generates a one-time-use linkwith a token and sends it to a user's email account.

PasswordResetDoneView:
    -> Tells users that an email - including a link to their password has been sent to them

PasswordResetConfirmView:
    -> Allows Users to set a new password

PasswordResetCompleteView:
    -> The success view that user is redirected to after successfully resetting their password
