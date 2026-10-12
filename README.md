# Mass Mailing Resubscribe

Gives people who unsubscribe by mistake an easy way back onto your Odoo mailing list.

Branches: `18.0`, `19.0`, `20.0`.

## What it adds

Odoo's unsubscribe flow has three pages. This module adds one button to each:

1. **"Are you sure you want to unsubscribe?"** → **Stay on the list.** Nothing changes; the page says "You're still subscribed."
2. **"Successfully unsubscribed!"** → **Resubscribe.** Puts the reader back on the list(s) that email removed them from and says "You're back on Newsletter."
3. **Mailing Subscriptions** (the manage page) → **Keep me subscribed**, under "Successfully Unsubscribed". Same effect, using Odoo's own subscription form.

Only the lists the email was sent to are restored, never lists the reader left earlier. Only lists marked **Show In Preferences** are offered.

## Security

The Resubscribe route (`/mailing/<id>/resubscribe`) uses the same signed token as Odoo's unsubscribe link, so a reader can only change their own subscription.

## Choosing which lists readers see

Odoo's manage page offers every public list under "You may also be interested in." To hide a list from it, open Email Marketing → Mailing Lists → the list, and untick **Show In Preferences**. No code needed.

## Notes

- Unsubscribe links only work on mailings that have a mailing list attached. A Marketing Automation email sent to contacts with no list attached shows "unsubscribed" but changes nothing (standard Odoo behavior), so attach the list.
- Re-opting someone in after they unsubscribe should only ever be their own action. This module doesn't send any "come back" emails.

## Tests

```
odoo-bin -d <db> -i mass_mailing_resubscribe --test-tags /mass_mailing_resubscribe --stop-after-init
```

License: LGPL-3. Built by [19 Prince](https://www.19prince.com).
