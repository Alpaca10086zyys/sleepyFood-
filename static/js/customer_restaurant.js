document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_all_merchants')
        .then(response => response.json())
        .then(shops => {
            const shopButtonsContainer = document.getElementById('shop-buttons-container');
            if (!shopButtonsContainer) {
                console.error('Container for shop buttons not found.');
                return;
            }
            shops.forEach(shop => {
                const button = document.createElement('button');
                button.textContent = shop.name;
                button.classList.add('shop-button');
                button.addEventListener('click', () => {
                    showShop(`shop${shop.id}_items`);
                });
                shopButtonsContainer.appendChild(button);
            });
        })
        .catch(error => console.error('Error fetching merchants:', error));
});

function showShop(shopId) {
    var shops = document.querySelectorAll('.shop');
    shops.forEach(function (shop) {
        shop.style.display = 'none';
    });
    var shopToShow = document.getElementById(shopId);
    if (shopToShow) {
        shopToShow.style.display = 'block';
    }
}
