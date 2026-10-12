/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

const btnHtml = (id, label, cls) => `<button type="button" id="${id}" class="btn ${cls} ms-2">${label}</button>`;

// Page 1, "Are you sure you want to unsubscribe?": stay without changing anything.
function initConfirmPage() {
    const form = document.querySelector('form[action="/mailing/confirm_unsubscribe"]');
    if (!form) {
        return;
    }
    form.querySelector('button[type="submit"]').insertAdjacentHTML("afterend", btnHtml("o_mailing_stay", "Stay on the list", "btn-outline-primary"));
    document.getElementById("o_mailing_stay").addEventListener("click", () => {
        document.getElementById("info_state").innerHTML = "<p class='mb-0 text-center'><strong>You're still subscribed.</strong></p>";
    });
}

// Page 2, "Successfully unsubscribed!": one click back onto the list just left.
function initDonePage() {
    const manage = document.querySelector('#info_state a[href*="/unsubscribe?"]');
    if (!manage) {
        return;
    }
    manage.insertAdjacentHTML("afterend", btnHtml("o_mailing_resubscribe_done", "Resubscribe", "btn-outline-primary"));
    document.getElementById("o_mailing_resubscribe_done").addEventListener("click", async (ev) => {
        ev.target.disabled = true;
        const url = new URL(manage.href);
        const msg = document.querySelector("#info_state p");
        try {
            const names = await rpc(`/mailing/${url.pathname.split("/")[2]}/resubscribe`, {
                document_id: url.searchParams.get("document_id"),
                email: url.searchParams.get("email"),
                hash_token: url.searchParams.get("hash_token"),
            });
            msg.textContent = names.length ? `You're back on ${names.join(", ")}.` : "You're subscribed again.";
            ev.target.remove();
        } catch {
            msg.textContent = "Something went wrong. Use Manage Subscriptions to rejoin.";
            ev.target.disabled = false;
        }
    });
}

// Page 3, subscription management: re-tick the lists this mailing removed and submit Odoo's own form.
document.addEventListener("click", (ev) => {
    const btn = ev.target.closest("#o_mailing_resubscribe");
    if (!btn) {
        return;
    }
    for (const id of btn.dataset.listIds.split(",")) {
        const box = document.querySelector(`#o_mailing_subscription_form_lists input[value="${id}"]`);
        if (box) {
            box.checked = true;
        }
    }
    document.getElementById("button_form_send")?.click();
    const info = document.getElementById("o_mailing_subscription_info");
    info.querySelector("h1").textContent = "You're still subscribed";
    info.querySelector(":scope > span")?.classList.add("d-none"); // "You are no longer part of..."
    document.getElementById("o_mailing_subscription_feedback")?.classList.add("d-none");
    btn.closest("#o_mailing_resubscribe_wrap").innerHTML = "<p class='mb-0'>Thanks for sticking around.</p>";
});

const init = () => { initConfirmPage(); initDonePage(); };
document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
