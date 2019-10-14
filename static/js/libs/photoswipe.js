$(document).ready(function(){
    var mouseUsed = false;
        $('body').on('mousedown', '.pswp__scroll-wrap', function(event) {
        // On mousedown, temporarily remove the transition class in preparation for swipe.
            $(this).children('.pswp__container_transition').removeClass('pswp__container_transition');
        }).on('mousedown', '.pswp__button--arrow--left, .pswp__button--arrow--right', function(event) {
        // Exlude navigation arrows from the above event.
        event.stopPropagation();
    })
});


(function($) {
    var $pswp = $('.pswp')[0];
    var image = [];

    $('.isotope-elements').each( function() {
        var $pic     = $(this),
            getItems = function() {
                var items = [];
                $pic.find('.drawing').each(function() {
                    var $href   = $(this).attr('href'),
                        $size   = $(this).data('size').split('x'),
                        $width  = $size[0],
                        $height = $size[1],
                        $title = $(this).data('title');

                    var item = {
                        src : $href,
                        w   : $width,
                        h   : $height,
                        title: $title
                    }

                    items.push(item);
                    
                });
                console.log(items);
                return items;

            }

        var items = getItems();
        
        $.each(items, function(index, value) {
            image[index]     = new Image();
            image[index].src = value['src'];
        });

        $pic.on('click', 'figure', function(event) {
            event.preventDefault();
            
            var $index = $( "figure" ).index( this );
            console.log($index);
            var options = {
               
                index: $index,
                bgOpacity: 1,
                showHideOpacity: true,
                barsSize: {top:120, bottom:80}
                
                
            }
            var lightBox = new PhotoSwipe($pswp, PhotoSwipeUI_Default, items, options);
            lightBox.init();
               // Transition Manager function (triggers only on mouseUsed)
            function transitionManager() {
                // Create var to store slide index
                var currentSlide = options.index;
                // Listen for photoswipe change event to re-apply transition class
                lightBox.listen('beforeChange', function() {
                // Only apply transition class if difference between last and next slide is < 2
                // If difference > 1, it means we are at the loop seam.
                    var transition = Math.abs(lightBox.getCurrentIndex()-currentSlide) < 2;
                    // Apply transition class depending on above
                    $('.pswp__container').toggleClass('pswp__container_transition', transition);
                    // Update currentSlide
                    currentSlide = lightBox.getCurrentIndex();
              });
            }

            lightBox.listen('mouseUsed', function(){
                mouseUsed = true;
                transitionManager();
            });
        });
    });
})(jQuery);

(function($) {
    var $pswp = $('.pswp')[0];
    var image = [];

    $('.framed-images').each( function() {
        var $pic     = $(this),
            getItems = function() {
                var items = [];
                $pic.find('.frame-detail').each(function() {
                    var $href   = $(this).attr('href'),
                        $size   = $(this).data('size').split('x'),
                        $width  = $size[0],
                        $height = $size[1],
                        $title = $(this).data('caption');

                    var item = {
                        src : $href,
                        w   : $width,
                        h   : $height,
                        title: $title
                    }

                    items.push(item);
                    
                });
                console.log(items);
                return items;

            }

        var items = getItems();
        
        $.each(items, function(index, value) {
            image[index]     = new Image();
            image[index].src = value['src'];
        });

        $pic.on('click', 'figure', function(event) {
            event.preventDefault();
            
            var $index = $( "figure" ).index( this );
            console.log($index);
            var options = {
               
                index: $index,
                bgOpacity: 1,
                showHideOpacity: true,
                barsSize: {top:120, bottom:80}
                
                
            }
            var lightBox = new PhotoSwipe($pswp, PhotoSwipeUI_Default, items, options);
            lightBox.init();
               // Transition Manager function (triggers only on mouseUsed)
            function transitionManager() {
                // Create var to store slide index
                var currentSlide = options.index;
                // Listen for photoswipe change event to re-apply transition class
                lightBox.listen('beforeChange', function() {
                // Only apply transition class if difference between last and next slide is < 2
                // If difference > 1, it means we are at the loop seam.
                    var transition = Math.abs(lightBox.getCurrentIndex()-currentSlide) < 2;
                    // Apply transition class depending on above
                    $('.pswp__container').toggleClass('pswp__container_transition', transition);
                    // Update currentSlide
                    currentSlide = lightBox.getCurrentIndex();
              });
            }

            lightBox.listen('mouseUsed', function(){
                mouseUsed = true;
                transitionManager();
            });
        });
    });
})(jQuery);
