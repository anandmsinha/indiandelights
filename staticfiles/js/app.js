(function($, window, document) {
  var addToCart, csrfSafeMethod, csrftoken, equalHeight, getCookie, objectSize, requestUrls, sameOriginUrl, updateCart;
  requestUrls = {
    baseUrl: '/',
    addToCart: '/item/cart/'
  };
  if (!String.prototype.format) {
    String.prototype.format = function() {
      var args;
      args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) {
        if (typeof args[number] !== "undefined") {
          return args[number];
        } else {
          return match;
        }
      });
    };
  }
  objectSize = function(the_object) {
    var key, object_size;
    object_size = 0;
    for (key in the_object) {
      if (the_object.hasOwnProperty(key)) {
        object_size++;
      }
    }
    return object_size;
  };
  csrfSafeMethod = function(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };
  sameOriginUrl = function(url) {
    var host, origin, protocol, sr_origin;
    host = document.location.host;
    protocol = document.location.protocol;
    sr_origin = '//' + host;
    origin = protocol + sr_origin;
    return (url === origin || url.slice(0, origin.length + 1) === origin + '/') || (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
  };
  getCookie = function(name) {
    var cookie, cookieValue, cookies, cookiesLength, i, nameLength;
    cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      cookies = document.cookie.split(';');
      i = 0;
      cookiesLength = cookies.length;
      while (i < cookiesLength) {
        cookie = $.trim(cookies[i]);
        nameLength = name.length + 1;
        if (cookie.substring(0, nameLength) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(nameLength));
          break;
        }
        ++i;
      }
    }
    return cookieValue;
  };
  csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
        return xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  equalHeight = function(group, state) {
    var changeHeight, tallest;
    if (!state) {
      return group.each(function() {
        return $(this).height(345);
      });
    } else {
      tallest = 0;
      changeHeight = false;
      if (group.length > 0) {
        tallest = $(group[0]).height();
      }
      group.each(function() {
        var tmpHeight;
        tmpHeight = $(this).height();
        if (tmpHeight > tallest) {
          tallest = tmpHeight;
          return changeHeight = true;
        }
      });
      if (changeHeight) {
        return group.each(function() {
          return $(this).height(tallest);
        });
      }
    }
  };
  $(function() {
    return equalHeight($('.product__300__thumbnail'), false);
  });
  $(window).resize(function(e) {
    return equalHeight($('.product__300__thumbnail'), true);
  });
  updateCart = function(cart) {
    var bformat, cartSize, htmlop;
    htmlop = '';
    bformat = '<div class="media"><a href="#" class="pull-left"><img width="40" height="36" src="{0}" alt=""></a>' + '<div class="media-body"><a href="#">{1}</a><p>Qty - {2} X {3}</p></div></div>';
    cartSize = objectSize(cart);
    $.each(cart, function(k, v) {
      return htmlop += bformat.format(v.thumbnail, v.name, v.qty, v.qty_display);
    });
    if (cartSize > 0) {
      $('#main__cart__btn__codes').removeClass('hide');
    } else {
      $('#main__cart__btn__codes').addClass('hide');
    }
    $('#cart__dropdown').html(htmlop);
    return $('#cart__default__count').text(cartSize);
  };
  addToCart = function(id, qty, msg) {
    return $.ajax({
      type: 'POST',
      url: requestUrls.addToCart,
      data: {
        type: 'add',
        pid: id,
        quantity: qty
      },
      success: function(data) {
        if (data.cart) {
          return updateCart(data.cart);
        }
      },
      error: function(data) {
        return alert('Some error has occured');
      }
    });
  };
  return $(document).on('click', '.add__to__cart__btn', function(e) {
    var link, qty;
    link = $(this);
    if (!link.hasClass('disabled')) {
      qty = link.parent().find('.special__select__box').val();
      link.addClass('disabled');
      addToCart(link.attr('pid'), qty, 'Your item has been succesfully added to cart.');
      link.removeClass('disabled');
    }
    return false;
  });
})(jQuery, window, document);
