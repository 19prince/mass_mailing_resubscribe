{
    "name": "Mass Mailing: One-Click Resubscribe",
    "version": "18.0.1.0.0",
    "summary": "Adds a 'Clicked by mistake? Keep me subscribed' button to the unsubscribe page",
    "author": "19 Prince",
    "website": "https://19prince.com",
    "category": "Marketing/Email Marketing",
    "depends": ["mass_mailing"],
    "data": ["views/unsubscribe_templates.xml"],
    "assets": {
        "mass_mailing.mailing_assets": [
            "mass_mailing_resubscribe/static/src/js/resubscribe.js",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
