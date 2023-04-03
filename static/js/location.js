

function runOnce(func) {// set this function to run only once
  let hasRun = false;
  return function() {
    if (!hasRun) {
      hasRun = true;
      func.apply(this, arguments);
    }
  }
}


const get_geo=function getPosition(){
 if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition(function(res){
   var lat = res.coords.latitude;
   var lon = res.coords.longitude;
   var coor = {lat:lat,lon:lon};
   var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
   $.ajax({
    url:"",
    type:"post",

    headers: { 'X-CSRFToken': csrftoken
    },
    data:{
        coor:JSON.stringify(coor),
    },
    success:function(){
        alert('Thanks for sharing your location!')
    }
    })
  },function(err){
   console.log("err",err)
  })
 }
}

window.onload = runOnce(get_geo);
