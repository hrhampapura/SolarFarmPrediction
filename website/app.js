function onClickedClassify() {
  console.log("Classify Site button clicked");
  var lat = document.getElementById("uilat");
  var lon = document.getElementById("uilon");
  var model = document.getElementById("uimodel");
  var classified = document.getElementById("uiclassifysite");

  var url = "http://127.0.0.1:5000/classify_solar_site";

  $.post(url, {
      lat: parseFloat(lat.value),
      lat: parseFloat(lon.value),
      model:model.value
  },function(data, status) {
      console.log(data.solar_site_classification);
      classified.innerHTML = "<h2>" + data.solar_site_classification.toString() + "</h2>";
      console.log(status);
  });
}