
function reatToPost(id,like) {
    $.ajax({
        url: "/"+id+"/view",
        data: {
              id: id,
              like: like
        },
        type: "POST",
      })
     .done(function() {
       console.log('done')
      })
     .fail(function( xhr, status, errorThrown ) {
        alert( "Sorry, there was a problem!" );
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
     })
   }

$(document).ready(function() {
  console.log('started')
  $('#likebutton').click(function(event){
    let but = $(this);
    let postId = but.attr('data-post-id')
    if (but.attr('value').match('like')) {
      console.log('liking');
      $('#count').text(function(i,orig) {
        return (parseInt(orig) + 1).toString()
      })
      reatToPost(postId,true);
    } else {
      console.log('unliking');
      $('#count').text(function(i,orig) {
        return (parseInt(orig) - 1).toString()
      })
      reatToPost(postId,false);
    }
  });
})
