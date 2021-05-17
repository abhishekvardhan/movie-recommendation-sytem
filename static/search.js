document.getElementById("search").onclick = function () {
  var name = document.getElementById("movie_name").value;
  x = x.concat(name);
  document.getElementById("movie_name").value = x;
  var dat = document.getElementById("Link").innerHTML;
  if (dat == 'Search By') {
    alert('dat');
    document.getElementById('result1').innerHTML = '*Please Select An Option';
  }
  else {
    document.getElementById("frm").submit();
  }
  document.getElementById("input-area").style.display = "none";
  document.getElementById("details").style.display = "none";
  document.getElementById("castfo").style.display = "none";
  document.getElementById("recos").style.display = "none";
  document.getElementById("senti").style.display = "none";
  document.getElementsByClassName("footer").style.display = "none";
  document.getElementById("gif").style.display = "block";

}