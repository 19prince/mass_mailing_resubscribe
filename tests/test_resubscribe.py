from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestResubscribe(HttpCase):

    def _unsubscribe(self, mlist):
        contact = self.env["mailing.contact"].create({"name": "Reader", "email": "reader@example.com", "list_ids": [(4, mlist.id)]})
        mailing = self.env["mailing.mailing"].create({
            "subject": "Hi", "body_html": "<p>Hi</p>",
            "mailing_model_id": self.env.ref("mass_mailing.model_mailing_list").id,
            "contact_list_ids": [(6, 0, mlist.ids)],
        })
        url = mailing._get_unsubscribe_url(contact.email, contact.id).replace("/confirm_unsubscribe", "/unsubscribe")
        self.mailing = mailing
        return contact, self.url_open(url).text

    def test_button_offers_only_the_list_just_left(self):
        newsletter = self.env["mailing.list"].create({"name": "Newsletter", "is_public": True})
        contact, html = self._unsubscribe(newsletter)
        self.assertTrue(contact.subscription_ids.opt_out, "the link itself still unsubscribes")
        self.assertIn('id="o_mailing_resubscribe"', html)
        self.assertIn(f'data-list-ids="{newsletter.id}"', html)

    def test_no_button_for_private_list(self):
        private = self.env["mailing.list"].create({"name": "Internal", "is_public": False})
        _contact, html = self._unsubscribe(private)
        self.assertNotIn('id="o_mailing_resubscribe"', html)

    def test_resubscribe_route_opts_back_in(self):
        newsletter = self.env["mailing.list"].create({"name": "Newsletter", "is_public": True})
        contact, _html = self._unsubscribe(newsletter)
        self.assertTrue(contact.subscription_ids.opt_out)
        params = {"document_id": contact.id, "email": contact.email,
                  "hash_token": self.mailing._generate_mailing_recipient_token(contact.id, contact.email)}
        names = self.make_jsonrpc_request(f"/mailing/{self.mailing.id}/resubscribe", params)
        self.assertEqual(names, ["Newsletter"])
        contact.subscription_ids.invalidate_recordset()
        self.assertFalse(contact.subscription_ids.opt_out)

    def test_resubscribe_route_rejects_bad_token(self):
        newsletter = self.env["mailing.list"].create({"name": "Newsletter", "is_public": True})
        contact, _html = self._unsubscribe(newsletter)
        with self.assertRaises(Exception):
            self.make_jsonrpc_request(f"/mailing/{self.mailing.id}/resubscribe",
                                      {"document_id": contact.id, "email": contact.email, "hash_token": "nope"})
        self.assertTrue(contact.subscription_ids.opt_out)
