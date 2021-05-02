document.getElementById("search").onclick = function () {
  document.getElementById("input-area").style.display = "none";
  document.getElementById("details").style.display = "none";
  document.getElementById("castfo").style.display = "none";
  document.getElementById("recos").style.display = "none";
  document.getElementById("senti").style.display = "none";
  document.getElementsByClassName("footer").display="none";
  document.getElementById("gif").style.display = "block";
  var name = document.getElementById("movie_name").value;
    x = x.concat(name);
    document.getElementById("movie_name").value=x;
  }