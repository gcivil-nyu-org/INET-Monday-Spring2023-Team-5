window.onload = function () {
  //get user's location
  getPosition();
}
function getPosition(){
 if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition(function(res){
   console.log("res",res)
  },function(err){
   console.log("err",err)
  })
 }
}

