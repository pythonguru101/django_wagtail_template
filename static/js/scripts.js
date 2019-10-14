$(document).ready(function(){

	$('.overlay-preload').fadeOut('fast');

	// Cookie Bar
	$.cookieBar({
		message:'We use cookies. To find out more click ',
		declineButton:false,
		policyButton:true,
		policyText: 'here',
		policyURL: '/cookies-and-privacy-policy/',
		fixed: true,
		bottom: true,
		zindex: '2000',
	});


	// collaborations header
	$('.change-on-hover').hover(function(){
		$this = $(this);
		$color = $this.data("color");
		$this.css("background-color", $color);
		$this.css("border-color", $color);
		$this.css("color", "#fff");
	}, function() {
		$this.css("background-color", "#fff");
		$this.css("border-color", "#000");
		$this.css("color", "#000");
	})

	// menu hover
	$('.menu--change-on-hover').hover(function(){
		$this = $(this);
		$color = $this.data("color");
		console.log($color)
		$this.css("color", $color);
	}, function() {
		$this.css("color", "#000");
	})

	// animate header
	$(function(){
		var shrinkHeader = 100;
			$(window).scroll(function() {
			var scroll = getCurrentScroll();
				if ( scroll >= shrinkHeader ) {
					$('.navigation').addClass('shrink');
				}
				else {
					$('.navigation').removeClass('shrink');
				}
			});
		function getCurrentScroll() {
			return window.pageYOffset || document.documentElement.scrollTop;
		}
	});

	// isotope layout
	var $grid = $('.fitrows').isotope({
		itemSelector: '.each-element',
		layoutMode: 'fitRows'
	});
	// layout Isotope after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.isotope('layout');
	});

	// show menu
	$('.menu_trigger a').click(function(){
		console.log('click')
		$('.menu-container').fadeIn('fast');
		if ($('body.homepage').length) {
			$('body').removeClass('homepage');
		} 
	});

	// hide menu
	$('.menu-container').click( function(e) {
		if (!$('body.homepage').length) {
			$('.menu-container').fadeOut('fast');
			e.stopPropagation();
		} 
	});

	// show product titles on overview
	$('.product-overview .each-product').hover(function(){
		$(this).find('.product-title').fadeIn('fast');
	}, function(){
		$(this).find('.product-title').fadeOut('fast');
	});

	// product slideshows
	if ($('.single-product .swiper-container').length) {
		$this = $(this);
		if ($this.find('.swiper-slide').length > 2) {
			var galleryThumbs = new Swiper('.gallery-thumbs', {
				slidesPerView: 4,
				freeMode: true,
				watchSlidesVisibility: true,
				watchSlidesProgress: true,
			});
			var mySwiper = new Swiper ('.swiper-container.gallery', {
				// Optional parameters
				direction: 'horizontal',
				loop: true,
				navigation: {
					nextEl: '.swipe-hover--right',
					prevEl: '.swipe-hover--left',
				},
				thumbs: {
					swiper: galleryThumbs
				}
			});
		}
	}

	$('.swiper-container.gallery-thumbs').each(function(){
		$this= $(this)
		$slides = $(this).find('.swiper-slide').length
		console.log($slides)
		if ($slides < 2) {
			$this.hide();
		}

	})

	$('.swipe-hover').hover(function(){
		$this = $(this);
		$arrow = $this.find('.arrow');
		$arrow.fadeIn('fast');
		}, function (){
		$arrow.fadeOut('fast');
	})


	// slideshow hover




	// make checkout form look tidy
	var name_address = $('.name-address')
	var height = name_address.outerHeight();
	var summary = $('.summary')
	if (height) {
		console.log(height)
		summary.css( "min-height", height + "px" );
	}

	// drop down basket on Amend page
	var amend_basket = $('body.amend-basket')
	if (amend_basket.length) {
		showCart()
	}


});


//Javascript function to perform currency formatting
function CommaFormatted(amount) {
  var delimiter = ","; // replace comma if desired
  var a = amount.split('.',2)
  var d = a[1];
  var i = parseInt(a[0]);
  if(isNaN(i)) { return ''; }
  var minus = '';
  if(i < 0) { minus = '-'; }
  i = Math.abs(i);
  var n = new String(i);
  var a = [];
  while(n.length > 3) {
    var nn = n.substr(n.length-3);
    a.unshift(nn);
    n = n.substr(0,n.length-3);
  }
  if(n.length > 0) { a.unshift(n); }
  n = a.join(delimiter);
  if(d.length < 1) { amount = n; }
  else { amount = n + '.' + d; }
  amount = minus + amount;

  return amount;
}
