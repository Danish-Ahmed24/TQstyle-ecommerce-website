document.addEventListener('DOMContentLoaded', function () {
    initGallery();
    initAddToCart();
});

function initGallery() {
    const mainImage          = document.querySelector('#mainProductImage');
    const thumbnails         = document.querySelectorAll('.thumbnail-item');

    if (!thumbnails.length) return;

    const selectedPriceValue = document.querySelector('#selectedPriceValue');
    const stockStatus        = document.querySelector('#stockStatus');
    const addToCartButton    = document.querySelector('#addToCartButton');
    const orderWhatsappButton= document.querySelector('#orderWhatsappButton');
    const selectedVariantId  = document.querySelector('#selectedVariantId');
    const whatsappVariantId  = document.querySelector('#whatsappVariantId');
    const bubble             = stockStatus ? stockStatus.previousElementSibling : null;

    // Store original button HTML so we can restore it when back in-stock
    const addToCartOriginalHTML = addToCartButton ? addToCartButton.innerHTML : '';

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function () {
            const variantId = this.getAttribute('data-variant-id');
            const newSrc    = this.getAttribute('data-image');
            const price     = this.getAttribute('data-price');
            const stock     = parseInt(this.getAttribute('data-stock'), 10);

            // Gallery + price
            if (mainImage) {
                mainImage.style.opacity = '0.5';
                mainImage.setAttribute('src', newSrc);
                mainImage.onload = () => { mainImage.style.opacity = '1'; };
            }
            if (selectedPriceValue) selectedPriceValue.textContent = price;

            // Sync hidden form inputs
            if (selectedVariantId) selectedVariantId.value = variantId;
            if (whatsappVariantId)  whatsappVariantId.value  = variantId;

            // Stock UI + button state
            if (stock > 0) {
                if (stockStatus) {
                    stockStatus.textContent  = `In Stock (${stock} available)`;
                    stockStatus.className    = 'text-sm font-medium text-emerald-600';
                }
                if (bubble) {
                    bubble.className = 'inline-block w-2.5 h-2.5 rounded-full flex-shrink-0 bg-emerald-400 shadow-sm shadow-emerald-400/60 animate-pulse';
                }
                if (addToCartButton) {
                    addToCartButton.disabled = false;
                    addToCartButton.innerHTML = addToCartOriginalHTML;
                }
                if (orderWhatsappButton) orderWhatsappButton.disabled = false;
            } else {
                if (stockStatus) {
                    stockStatus.textContent  = 'Out of Stock';
                    stockStatus.className    = 'text-sm font-medium text-red-500';
                }
                if (bubble) {
                    bubble.className = 'inline-block w-2.5 h-2.5 rounded-full flex-shrink-0 bg-red-400';
                }
                if (addToCartButton) {
                    addToCartButton.disabled = true;
                    addToCartButton.innerHTML = 'Out of Stock';
                }
                if (orderWhatsappButton) orderWhatsappButton.disabled = true;
            }

            // Thumbnail ring highlight
            thumbnails.forEach(t => {
                t.classList.remove('ring-[#C8A165]', 'ring-2');
                t.classList.add('ring-[#E5DDD3]');
            });
            this.classList.remove('ring-[#E5DDD3]');
            this.classList.add('ring-[#C8A165]', 'ring-2');
        });
    });
}

function initAddToCart() {
    const form = document.getElementById('addToCartForm');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const btn = form.querySelector('#addToCartButton');
        const originalHTML = btn ? btn.innerHTML : '';

        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loading loading-spinner loading-sm"></span>';
        }

        try {
            const res = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            });
            const data = await res.json();
            if (data.success) {
                updateCartUI(data.cart_count, data.cart_total);
                showToast(data.message || 'Added to cart', 'success');
            } else {
                showToast(data.message || 'Could not add to cart', 'error');
            }
        } catch (err) {
            form.submit();
            return;
        }

        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
        }
    });
}
