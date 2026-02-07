document.addEventListener('DOMContentLoaded', function() {
    const checkoutButton = document.querySelector("#checkOut");
    
    if (checkoutButton) {
        checkoutButton.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const cart = JSON.parse(localStorage.getItem('cart')) || [];
            
            if (cart.length === 0) {
                alert('Your cart is empty!');
                return;
            }
            
            // Build WhatsApp message
            let message = "Hello! I want to place an order:\n\n";
            
            cart.forEach((item, index) => {
                message += `${index + 1}. Product ID: ${item}\n`;
                message += `   Quantity: 1\n\n`;
            });
            
            message += "Please confirm the order details and total price.";
            
            // Replace with your business WhatsApp number (including country code, no + or -)
            const whatsappNumber = "923193555402"; // Change this to your number
            
            // Encode message for URL
            const encodedMessage = encodeURIComponent(message);
            
            // Open WhatsApp
            const whatsappURL = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
            window.open(whatsappURL, '_blank');
            
            // Optional: Clear cart after opening WhatsApp
            // localStorage.removeItem('cart');
        });
    }
});