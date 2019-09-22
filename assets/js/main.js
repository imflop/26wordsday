// Сервисные функции

function Sidebar (selector) {
    /*
    Сервис-функция для управления сайдбаром
    */
    const sidebar_btn_main_wrapper_selector = '.js-sidebar_btn_main_wrapper';
    const sidebar = $(selector);

    this.init_collapsible_elements = function () {
        /*
        Метод инициализации css-классов для сворачиваемых элементов
        */
        $('[data-is-open="true"]').addClass('is-open');
        $('[data-is-open="false"]').addClass('closed');
    };

    this.toggleSidebar = function () {
        /*
        Метод для раскрытия/свертывания сайдбара
        */
        toggle_sidebar_element(sidebar);
    };

    this.openSidebar = function () {
        /*
        Метод для раскрытия сайдбара
        */
        toggle_sidebar_element(sidebar, false);
    };

    this.closeSidebar = function () {
        /*
        Метод для свертывания сайдбара
        */
        toggle_sidebar_element(sidebar, true);
    };

    this.toggleDropdown = function (dropdown_toggle_btn) {
        /*
        Метод для раскрытия/свертывания элементов 'dropdown'
        */
        const dropdown = dropdown_toggle_btn.closest(sidebar_btn_main_wrapper_selector);
        toggle_sidebar_element(dropdown);
    };

    function toggle_sidebar_element(element, state_to_close=null) {
        /*
        Функция для назначения атрибутов сворачиваемым элементам
        */
        if (state_to_close === null && element.hasClass('is-open') || state_to_close) {
            element.removeClass('is-open');
            element.attr('data-is-open', false);
        }
        else {
            element.addClass('is-open');
            element.attr('data-is-open', true);
        }
    }
}

function Messages(container){
    // Сервис для вывода сообщений пользователю о каких-либо операциях

    let msgContainer = $(container);

    this.fullScreen = function () {
        // Сообщение - заполнение экрана (указанного блока) по таймеру

        self = this;

        const message = (
            $('<div/>', {
                class: 'js-full-screen-message',
                style: 'position: absolute;' +
                       'display: flex;' +
                       'align-items: center;' +
                       'justify-content: center;' +
                       'top: 0;' +
                       'left: 0;' +
                       'right: 0;' +
                       'bottom: 0;' +
                       'z-index: 100;' +
                       'text-align: center;' +
                       'color: white;'
            }).append(
                $('<div/>',{
                    class: 'js-full-screen-message-img',
                    style: 'display: block;' +
                           'padding: 0 auto;' +
                           // 'position: fixed;' +
                           // 'top: 50%;' +
                           // 'left: 50%;' +
                           // 'transform: translate(-50%, -50%);' +
                           'text-align: center;'
                }).append(
                    $('<img>', {
                        style: 'width: 6rem;' +
                               'height: 6rem;',
                        src: ''
                    })
                ).append(
                    $('<div/>',{
                        class: 'js-full-screen-message-text',
                        style: 'font-size: 20px;' +
                               'margin-top: 20px;' +
                               'color: #900;'
                    })
                ).append(
                    $('<div/>',{
                        class: 'js-full-screen-tip-message-text',
                        style: 'font-size: 14px;' +
                               'color: #56C7E1;'
                    })
                )
            )
        );

        const returnButton = (
            $('<button/>',{
                class: 'waves-effect waves-light btn js-return-btn',
                style: 'background-color: #900;' +
                       'margin-top: 40px;',
                html: 'Cancel'
            })
        );

        this.showTimeOutMessage = function(icon='', text='', timeOut=600, animation='slow', callback=null) {
            // Метод для отображения сообщения по таймеру

            message.find('.js-full-screen-message-text').text(text);
            message.find('img').attr('src', icon);

            msgContainer.append(message).fadeIn(animation);
            setBlur(msgContainer);

            $.when(
                setTimeout(function() {

                    setBlur(msgContainer, '');
                    message.remove();

                }, timeOut)
            ).done(function (){
                if(callback){
                    setTimeout(function() {

                        callback();

                    }, timeOut)
                }
            })
        };

        this.preloaderMessage = function (main, done, icon='', text='', iconOnFail='', textOnFail='',
                                          animation='slow', timeOut=200) {
            // Метод для отображения сообщения по завершению операций в кэлбэке main и выполнения операций
            // в кэлбэке done

            message.find('.js-full-screen-message-text').text(text);
            message.find('img').attr('src', icon);

            msgContainer.append(message).fadeIn(animation);
            msgContainer.find('.js-blur').css({
                'filter': 'blur(4px)', '-webkit-filter': 'blur(4px)'
            });

            setTimeout(function () {
                $.when(main).done(function (response){
                    message.remove();
                    done(response, message);
                }).fail(function (response){
                    self.addSimpleMessage(iconOnFail, textOnFail, animation)
                })
            }, timeOut);
        };

        this.addSimpleMessage = function (icon='', text='', animation='slow') {
            // Метод для вывода сообщений о произошедшей ошибке '.fail()'

            message.find('.js-full-screen-message-img').append(returnButton);
            message.find('.js-full-screen-message-text').text(text);
            message.find('img').attr('src', icon);
            msgContainer.append(message).fadeIn(animation);

            msgContainer.find('.js-blur').css({
                'filter': 'blur(4px)', '-webkit-filter': 'blur(4px)'
            });

            returnButton.click(function () {
                setBlur(msgContainer, '');
                message.remove();
            })
        };

        this.setTipMessage = function (text) {
            // Метод для установки текста подсказки в сообщение

            message.find('.js-full-screen-tip-message-text').css('margin-top', '20px').text(text);
        };

        function setBlur(parentContainerObj, value='blur(4px)') {
            // Функция для добавления стилевого размытия контейнера

            parentContainerObj.find('.js-blur').css({'filter': value, '-webkit-filter': value});
        }
    };
}