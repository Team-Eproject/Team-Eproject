/* common-ui.js : jQuery UI 部品の初期化 */
$(function () {
  $('.selectmenu').selectmenu({
    width: false,
    change: function () {
      // バックエンド実装後、ここでクエリ送信や画面更新に接続する
      // 例: location.search = new URLSearchParams(new FormData(this.form)).toString();
    }
  });

  $('#expiry-date').datepicker({
    dateFormat: 'yy年mm月dd日',
    monthNames: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
    dayNamesMin: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
    showMonthAfterYear: false,
    changeMonth: true,
    changeYear: true
  });
});
