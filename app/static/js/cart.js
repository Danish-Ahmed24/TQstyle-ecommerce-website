/**
 * cart.js — AJAX cart interactions for the cart page.
 * All actions have SSR form fallback (no JS required for core functionality).
 */

document.addEventListener('DOMContentLoaded', () => {
    initQtyControls();
    initRemoveForms();
    initPlaceOrderSpinner();
});

function initQtyControls() {
    document.querySelectorAll('.qty-form').forEach(form => {
        const input = form.querySelector('.qty-input');
        const decBtn = form.querySelector('.qty-dec');
        const incBtn = form.querySelector('.qty-inc');

        decBtn?.addEventListener('click', () => {
            const next = Math.max(0, parseInt(input.value, 10) - 1);
            input.value = next;
            submitCartUpdate(form);
        });

        incBtn?.addEventListener('click', () => {
            const next = Math.min(99, parseInt(input.value, 10) + 1);
            input.value = next;
            submitCartUpdate(form);
        });

        // Allow direct input edits (blur triggers update)
        input.addEventListener('change', () => submitCartUpdate(form));
    });
}

function initRemoveForms() {
    document.querySelectorAll('.remove-form').forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();
            submitCartRemove(form);
        });
    });
}

function initPlaceOrderSpinner() {
    const form = document.getElementById('place-order-form');
    form?.addEventListener('submit', () => {
        const btn = form.querySelector('[type="submit"]');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loading loading-spinner loading-sm"></span> Placing order…';
        }
    });
}

async function submitCartUpdate(form) {
    setFormBusy(form, true);
    try {
        const res = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        const data = await res.json();
        handleCartResponse(data, form.closest('[data-cart-item]'));
    } catch {
        form.submit(); // SSR fallback
    } finally {
        setFormBusy(form, false);
    }
}

async function submitCartRemove(form) {
    setFormBusy(form, true);
    try {
        const res = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        const data = await res.json();
        handleCartResponse(data, form.closest('[data-cart-item]'));
    } catch {
        form.submit(); // SSR fallback
    }
}

function handleCartResponse(data, itemEl) {
    if (!data.success) return;

    if (data.removed) {
        itemEl?.remove();
    } else {
        const itemTotal = itemEl?.querySelector('[data-item-total]');
        if (itemTotal && data.item_total) {
            itemTotal.textContent = `Rs.${data.item_total}`;
        }
    }

    updateCartUI(data.cart_count, data.cart_total);

    if (data.cart_count === 0) {
        // Show empty state without a full reload
        const container = document.getElementById('cart-items-container');
        const summary = document.getElementById('cart-summary');
        const emptyState = document.getElementById('cart-empty-state');
        if (container) container.style.display = 'none';
        if (summary) summary.style.display = 'none';
        if (emptyState) emptyState.style.display = 'flex';
    }
}

function setFormBusy(form, busy) {
    form.querySelectorAll('button').forEach(btn => (btn.disabled = busy));
}
// updateCartUI is defined globally in base.html
