var my_api_key = 'ef83cac599a8b6b59be433cffe4aa715';
var movie_title= $('.movie_title').val();
$(function(){
const source = document.getElementById('movie_name');
  const inputHandler = function(e) {
    if(e.target.value==""){
      $('.button1').attr('disabled', true);
    }
    else{
      $('.button1').attr('disabled', false);
    }
  }
$('.button1').on('click',function(movie_title){
    $.ajax({
      type:'POST',
      url:"/predict",
      data:{'title':movie_title},
      contentType: "application/x-www-form-urlencoded",
      success: function(movie_title){
        search(movie_title)}
      });
    });
});
// 