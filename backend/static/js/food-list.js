/* food-list.js : 一覧/カードの共通クリック処理 */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-detail-url]').forEach(function (item) {
    item.addEventListener('click', function (event) {
      if (event.target.closest('button')) return;
      location.href = item.dataset.detailUrl;
    });
  });

  document.querySelectorAll('.favorite-toggle').forEach(function (button) {
    button.addEventListener('click', function () {
      button.classList.toggle('is-favorite');

      // お気に入り一覧では解除後に行ごと消す想定
      const favoriteItem = button.closest('.favorite-item');
      if (favoriteItem && !button.classList.contains('is-favorite')) {
        favoriteItem.remove();
      }
    });
  });
// ソート自動適用
  document.querySelectorAll('.small-add-button').forEach(function (button) {
    button.addEventListener('click', function () {
      // 後で sessionStorage か URLパラメータ経由で food_register.html に渡す
      const params = new URLSearchParams();
      params.set('name', button.dataset.foodName || '');
      params.set('category', button.dataset.category || '');
      location.href = '/foods/register/?' + params.toString();
    });
  });  
});
