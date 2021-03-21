  document.getElementById("map").addEventListener("load", function() {
    var doc = this.getSVGDocument();
    var svg = doc.getElementById("map-svg");
    var circleNode = document.getElementById('redCircle');
    document.getElementById('init').addEventListener('click', function(){
      if(circleNode == null){
        circleNode = doc.createElementNS("http://www.w3.org/2000/svg", "circle");
        circleNode.setAttributeNS(null, 'cx', circle_x_src);
        circleNode.setAttributeNS(null, 'cy', circle_y_src);
        circleNode.setAttributeNS(null, 'r', '3');
        circleNode.setAttributeNS(null, 'fill', 'red');
        circleNode.setAttributeNS(null, 'id', 'redCircle');
        svg.appendChild(circleNode);
      }
      });
  });
