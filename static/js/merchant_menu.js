document.getElementById('add-food-button').addEventListener('click', function() {
    let foodName = prompt('请输入菜品名称');
    if (!foodName) return;  // 如果未输入名称，直接返回

    let foodPrice = prompt('请输入菜品价格');
    if (!foodPrice) return;  // 如果未输入价格，直接返回

    let newButton = document.createElement('button');
    newButton.textContent = foodName;
    newButton.onclick = function() {
        displayFoodDetails(foodName, foodPrice);
    };

    let addButton = document.getElementById('add-food-button');
    addButton.parentNode.insertBefore(newButton, addButton);
});

function displayFoodDetails(name, price) {
    let foodInfoContainer = document.querySelector('.food-information');
    foodInfoContainer.innerHTML = `
        <h2>菜品信息</h2>
        <div class="food">
            <ul>
                <li>菜品名称: ${name}</li>
                <li>菜品价格: ${price}</li>
            </ul>
        </div>
    `;
}

function showFood(foodId) {
    let allFoods = document.querySelectorAll('.food-information .food');
    allFoods.forEach(food => food.style.display = 'none');
    document.getElementById(`${foodId}-info`).style.display = 'block';
}