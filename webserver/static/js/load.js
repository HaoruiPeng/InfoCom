  // document.getElementById("map").addEventListener("load", function() {
  //   var doc = this.getSVGDocument();
  //   var svg = doc.getElementById("map-svg");
  //   var circleNode = document.getElementById('redCircle');
  //   document.getElementById('init').addEventListener('click', function(){
  //     if(circleNode == null){
  //       circleNode = doc.createElementNS("http://www.w3.org/2000/svg", "circle");
  //       circleNode.setAttributeNS(null, 'cx', circle_x_src);
  //       circleNode.setAttributeNS(null, 'cy', circle_y_src);
  //       circleNode.setAttributeNS(null, 'r', '3');
  //       circleNode.setAttributeNS(null, 'fill', 'red');
  //       circleNode.setAttributeNS(null, 'id', 'redCircle');
  //       svg.appendChild(circleNode);
  //     }
  //     else{
  //       circleNode.setAttributeNS(null, 'cx', circle_x_src);
  //       circleNode.setAttributeNS(null, 'cy', circle_y_src);
  //       circleNode.setAttributeNS(null, 'r', '3');
  //       circleNode.setAttributeNS(null, 'fill', 'red');
  //       circleNode.setAttributeNS(null, 'id', 'redCircle');
  //     }
  //     });
  // });


  document.getElementById("map").addEventListener("load", function() {
    var doc = this.getSVGDocument();
    var svg = doc.getElementById("map-svg");
    var circleNode = document.getElementById('myDrone');
    console.log(circle_x, circle_y);
    if(circleNode == null){
      circleNode = doc.createElementNS("http://www.w3.org/2000/svg", "circle");
      circleNode.setAttributeNS(null, 'cx', circle_x);
      circleNode.setAttributeNS(null, 'cy', circle_y);
      circleNode.setAttributeNS(null, 'r', '3');
      circleNode.setAttributeNS(null, 'fill', 'limegreen');
      circleNode.setAttributeNS(null, 'id', 'myDrone');
      svg.appendChild(circleNode);
    }
    else{
      circleNode.setAttributeNS(null, 'cx', circle_x);
      circleNode.setAttributeNS(null, 'cy', circle_y);
      circleNode.setAttributeNS(null, 'r', '3');
      circleNode.setAttributeNS(null, 'fill', 'limegreen');
      circleNode.setAttributeNS(null, 'id', 'myDrone');
    }
    // while (true) {
    //   if(status == "Activate"){
    //   console.log(circle_x, circle_y);
    //   circleNode.setAttributeNS(null, 'cx', circle_x);
    //   circleNode.setAttributeNS(null, 'cy', circle_y);
    //   circleNode.setAttributeNS(null, 'fill', 'red');
    //   }
    //   if(status == "Idle"){
    //     circleNode.setAttributeNS(null, 'fill', 'green');
    //   }
    // }
  });
