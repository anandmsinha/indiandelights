(function($, window, document) {
  var addToCart, cartHtml, csrfSafeMethod, csrftoken, equalHeight, getCookie, infoMessages, loopStatusBtn, objectSize, requestUrls, sameOriginUrl, showErrorToast, showSuccessToast, updateCart;
  toastr.options = {
    closeButton: true,
    debug: false,
    progressBar: false,
    positionClass: 'toast-bottom-right',
    showDuration: '300',
    hideDuration: '1000',
    timeOut: '5000',
    extendedTimeOut: '1000',
    showEasing: 'swing',
    hideEasing: 'linear',
    showMethod: 'fadeIn',
    hideMethod: 'fadeOut'
  };
  showSuccessToast = function(message) {
    return toastr["success"](message);
  };
  showErrorToast = function(message) {
    return toastr["error"](message);
  };
  requestUrls = {
    baseUrl: '/',
    addToCart: '/item/cart/'
  };
  infoMessages = {
    itemAdded: 'Item successfully added to cart',
    itemRemoved: 'Item successfully removed from cart',
    error: 'Some error has occured',
    errorRefresh: 'Some error has occured please refresh the page and try again.'
  };
  cartHtml = {
    emptyCart: '<p class="text-info">Your cart is empty</p>',
    mediaObject: '<div class="media"><a href="#" class="pull-left"><img width="40" height="36" src="{0}" alt=""></a>' + '<div class="media-body"><a href="#">{1}</a><p>Qty - {2} X {3}</p></div></div>'
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
    bformat = cartHtml.mediaObject;
    cartSize = objectSize(cart);
    $.each(cart, function(k, v) {
      return htmlop += bformat.format(v.thumbnail, v.name, v.qty, v.qty_display);
    });
    if (cartSize > 0) {
      $('#main__cart__btn__codes').removeClass('hide');
      $('#cart__dropdown').html(htmlop);
    } else {
      $('#main__cart__btn__codes').addClass('hide');
      $('#cart__dropdown').html(cartHtml.emptyCart);
    }
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
          updateCart(data.cart);
          return showSuccessToast(msg);
        } else {
          return showErrorToast(infoMessages.error);
        }
      },
      error: function(data) {
        return showErrorToast(infoMessages.error);
      }
    });
  };
  $(document).on('click', '.add__to__cart__btn', function(e) {
    var link, qty;
    link = $(this);
    if (!link.hasClass('disabled')) {
      qty = link.parent().find('.special__select__box').val();
      link.addClass('disabled');
      link.attr('disabled', 'disabled');
      addToCart(link.attr('pid'), qty, infoMessages.itemAdded);
      link.removeClass('disabled');
      link.removeAttr('disabled');
    }
    return false;
  });
  loopStatusBtn = function(btn) {
    var tmpDisbAttr;
    tmpDisbAttr = btn.attr('disabled');
    return !((typeof tmpDisbAttr !== typeof void 0) && (tmpDisbAttr !== false));
  };
  $(document).on('click', '#product__pchase__btn', function(e) {
    var mainBtn;
    mainBtn = $(this);
    if (loopStatusBtn(mainBtn)) {
      mainBtn.attr('disabled', 'disabled');
      addToCart(mainBtn.attr('pid'), $('#product__pchase__select').val(), infoMessages.itemAdded);
      return mainBtn.removeAttr('disabled');
    }
  });
  $(document).on('click', '#cart__ck__upd__cart', function(e) {
    var cart__inputs, items_array, quantity_array;
    cart__inputs = $('#cart__ck__table__body').find('.cart__ck__input__qty');
    items_array = [];
    quantity_array = [];
    cart__inputs.each(function(index) {
      var newval, oldval;
      oldval = parseInt($(this).attr('oval'));
      newval = parseInt($(this).val());
      if (oldval !== newval) {
        items_array.push($(this).attr('pid'));
        return quantity_array.push(newval);
      }
    });
    if (items_array.length === 0) {
      return showSuccessToast('No change detected in cart.');
    } else {
      return $.ajax({
        type: 'POST',
        url: requestUrls.addToCart,
        data: {
          type: 'update',
          'products[]': items_array,
          'quantity[]': quantity_array
        },
        success: function(data) {
          var cartData, cartPriceTotal, cartSize, mainHtml;
          if (data.cart) {
            cartData = data.cart;
            updateCart(cartData);
            cartSize = objectSize(cartData);
            if (cartSize > 0) {
              mainHtml = '';
              cartPriceTotal = 0;
              $.each(cartData, function(key, val) {
                cartPriceTotal += parseFloat(val.subtotal);
                return mainHtml += "<tr class=\"cart__item__row\"><td><img src=\"" + val.thumbnail + "\"></td><td>" + val.name + "</td><td>" + val.price + "<td><input type=\"number\" step=\"1\" class=\"cart__ck__input__qty\" pid=\"" + val.pk + "\" min=\"1\" oval=\"" + val.qty + "\" value=\"" + val.qty + "\" /></td><td><button pid=\"" + val.pk + "\" mtotal=\"" + val.subtotal + "\" type=\"button\" class=\"btn btn-danger cart__ck__remove btn-xs\">Remove</button></td><td><b>" + val.subtotal + " Rs</b></td>";
              });
              mainHtml += "<tr><td colspan=\"4\"><button id=\"cart__ck__upd__cart\" type=\"button\" class=\"btn btn-info pull-right\">Update Cart</button></td><td><p class=\"pull-right\">Total</p></td><td><b><span id=\"cart__ck__total__cost\">" + cartPriceTotal + "</span> Rs</b></td></tr>";
              $('#cart__ck__table__body').html(mainHtml);
            } else {
              $('#cart__ck__main__table').html(cartHtml.emptyCart);
            }
            return showSuccessToast('Cart updated');
          } else {
            return showErrorToast('Cart update failed');
          }
        }
      });
    }
  });
  return $(document).on('click', '.cart__ck__remove', function(e) {
    var removeBtn;
    removeBtn = $(this);
    if (!removeBtn.hasClass('disabled')) {
      removeBtn.addClass('disabled');
      $.ajax({
        type: 'POST',
        url: requestUrls.addToCart,
        data: {
          type: 'remove',
          pid: removeBtn.attr('pid')
        },
        success: function(data) {
          var cartData, cartSize, total;
          if (data.cart) {
            cartData = data.cart;
            updateCart(cartData);
            cartSize = objectSize(cartData);
            if (cartSize > 0) {
              total = parseFloat($('#cart__ck__total__cost').text()) - parseFloat(removeBtn.attr('mtotal'));
              $('#cart__ck__total__cost').text(total);
              removeBtn.parent().parent().remove();
            } else {
              $('#cart__ck__main__table').html(cartHtml.emptyCart);
            }
            return showSuccessToast(infoMessages.itemRemoved);
          } else {
            return showErrorToast(infoMessages.errorRefresh);
          }
        },
        error: function(data) {
          return showErrorToast(infoMessages.errorRefresh);
        }
      });
      return removeBtn.removeClass('disabled');
    }
  });
})(jQuery, window, document);
