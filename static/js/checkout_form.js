$("#btn-submit-chkout").click(function () {
	var $btn_submit = $(this);
	var billing = {};
	billing.first_name = $("#id_first_name").val();
	billing.last_name = $("#id_last_name").val();
	billing.name = [billing.first_name, billing.last_name].join(" ");
	billing.email = $("#id_email").val();
	billing.telephone = $("#id_telephone").val();

	billing.address_line1 = $("#id_address_line1").val() + " " + $("#id_address_line2").val();
	billing.address_city = $("#id_address_city").val();
	billing.address_state = $("#id_address_state").val();
	billing.address_zip = $("#id_address_postcode").val();
	billing.address_country = $("#id_address_country").val();
	billing.currency = "gbp";

	var options = {};
	options.is_shipping_to_billing = true;
	if ($('#id_use_for_shipping').length) {
		options.is_shipping_to_billing = $('#id_use_for_shipping:checkbox:checked').length == 1;
	}

	var shipping = {};
	shipping.first_name = $("#id_shipping_first_name").val();
	shipping.last_name = $("#id_shipping_last_name").val();
	shipping.name = [shipping.first_name, shipping.last_name].join(" ");

	shipping.address_line1 = $("#id_shipping_address_line1").val() + " " + $("#id_shipping_address_line2").val();
	shipping.address_city = $("#id_shipping_address_city").val();
	shipping.address_state = $("#id_shipping_address_state").val();
	shipping.address_zip = $("#id_shipping_address_postcode").val();
	shipping.address_country = $("#id_shipping_address_country").val();

	$("#CardName").val(billing.name); //billing name

	var is_valid = true;

	$(".form-row-input-group").find(".input-checkout").each(function () {
		var $ele = $(this);

		$ele.parent().find("small").remove();
	});

	$("#checkout__billing_details").find(".input-checkout").each(function () {
		var $ele = $(this);

		if ($ele.prop("required")) {
			var label = $("label[for='" + $ele.attr("id") + "']");

			if (label) { // add "error" to label
				if ($ele.val()) {
					label.removeClass("form-error");
				} else if (label.find('span.form-error').length <= 0) {
					is_valid = false;
					label.addClass("form-error");
					$ele.parent().addClass('error');
				} else {
					is_valid = false;
				}
			}
		}
	});

	if (!$("#id_use_for_shipping").prop("checked")) {
		$("#id_shipping_first_name").prop('required', true);
		$("#id_shipping_last_name").prop('required', true);
		$("#id_shipping_address_line1").prop('required', true);
		$("#id_shipping_address_city").prop('required', true);
		$("#id_shipping_address_postcode").prop('required', true);
		$("#id_shipping_address_country").prop('required', true);

		$("#checkout__shipping_address").find(".input-checkout").each(function () {
			var $ele = $(this);

			if ($ele.prop("required")) {
				var label = $("label[for='" + $ele.attr("id") + "']");

				if (label) { // add "error" to label
					if ($ele.val()) {
						label.removeClass("form-error");
					} else if (label.find('span.form-error').length <= 0) {
						is_valid = false;
						label.addClass("form-error");
						$ele.parent().addClass('error');
					} else {
						is_valid = false;
					}
				}
			}
		});
	}

	var label = $("#check_accept_lbl");
	var href = $("#check_accept_href");
	if ($("#id_checkbox_terms").is(':checked')) {
		label.css({"color":"black"});
		href.css({"color":"black"});
	} else {
		label.css({"color":"red"});
		href.css({"color":"black"});
		is_valid = false;
	}
	
	if ($('.promotion-error').text() != '') {
		is_valid = false;
	}

	if ($("#id_email").val() != $("#id_email_confirm").val()){
		is_valid = false;
		$("#id_email_confirm").val('');
	}

	if (!is_valid) {
		$("div.checkout-error").html('Please check the form and correct any errors');
		$('html, body').animate({scrollTop: 0}, 'fast');
		return;
	}

	// stripe.createToken(card_number, billing).then(function (result) {
	// 	if (result.error) {
	// 		$btn_submit.prop("disabled", false);
	// 		$("#id_card_errors").html(result.error.message);
	// 	} else {
	// 		$btn_submit.prop("disabled", true);
	// 		$('.btn__spinner').addClass('active');
	// 		$('.btn--buy').css('display', 'none');
	// 		console.log('clicked');
	// 		$("#id_card_errors").html("");
	// 		result.shipping = shipping;
	// 		result.options = options;
	// 		result.token.card.telephone = billing.telephone;
    //
	// 		console.log(result, "--- console result");
    //
	// 		$.ajax({
	// 			type: 'POST',
	// 			contentType: 'application/json; charset=utf-8',
	// 			data: JSON.stringify(result),
	// 			dataType: "json",
	// 			url: '/home/checkout/',
	// 			success: function (data) {
	// 				// Debug
	// 				console.log(data);
	// 				$("div.errors").html("");
    //
	// 				if (data["errors"]) {
	// 					for (var i = 0; i < data["errors"].length; i++) {
	// 						// Debug
	// 						console.log(data["errors"][i]);
	// 						$("div.errors").append('<p class="body-text">' + data["errors"][i] + '</p>');
	// 					}
	// 					$('html, body').animate({scrollTop: 0}, 'fast');
	// 					$btn_submit.prop("disabled", false);
	// 				}
    //
	// 				// Show successful message
	// 				if (data.transaction_id && data.order_number) {
	// 					$("div.message").html(
	// 							'<h2>Thank you</h2>' +
	// 							'<p>Your order was successful and we have received your payment. Your order number is WRO' + data.order_number + '.</p>' +
	// 							'<p>We have sent you an email with your order and shipping details. If you have any questions about your order, please do not hesitate to get in touch with us on <a href="mailto:orders@thewrongshop.co.uk">orders@thewrongshop.co.uk</a>.'
	// 					);
	// 					$(".checkout-form").html("");
	// 					$("#widget").html("");
	// 					$(".errors").html("");
	// 				}
	// 			},
	// 		});
	// 	}
	// });

});

$("#id_promotion").on("change", function () {
	$(".promotion-error").hide();

	var promotion_code = $(this).val();

	$.ajax({
		type: 'POST',
		url: "/home/check_promotion/",
		data: {"promotion_code": promotion_code},
		success: function (resp) {
			if (resp.is_valid) {
				$(".home-content").load("/home/index/", function () {
					updateCountyCode();
				});
				$(".promotion-error").text('');
			} else {
				$(".promotion-error").text(resp.msg).show();
			}
		},
		error: function() {
			$(".promotion-error").text('Something went wrong!').show();
		}
	});
});

if ($("#id_address_country").val() == "")
{
	var initial_cost = 0;
	$('#shipping-total').text(initial_cost.toFixed(2));
	var cart_sub_total = $('#home-subtotal').text();
	$('#home-total').text(cart_sub_total);
}