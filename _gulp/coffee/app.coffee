(($, window, document) ->
    requestUrls = 
        baseUrl: '/'
        addToCart: '/item/cart/'

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

    equalHeight = (group) ->
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
        equalHeight $('.product__300__thumbnail')

    $(window).resize (e) ->
        equalHeight $('.product__300__thumbnail')

    updateCart = (cart) ->
        htmlop = ''
        bformat = '<div class="media"><a href="#" class="pull-left"><img width="40" height="36" src="{0}" alt=""></a>' + 
            '<div class="media-body"><a href="#">{1}</a><p>Qty - {2} X {3}</p></div></div>'
        cartSize = objectSize(cart)
        $.each cart, (k, v) ->
            htmlop += bformat.format(v.thumbnail, v.name, v.qty, v.qty_display)
        if cartSize > 0
            $('#main__cart__btn__codes').removeClass('hide')
        else
            $('#main__cart__btn__codes').addClass('hide')
        $('#cart__dropdown').html htmlop
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
            error: (data) ->
                alert('Some error has occured')

    $(document).on 'click', '.add__to__cart__btn', (e) ->
        link = $(this)
        if !link.hasClass 'disabled'
            qty = link.parent().find('.special__select__box').val()
            link.addClass 'disabled'
            addToCart(link.attr('pid'), qty, 'Your item has been succesfully added to cart.')
            link.removeClass 'disabled'
        return false
) jQuery, window, document