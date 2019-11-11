var title_place = "up";

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

$( window ).on( 'resize', function() { title_setup(); } );

$( window ).on( 'load', function() {
  setTimeout( function() { window.dispatchEvent( new Event( 'resize' ) ); },
              5000 );
} );

function title_setup()
{
  if ( $( ".page-title" ).height() > 0.8 * $( ".page-title" ).width() &&
       title_place == "up" ) {
    $( ".page-title" ).detach().appendTo( "#nav-bottom" );
    $( "#nav-bottom" ).css( 'display', 'flex' );
    title_place = "down";
  } else if ( 0.5 * ( $( window ).width() - $( ".nav-icons-right" ).width() -
                      $( ".nav-icons-left" ).width() ) >
                $( "#nav-top" ).height() + $( "#nav-bottom" ).height() &&
              title_place == "down" ) {
    $( ".page-title" ).insertAfter( ".nav-icons-left" );
    $( "#nav-bottom" ).hide();
    title_place = "up";
  }
}

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
      index : startsAtIndex, // start at first slide
      addCaptionHTMLFn : function( e, t ) {
        return e.title ? ( t.children[0].innerHTML   = e.title,
                           t.children[0].style.width = e.w * e.fitRatio + "px",
                           !0 )
                       : ( t.children[0].innerHTML = "", !1 )
      },
      timeToIdle : 2000,

      shareEl : false,

    };

    // Initializes and opens PhotoSwipe
    var gallery = new PhotoSwipe(
      pswpElement, PhotoSwipeUI_Default, window.djangoAlbumImages, options );
    gallery.init();
  }
}
