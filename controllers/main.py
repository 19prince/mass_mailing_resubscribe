from werkzeug.exceptions import NotFound, Unauthorized

from odoo import http
from odoo.addons.mass_mailing.controllers.main import MassMailController


class MassMailResubscribe(MassMailController):

    @http.route('/mailing/<int:mailing_id>/resubscribe', type='json', auth='public', website=True)
    def mailing_resubscribe(self, mailing_id, document_id=None, email=None, hash_token=None):
        """Undo an unsubscribe: opt back in to the mailing's own public lists.
        Same token check as Odoo's unsubscribe link, so only the recipient can call it."""
        email_found, hash_token_found = self._fetch_user_information(email, hash_token)
        try:
            mailing_sudo = self._check_mailing_email_token(
                mailing_id, document_id, email_found, hash_token_found, required_mailing_id=True)
        except NotFound as e:
            raise Unauthorized() from e
        lists = mailing_sudo.contact_list_ids.filtered('is_public')
        lists._update_subscription_from_email(email_found, opt_out=False)
        return lists.mapped('name')
