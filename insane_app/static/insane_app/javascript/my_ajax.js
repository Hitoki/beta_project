$('#like').click(function(){
  var storyid;
  storyid = $(this).attr("data-storyid");
  jQuery.get('/insane/'+storyid+'/like/', {}, function(created){
    if(created==1){
      $('#like_count').html(parseInt($('#like_count').html())+1);
      $('#like')[0].classList.add('fas');
      $('#like')[0].classList.remove('far');
    }
    else{
      $('#like_count').html(parseInt($('#like_count').html())-1);
      $('#like')[0].classList.add('far');
      $('#like')[0].classList.remove('fas');
  }
  });
});
