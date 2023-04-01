window.onload = function () {
  //get user's location
  getPosition();
}
function getPosition(){
 if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition(function(res){
   var lat = res.coords.latitude;
   var lon = res.coords.longitude;
   // send two float values to the backend using a POST request
    $.ajax({
      url: '/',
      type: 'POST',
      data: {
        value1: lat,
        value2: lon
      },
      success: function(response) {
        console.log('Success:', response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
  },function(err){
   console.log("err",err)
  })
 }
}



