/* food-register.js : 食品登録フォームの数量操作・Datepicker設定 */
document.addEventListener('DOMContentLoaded', function () {
  const quantityInput = document.getElementById('quantity-input');
  const increaseButton = document.getElementById('increase-quantity');
  const decreaseButton = document.getElementById('decrease-quantity');

  if (quantityInput && increaseButton && decreaseButton) {
    increaseButton.addEventListener('click', function () {
      quantityInput.value = Number(quantityInput.value || 1) + 1;
    });

    decreaseButton.addEventListener('click', function () {
      const nextValue = Number(quantityInput.value || 1) - 1;
      quantityInput.value = nextValue < 1 ? 1 : nextValue;
    });
  }

  /* Datepicker設定 日本語化とデータ形式*/
  if (window.jQuery && $('#expiry-date').length) {
  $('#expiry-date').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true,
    changeMonth: true,
    monthNames: [
      '1月', '2月', '3月', '4月', '5月', '6月',
      '7月', '8月', '9月', '10月', '11月', '12月'
    ],
    monthNamesShort: [
      '1月', '2月', '3月', '4月', '5月', '6月',
      '7月', '8月', '9月', '10月', '11月', '12月'
    ],
    dayNamesMin: ['日', '月', '火', '水', '木', '金', '土']
    });
  }
});