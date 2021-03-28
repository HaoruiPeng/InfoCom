function submit() {
  var src_addr = document.getElementById('src_addr').value;
  var dst_addr = document.getElementById('dst_addr').value;
  var data = { "src_addr": src_addr,
               "dst_addr": dst_addr,
             }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    try{
      var resp = JSON.parse(this.responseText);
      circle_x_src = resp.src_x;
      circle_y_src = resp.src_y;
      circle_x_dst = resp.dst_x;
      circle_y_dst = resp.dst_y;
      alert("Got addresses");
    }
    catch(err){
      alert(this.responseText);
    }
  }
};
xhttp.open("POST", "/submit", false);
xhttp.send(JSON.stringify(data));
};
