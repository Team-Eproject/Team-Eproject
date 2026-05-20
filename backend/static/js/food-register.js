/* food-register.js : 食品登録フォームの数量操作 */
document.addEventListener('DOMContentLoaded', function () {
  const quantityInput = document.getElementById('quantity-input');
  const increaseButton = document.getElementById('increase-quantity');
  const decreaseButton = document.getElementById('decrease-quantity');

  if (!quantityInput || !increaseButton || !decreaseButton) return;

  increaseButton.addEventListener('click', function () {
    quantityInput.value = Number(quantityInput.value || 1) + 1;
  });

  decreaseButton.addEventListener('click', function () {
    const nextValue = Number(quantityInput.value || 1) - 1;
    quantityInput.value = nextValue < 1 ? 1 : nextValue;
  });
});
