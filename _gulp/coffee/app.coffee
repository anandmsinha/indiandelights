(($, window, document) ->
    # Configure toaster
    toastr.options =
        closeButton: true
        debug: false
        progressBar: false
        positionClass: 'toast-bottom-right'
        showDuration: '300'
        hideDuration: '1000'
        timeOut: '5000'
        extendedTimeOut: '1000'
        showEasing: 'swing'
        hideEasing: 'linear'
        showMethod: 'fadeIn'
        hideMethod: 'fadeOut'

    showSuccessToast = (message) ->
        toastr["success"](message)

    showErrorToast = (message) ->
        toastr["error"](message)

    requestUrls =
        baseUrl: '/'
        addToCart: '/item/cart/'

    infoMessages =
        itemAdded: 'Item successfully added to cart'
        itemRemoved: 'Item successfully removed from cart'
        error: 'Some error has occured'
        errorRefresh: 'Some error has occured please refresh the page and try again.'

    cartHtml =
        emptyCart: '<p class="text-info">Your cart is empty</p>'
        mediaObject: '<div class="media"><a href="#" class="pull-left"><img width="40" height="36" src="{0}" alt=""></a>' +
            '<div class="media-body"><a href="#">{1}</a><p>Qty - {2} X {3}</p></div></div>'

    unless String::format
      String::format = ->
        args = arguments
        @replace /{(\d+)}/g, (match, number) ->
          (if typeof args[number] isnt "undefined" then args[number] else match)

    objectSize = (the_object) ->
        object_size = 0
        for key of the_object
            object_size++  if the_object.hasOwnProperty(key)
        object_size

    csrfSafeMethod = (method) ->
        /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);

    sameOriginUrl = (url) ->
        host = document.location.host
        protocol = document.location.protocol
        sr_origin = '//' + host
        origin = protocol + sr_origin
        (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url))

    getCookie = (name) ->
        cookieValue = null
        if document.cookie and document.cookie != ''
            cookies = document.cookie.split(';')
            i = 0
            cookiesLength = cookies.length
            while i < cookiesLength
                cookie = $.trim(cookies[i])
                nameLength = name.length + 1
                if cookie.substring(0, nameLength) == (name + '=')
                    cookieValue = decodeURIComponent(cookie.substring(nameLength))
                    break
                ++i
        cookieValue

    csrftoken = getCookie('csrftoken')

    $.ajaxSetup
        beforeSend: (xhr, settings) ->
            if !csrfSafeMethod(settings.type) and !settings.crossDomain
                xhr.setRequestHeader("X-CSRFToken", csrftoken)

    equalHeight = (group, state) ->
        if !state
            group.each ->
                $(this).height(345)
        else
            tallest = 0
            changeHeight = false
            if group.length > 0
                tallest = $(group[0]).height()
            group.each ->
                tmpHeight = $(this).height()
                if tmpHeight > tallest
                    tallest = tmpHeight
                    changeHeight = true
            if changeHeight
                group.each ->
                    $(this).height(tallest)

    $ ->
        equalHeight $('.product__300__thumbnail'), false

    $(window).resize (e) ->
        equalHeight $('.product__300__thumbnail'), true

    updateCart = (cart) ->
        htmlop = ''
        bformat = cartHtml.mediaObject
        cartSize = objectSize(cart)
        $.each cart, (k, v) ->
            htmlop += bformat.format(v.thumbnail, v.name, v.qty, v.qty_display)
        if cartSize > 0
            $('#main__cart__btn__codes').removeClass('hide')
            $('#cart__dropdown').html htmlop
        else
            $('#main__cart__btn__codes').addClass('hide')
            $('#cart__dropdown').html cartHtml.emptyCart

        $('#cart__default__count').text cartSize

    addToCart = (id, qty, msg) ->
        $.ajax
            type: 'POST'
            url: requestUrls.addToCart
            data:
                type: 'add'
                pid: id
                quantity: qty
            success: (data) ->
                if data.cart
                    updateCart(data.cart)
                    showSuccessToast(msg)
                else
                    showErrorToast(infoMessages.error)
            error: (data) ->
                showErrorToast(infoMessages.error)

    $(document).on 'click', '.add__to__cart__btn', (e) ->
        link = $(this)
        if !link.hasClass 'disabled'
            qty = link.parent().find('.special__select__box').val()
            link.addClass 'disabled'
            link.attr 'disabled', 'disabled'
            addToCart(link.attr('pid'), qty, infoMessages.itemAdded)
            link.removeClass 'disabled'
            link.removeAttr 'disabled'
        return false

    loopStatusBtn = (btn) ->
        tmpDisbAttr = btn.attr 'disabled'
        return !((typeof tmpDisbAttr != typeof undefined) && (tmpDisbAttr != false))

    $(document).on 'click', '#product__pchase__btn', (e) ->
        mainBtn = $(this)
        if loopStatusBtn(mainBtn)
            mainBtn.attr('disabled', 'disabled')
            addToCart mainBtn.attr('pid'), $('#product__pchase__select').val(), infoMessages.itemAdded
            mainBtn.removeAttr 'disabled'

    $(document).on 'click', '#cart__ck__upd__cart', (e) ->
        cart__inputs = $('#cart__ck__table__body').find('.cart__ck__input__qty')
        items_array = []
        quantity_array = []
        cart__inputs.each (index) ->
            oldval = parseInt($(this).attr('oval'))
            newval = parseInt($(this).val())
            if oldval != newval
                items_array.push($(this).attr('pid'))
                quantity_array.push(newval)
        if items_array.length == 0
            showSuccessToast('No change detected in cart.')
        else
            $.ajax
                type: 'POST'
                url: requestUrls.addToCart
                data:
                    type: 'update'
                    'products[]': items_array
                    'quantity[]': quantity_array
                success: (data) ->
                    if data.cart
                        cartData = data.cart
                        updateCart(cartData)
                        cartSize = objectSize(cartData)
                        if cartSize > 0
                            mainHtml = ''
                            cartPriceTotal = 0
                            $.each cartData, (key, val) ->
                                cartPriceTotal += parseFloat(val.subtotal)
                                mainHtml += "<tr class=\"cart__item__row\"><td><img src=\"#{val.thumbnail}\"></td><td>#{val.name}</td><td>#{val.price}<td><input type=\"number\" step=\"1\" class=\"cart__ck__input__qty\" pid=\"#{val.pk}\" min=\"1\" oval=\"#{val.qty}\" value=\"#{val.qty}\" /></td><td><button pid=\"#{val.pk}\" mtotal=\"#{val.subtotal}\" type=\"button\" class=\"btn btn-danger cart__ck__remove btn-xs\">Remove</button></td><td><b>#{val.subtotal} Rs</b></td>"
                            mainHtml += "<tr><td colspan=\"4\"><button id=\"cart__ck__upd__cart\" type=\"button\" class=\"btn btn-info pull-right\">Update Cart</button></td><td><p class=\"pull-right\">Total</p></td><td><b><span id=\"cart__ck__total__cost\">#{cartPriceTotal}</span> Rs</b></td></tr>"
                            $('#cart__ck__table__body').html mainHtml
                        else
                            $('#cart__ck__main__table').html(cartHtml.emptyCart)
                        showSuccessToast('Cart updated')
                    else
                        showErrorToast('Cart update failed')

    $(document).on 'click', '.cart__ck__remove', (e) ->
        removeBtn = $(this)
        if !removeBtn.hasClass 'disabled'
            removeBtn.addClass 'disabled'
            $.ajax
                type: 'POST'
                url: requestUrls.addToCart
                data:
                    type: 'remove'
                    pid: removeBtn.attr('pid')
                success: (data) ->
                    if data.cart
                        cartData = data.cart
                        updateCart(cartData)
                        cartSize = objectSize(cartData)
                        if cartSize > 0
                            # Just remove this row and update total
                            total = parseFloat($('#cart__ck__total__cost').text()) - parseFloat(removeBtn.attr('mtotal'))
                            $('#cart__ck__total__cost').text(total)
                            removeBtn.parent().parent().remove()
                        else
                            $('#cart__ck__main__table').html(cartHtml.emptyCart)
                        showSuccessToast(infoMessages.itemRemoved)
                    else
                        showErrorToast(infoMessages.errorRefresh)
                error: (data) ->
                    showErrorToast(infoMessages.errorRefresh)
            removeBtn.removeClass 'disabled'

) jQuery, window, document