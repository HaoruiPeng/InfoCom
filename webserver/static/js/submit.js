function submit() {
  var src_x = document.getElementById('src_x').value;
  var src_y = document.getElementById('src_y').value;
  var dst_x = document.getElementById('dst_x').value;
  var dst_y = document.getElementById('dst_y').value;
  var data = { "src_x": src_x,
               "src_y": src_y,
               "dst_x": dst_x,
               "dst_y": dst_y
             }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var resp = JSON.parse(this.responseText);
    circle_x_src = resp.src_x;
    circle_y_src = resp.src_y;
    circle_x_dst = resp.dst_x;
    circle_y_dst = resp.dst_y;
  }
};
xhttp.open("POST", "/submit", false);
xhttp.send(JSON.stringify(data));
};
