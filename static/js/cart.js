/*
 * This file contains the methods for the cart
 *
 */


function initShippingAddress() {
	if ($('#id_use_for_shipping').is(':checked')) {
		$('#shipping-address').slideUp(function() {
		});
	} else {
		$('#shipping-address').slideDown();
	}
}

function showShippingAddressChange() {
	if ($('#id_use_for_shipping').is(':checked')) {
		$('#shipping-address').slideUp(function() {
			setShippingData(true);
		});
	} else {
		setShippingData(false);
	}
}

function setShippingData(as_billing) {
	if (as_billing) {
		//Set the shipping fields
		$('#id_shipping_firstname').val($('#id_firstname').val());
		$('#id_shipping_lastname').val($('#id_lastname').val());
		$('#id_shipping_street').val($('#id_street').val());
		$('#id_shipping_city').val($('#id_city').val());
		$('#id_shipping_state').val($('#id_state').val());
		$('#id_shipping_address_country').val($('#id_address_country').val());
		$('#id_shipping_zip').val($('#id_zip').val());
	} else {
		//Reset the shipping fields
		$('#id_shipping_firstname').val('');
		$('#id_shipping_lastname').val('');
		$('#id_shipping_street').val('');
		$('#id_shipping_street0').val('');
		$('#id_shipping_street1').val('');
		$('#id_shipping_street2').val('');
		$('#id_shipping_city').val('');
		$('#id_shipping_state').val('');
		$('#id_shipping_address_country').val('');
		$('#id_shipping_zip').val('');

    $('#shipping-address').slideDown();
	}
}

function onCheckoutSubmit() {
	copyAddress();
	copyShippingAddress();

	if ($('#id_use_for_shipping').is(':checked')) {
		setShippingData(true);
	}
}

function copyAddress() {
	var street = $('#id_street0').val();

	var street1 = $('#id_street1').val();
	if (street1 != '') street += ' ' + street1;

	var street2 = $('#id_street2').val();
	if (street2 != '') street += ' ' + street2;

	$('#id_street').val(street);
}

function copyShippingAddress() {
	var street = $('#id_shipping_street0').val();

	var street1 = $('#id_shipping_street1').val();
	if (street1 != '') street += ' ' + street1;

	var street2 = $('#id_shipping_street2').val();
	if (street2 != '') street += ' ' + street2;

	$('#id_shipping_street').val(street);
}

function cartAppear(){
	$('html, body').animate( { scrollTop: 0 }, 'fast', function () {
		$("#basket").fadeIn('slow');
	});
}

function appendToCart(p_cart_item){	
	$("#basket").load("/home/append/", p_cart_item, function() {
		initShippingCosts();
		$("#widget").load("/home/status/", function () {
		  cartAppear();
		});
	});
}

function continueShopping(){
    $("#basket").fadeOut(200, function(){
    	$(".basket-underlay").fadeOut(200, function () {
    	    // $('.basket-container').css('margin-top', '0px');
    	    // $('.home-content').css('position', 'absolute');
    	});
    });
    $("#menu__basket").load("/home/status/");
}

function initShippingCosts() {
	//Update shipping costs
	var shipping_method_id = $('select#shipping option:selected').val();
	var shipping_costs = parseFloat($('input#' + shipping_method_id + '_shipping_cost').val());
	// var cart_items = parseFloat($('input#cart_num_items').val());
	// if (cart_items < 3) {
	//   shipping_costs = shipping_costs;
	// } else {
	//   shipping_costs = shipping_costs + ((cart_items - 1) * (shipping_costs / 3));
	// }
	var total = shipping_costs + parseFloat($('#home-subtotal').text().replace(",", ""));
	$('#shipping-total').text(shipping_costs.toFixed(2));
	$('#home-total').text('£' + CommaFormatted(total.toFixed(2)));
}

function updateShippingCosts(p_select){
	var shipping_method_id = $(p_select).val();
	var shipping_costs = parseFloat($('input#' + shipping_method_id + '_shipping_cost').val());
	// var cart_items = parseFloat($('input#cart_num_items').val());
	// if (cart_items < 3) {
	//   shipping_costs = shipping_costs;
	// } else {
	//   shipping_costs = shipping_costs + ((cart_items - 1) * (shipping_costs / 3));
	// }
	var total = shipping_costs + parseFloat($('#home-subtotal').text().replace(",", ""));
	$('#shipping-total').text(shipping_costs.toFixed(2));
	$('#home-total').text('£' + CommaFormatted(total.toFixed(2)));
	$.post("/home/shipping_method/", {
		id: shipping_method_id
	});
}

function updateShippingCosts2(shipping_method_id) {
    var s = $('input#' + shipping_method_id + '_shipping_cost').val();
    var shipping_costs = 0.0;
    if (s && s.length) {
      shipping_costs = parseFloat(s);
    }
    var subtotal = parseFloat($('#home-subtotal').text().replace(",", ""));

		var total = shipping_costs + subtotal;

    $('#shipping-total').text(shipping_costs.toFixed(2));
		$('#home-total').text(CommaFormatted(total.toFixed(2)));

    $.post("/home/shipping_method/", {id: shipping_method_id});
}

function updateCountyCode() {
	if ($("#id_use_for_shipping").length) {
		var countryCode;
		if ($("#id_use_for_shipping").is(':checked')) {
			$("#checkout__shipping_address").slideUp('fast');
			countryCode = $("#id_address_country").val();
		} else {
			$("#checkout__shipping_address").slideDown('fast');
			countryCode = $("#id_shipping_address_country").val();
		}

		$.post("/home/shipping_method2/", {"country_code": countryCode}, function (resp) {
				updateShippingCosts2(resp.shipping_method_id);
				check_valid_order();
			}, "json"
		);
	} else {
		check_valid_order();
	}
}

function removeFromCart(p_cart_item) {
	$("#basket").load("/home/remove/", p_cart_item, function () {
    	// initShippingCosts();
		$("#widget").load("/home/status/");
		if($("#basket-subtotal-col3").text() == "" || $("#basket-subtotal-col3").text() == null){
			$("#basket").hide();
		}
  	});
}

function update_cart(pk_cart_item, cart_item_attribute_id, quantity) {
	var data = {"items": $.JSON.encode([{"pk": pk_cart_item, "attribute_id": cart_item_attribute_id, "quantity": quantity}])};
	$("#basket").load("/home/update/", data, function () {
		// initShippingCosts();
		$("#widget").load("/home/status/");
	});
}

function cart_item_minus(pk_cart_item, cart_item_attribute_id, quantity) {
	var q = parseInt(quantity);
	q -= 1;
	if (q > 0) {
		update_cart(pk_cart_item, cart_item_attribute_id, q);
	}
}

function cart_item_plus(pk_cart_item, cart_item_attribute_id, quantity) {
	var q = parseInt(quantity);
	q += 1;
	if (q > 0) {
		update_cart(pk_cart_item, cart_item_attribute_id, q);
	}
}

function select_product_minus(product_pk, base_price){
	var $product_count = $("#selected-product-count");
	var org_count = parseInt($product_count.val());
  var $price = $(".home-content__totalprice");

	if (org_count > 1) {
		$product_count.val(org_count - 1);
		$price.text(parseInt(org_count - 1) * parseFloat(base_price));
		$("#menu__basket").load("/home/partial_update/", {"pk_cart_item": product_pk, "quantity": org_count - 1});
	}
}

function select_product_plus(product_pk, base_price){
	var $product_count = $("#selected-product-count");
	var org_count = parseInt($product_count.val());
    var $price = $(".home-content__totalprice");

	$product_count.val(org_count+1);
	$price.text(parseInt(org_count+1) * parseFloat(base_price));
	$("#menu__basket").load("/home/partial_update/", {"pk_cart_item": product_pk, "quantity": org_count+1});
}

$('.select-country').on('change', function() {
    updateCountyCode();
});

$("#id_use_for_shipping").on('change', function(){
    updateCountyCode();
});

function cartCheckout(){
	var shipping_method_id = $('select#shipping option:selected').val();
	if (shipping_method_id > 0){
	    continueShopping();
		//window.location = "/home/checkout/";
	} else {
		$('.calculate').addClass('red');
		$('.shipping-choose').fadeIn();
	}
}

function shippingCheck(){
	$('select#shipping').change(function(){
	var shipping_method_id = $('select#shipping option:selected').val();
	if (shipping_method_id > 0) {
		$('.calculate').removeClass('red');
		$('.shipping-choose').fadeOut();
		$('.checkout-button').addClass('ok');
		$('.not-ready').fadeOut(function(){
			$('.ready').fadeIn();
		});
		} else {
		$('.calculate').addClass('red');
		$('.shipping-choose').fadeIn();
		$('.checkout-button').removeClass('ok');
		$('.ready').fadeOut(function(){
			$('.not-ready').fadeIn();
		});
		}
	});
}

function showCart(){
	// ADDED : hide basket button //
	$("#basket").load("/home/index/", function() {
		var shipping_method_id = $('select#shipping option:selected').val();

		if (shipping_method_id > 0) {
			$('.checkout-button').addClass('ok');
			$('.ready').show();
		} else {
			$('.not-ready').show();
		}
		initShippingCosts();
		shippingCheck();
		cartAppear();
	});
}

//new_add

function initCheckoutForm() {
	$('#id_promotion').keyup(checkPromotionalCode);
	$('#id_promotion').change(checkPromotionalCode);

	$('input#id_vat_number').keyup(function() {
		var vat_number = $('input#id_vat_number').val();
		if (vat_number.length >= 5) {
			checkShippingVAT();
		}
	});
	$('select#id_shipping_address_country, select#id_address_country, input#id_vat_number').change(checkShippingVAT);

	//Initial promotional code check
	checkPromotionalCode();
	// checkShippingVAT();
}

function checkPromotionalCode() {
    //if ($('#id_promotion').val() != undefined) {
    //    if ($('#id_promotion').val().length == 6) {
    //        verifyPromotionalCode();
    //    } else {
    //        applyPromotion(0);
    //        $('.promotion .errorlist li').text('');
    //    }
	//}
}

function checkShippingVAT() {
	var shipping_code = $('select#id_shipping_address_country option:selected').val();
	var vat_number = $('#id_vat_number').val();

	if ($('#id_use_for_shipping').is(':checked')) {
	  shipping_code = $('select#id_address_country option:selected').val();
	}
	if (shipping_code != '') {
		$.post("/home/vat-rebate/", {shipping_code: shipping_code, vat_number: vat_number }, function(response) {
			var response_obj = JSON.parse(response);
			var vat_value = response_obj.value;
			rebateVAT(vat_value, response_obj.vat_country);
		});
	} else {
    rebateVAT(0, false);
	}
}

function rebateVAT(value, vat_country) {
	var shipping = parseFloat($('#shipping-total').text().replace(",", ""));
	var subtotal = parseFloat($('#home-subtotal').text().replace(",", ""));
	var promotion = parseFloat($('#home-promotion').text().replace(",", ""));
	var vat_number_field = $('#vat_numer_fieldset');
	subtotal -= promotion;
	var total = subtotal + shipping;
	var vat_el = $('#vat-row');

	if (vat_country) {
		vat_number_field.fadeIn();
	} else {
		vat_number_field.fadeOut(function() {
			vat_number_field.val('');
		});
	}

	if (value > 0) {
		var vat = subtotal / (100 + value) * value;
		subtotal -= vat;
		$('#vat-value').text(CommaFormatted(vat.toFixed(2)));

		vat_el.fadeIn();
	} else {
		vat_el.fadeOut();
	}
  total = subtotal+shipping;
	$('#home-total').text(CommaFormatted(total.toFixed(2)));
}

function check_valid_order() {
	$.ajax({
		type: 'GET',
		url: "/home/get_cart_data/",
		success: function (resp) {
			if (resp.total_price > 0) {
				$(".card-details-wrapper").removeClass('hide');
			} else {
				if (resp.total_quantity <= 0) { // empty basket
					location.href = '/';
				} else { // 100% discount
					$(".card-details-wrapper").addClass('hide');
				}
			}
		}
	})
}

function initProductAttributes($parent) {
	$parent.find('.single-product').each(function(index, product) {
		var $attributes = $(product).find('.product-attribute');
		$attributes.each(function(i, attribute) {
			var $attribute = $(attribute);
			var $attributes_section = $attribute.find('p.attributes');
			$attributes.each(function(j, attribute_j) {
				var $attribute_j = $(attribute_j);
				// if ($attribute.attr('data-id') == $attribute_j.attr('data-id')) {
				// 	$attributes_section.append('<span class="swap-att">'+$attribute_j.attr('data-title')+'</span>');
				// } else {
				// 	$attributes_section.append('<span class="swap-att"><a href="'+$attribute_j.attr('data-id')+'" class="swap">show '+$attribute_j.attr('data-title')+'</a></span>');
				// }
			});
		});
	});

	////this comes from wrongshop

	// $parent.find('.single-product .product-attribute a.swap').each(function(i,link) {
	// 	var $link = $(link);
	// 	$link.click(function(){
	// 		var $single_product = $link.parents('.single-product');
	// 		$single_product.find('.product-attribute:visible').hide();
	// 		$single_product.find('.product-attribute[data-id="'+$link.attr("href")+'"]').show();

	// 		return false;
	// 	});
	// });
}



/*! from ws.js */
$(document).ready(function(){


	$('#id_use_for_shipping').change(function(){
		showShippingAddressChange();
   	 });



	$('.checkout').ready(function(){
		initCheckoutForm();
		initShippingAddress();
		checkout = true;
	});

	$('.show-cvv').click(function(){
		$('#cvv').fadeIn('fast');
	});

	$('.close-cvv, #cvv').click(function(){
		$('#cvv').fadeOut('fast');
	});

	$('.submit-form').click(function () {
		$("#subscribe").submit();
	});

	// Prevent mailing list form being submitted if tick box not checked
	$('#subscribe').submit(function(event){
		if ($('#fielddykjkie-0').not(':checked').length){
			event.preventDefault();
            $('.error').fadeIn('fast');
        }
	});


	initProductAttributes($('body'));
});