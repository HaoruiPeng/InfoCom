const animateCircle = function(circle) {
  let startTime = 0;
  const totalTime = 5000; // 1000ms = 1s
  circle.setAttributeNS(null, 'cx', circle_x);
  circle.setAttributeNS(null, 'cy', circle_y);
  var x_step = circle_x_dst - circle_x_src;
  var y_step = circle_y_dst - circle_y_src;
  const animateStep = (timestamp) => {
    if (!startTime) startTime = timestamp;
    // progress goes from 0 to 1 over 1s
    const progress = (timestamp - startTime) / totalTime;
    // move right 100 px
    circle.setAttributeNS(null, 'cx', circle_x_src + x_step*progress);
    circle.setAttributeNS(null, 'cy', circle_y_src + y_step*progress);
    if (progress < 1) {
      window.requestAnimationFrame(animateStep);
    }
  }
  window.requestAnimationFrame(animateStep);
};
