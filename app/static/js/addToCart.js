document.addEventListener('DOMContentLoaded', function() {
    
    const button = document.querySelector("#addToCartButton");
    button.addEventListener('click',(e) => {
        e.preventDefault();
        e.stopPropagation();
        const productId = button.dataset.productId;
        console.log('Adding product to cart:', productId);
        cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart.push(productId);
        localStorage.setItem('cart', JSON.stringify(cart));
        alert('Product added to cart!');
    })
});