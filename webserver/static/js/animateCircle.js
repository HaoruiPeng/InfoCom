const animateCircle = function(circle) {
  let startTime = 0;
  const totalTime = 3000; // 1000ms = 1s
  circle.setAttributeNS(null, 'cx', circle_x_src);
  circle.setAttributeNS(null, 'cy', circle_y_src);
  var x_step = (circle_x_dst - circle_x_src)/totalTime;
  var y_step = (circle_y_dst - circle_y_src)/totalTime;
  const animateStep = (timestamp) => {
    if (!startTime) startTime = timestamp;
    // progress goes from 0 to 1 over 1s
    const progress = (timestamp - startTime) / totalTime;
    // move right 100 px
    var x = parseFloat(circle.getAttributeNS(null, 'cx'));
    var y = parseFloat(circle.getAttributeNS(null, 'cy'));
    console.log(x);
    circle.setAttributeNS(null, 'cx', x+ x_step);
    circle.setAttributeNS(null, 'cy', y+ y_step);
    if (progress < 1) {
      window.requestAnimationFrame(animateStep);
    }
  }
  window.requestAnimationFrame(animateStep);
};
