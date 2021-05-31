function login() {
  var username = document.getElementById('login-serialnumber').value;
  var password = document.getElementById('login-password').value;
  var data = { "login-serialnumber": username,
               "login-password": password,
             }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    try{
      document.write(xmlhttp.responseText);
    }
    catch(err){
      alert(this.responseText);
    }
  }
};
xhttp.open("POST", "/login", false);
xhttp.send(JSON.stringify(data));
};
