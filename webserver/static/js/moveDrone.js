document.getElementById("map").addEventListener("load", function() {
  var doc = this.getSVGDocument();
  document.getElementById('start').addEventListener('click', function(){
    try {
      var circle = doc.getElementById("redCircle");
      animateCircle(circle);
    }
    catch(err) {
      alert("No Drone found!");
    }
 });
});
