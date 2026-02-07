document.addEventListener('DOMContentLoaded', function() {
    // gallery
    mainImage = document.querySelector('#mainProductImage');   
    thumbnails = document.querySelectorAll('.thumbnail-item');
    selectedPriceValue = document.querySelector('#selectedPriceValue');
    stockStatus = document.querySelector('#stockStatus');
    addToCartButton = document.querySelector('#addToCartButton');
    orderWhatsappButton = document.querySelector('#orderWhatsappButton');
    // Find the bubble (it's the previous sibling of stockStatus)
    const bubble = stockStatus.previousElementSibling;
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const newSrc = this.getAttribute('data-image');
            const price = this.getAttribute('data-price');
            const stock = parseInt(this.getAttribute('data-stock'));
            
            // Update image and price
            mainImage.setAttribute('src', newSrc);
            selectedPriceValue.textContent = price;
            
            // Update stock status
            if (stock > 0) {
                stockStatus.textContent = `In Stock (${stock} available)`;
                bubble.className = 'w-3 h-3 rounded-full bg-green-500 animate-pulse shadow-lg shadow-green-500';

                addToCartButton.disabled = false;
                orderWhatsappButton.disabled = false;
            } else {
                stockStatus.textContent = 'Out of Stock';
                bubble.className = 'w-3 h-3 rounded-full bg-red-500';
                addToCartButton.disabled = true;
                orderWhatsappButton.disabled = true;
            }   
        });
    });
});