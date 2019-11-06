$( document ).ready( function() {
  $( ".sidenav" ).sidenav( {
    onCloseStart : function() {
      $( '.fa-times' ).addClass( 'fa-bars' ).removeClass( 'fa-times' );
    },

    onOpenStart : function() {
      $( '.fa-bars' ).addClass( 'fa-times' ).removeClass( 'fa-bars' );
    }
  } );

  $( "#sidenav-toggle" ).click( function() {
    var elem     = $( '.sidenav' );
    var instance = M.Sidenav.getInstance( elem );
    if ( instance.isOpen ) {
      $( '.sidenav' ).sidenav( 'close' );
    } else {
      $( '.sidenav' ).sidenav( 'open' );
    }
  } );

  $( '.tooltipped' ).tooltip();
} );

$( window )
  .on( 'resize',
       function() {
         if ( window.innerWidth <= 600 ) {
           if ( $( ".page-title" ).parent( '#nav-top' ).length ) {
             $( ".page-title" ).detach().appendTo( "#nav-bottom" );
           }
         } else {
           if ( $( ".page-title" ).parent( '#nav-bottom' ).length ) {
             $( ".page-title" ).insertAfter( ".nav-icons-left" );
           }
         }
       } )
  .trigger( 'resize' );

// Initializes PhotoSwipe.
var pswpInit = function( startsAtIndex ) {
  if ( !startsAtIndex ) { startsAtIndex = 0; }

  var pswpElement = document.querySelectorAll( '.pswp' )[0];

  // commented the array bellow since the images array will be loaded from the
  // server in variable called djangoAlbumImages.

  // build items array
  // var items = [
  //    {
  //        src: 'https://placekitten.com/600/400',
  //        w: 600,
  //        h: 400
  //    },
  //    {
  //        src: 'https://placekitten.com/1200/900',
  //        w: 1200,
  //        h: 900
  //    }
  //];

  // find is images are loaded from the server.
  if ( window.djangoAlbumImages && window.djangoAlbumImages.length > 0 ) {
    // define options (if needed)
    var options = {
      // optionName: 'option value'
      // for example:
      index : startsAtIndex // start at first slide
    };

    // Initializes and opens PhotoSwipe
    var gallery = new PhotoSwipe(
      pswpElement, PhotoSwipeUI_Default, window.djangoAlbumImages, options );
    gallery.init();
  }
}
