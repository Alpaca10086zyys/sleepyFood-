// document.addEventListener('DOMContentLoaded', () => {
//     const dishForm = document.getElementById('dishForm');
//     const dishName = document.getElementById('dishName');
//     const dishPrice = document.getElementById('dishPrice');
//     const dishList = document.getElementById('dishList');

//     dishForm.addEventListener('submit', function (event) {
//         event.preventDefault();
//         const newDish = {
//             name: dishName.value,
//             price: parseFloat(dishPrice.value)
//         };
//         addDish(newDish);
//     });

//     function addDish(dish) {
//         fetch('/add_dish', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(dish)
//         })
//             .then(response => response.json())
//             .then(data => {
//                 displayDish(data);
//                 dishName.value = '';
//                 dishPrice.value = '';
//             })
//             .catch(error => console.error('Error:', error));
//     }

//     function fetchDishes() {
//         fetch('/dishes')
//             .then(response => response.json())
//             .then(data => {
//                 data.forEach(dish => displayDish(dish));
//             })
//             .catch(error => console.error('Error:', error));
//     }

//     function displayDish(dish) {
//         const li = document.createElement('li');
//         li.textContent = `${dish.name} - ${dish.price}`;
//         dishList.appendChild(li);
//     }

//     fetchDishes();
// });

function showShop(shopId) {
    // 隐藏所有商店
    var shops = document.querySelectorAll('.shop');
    shops.forEach(function (shop) {
        shop.style.display = 'none';
    });

    // 显示特定商店
    var shopToShow = document.getElementById(shopId);
    if (shopToShow) {
        shopToShow.style.display = 'block';
    }
}

