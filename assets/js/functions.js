// Контейнерные функции

const twentysixwordsday = {
    /*
    Контейнер для хранения основных функций приложения
    */
    initDropdown: function () {
        /*
        Функция для инициализации сворачиваемых элементов
        */

        const collapsible_element_selector = '.js-collapsible-element-wrapper';
        const trigger_selector = '.js-collapsible-element-trigger';

        if ($(collapsible_element_selector).length && $(trigger_selector).length) {
            initSimpleCollapsibleElement(collapsible_element_selector, trigger_selector);
        }
    },

    initSidebar: function () {
        /*
        Функция для инициализации сайдбара
        */

        const sidebar_selector = '.js-collapsible_sidebar';
        const sidebar_trigger_selector = '.js-sidebar_toggle_btn';
        const collapse_on = 700;

        if ($(sidebar_selector).length && $(sidebar_trigger_selector).length) {
            initSimpleSidebar(sidebar_selector, sidebar_trigger_selector, collapse_on)
        }
    },

    initTray: function () {
        /*
        Функция для инициализации tray
        */

        const tray = new Tray('#landing-tray', 12);
        tray.updateHeaderTitle('Last Events');
        tray.addOrUpdateMessageItem('1', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('3', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('5', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('y', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('u', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('g', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('d', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('a', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('a', 'eeeerrr44rr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('3g', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('4d', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('5a', 'eeeerrrrr', '334455', 'ggyyy66', 'tttt');
        tray.addOrUpdateMessageItem('6a', 'eeeerrr44rr', '334455', 'ggyyy66', 'tttt');
    },

    initFloatingAjax: function () {
        // инициализация динамических сообщений.
        const messenger = new Messages();
        const preloader = new messenger.fullScreen();
        // инициализация загрузчика контента по ajax.
        const ajax_loader = new FloatingAjaxLoader();
        const icons_setup = {
            'NEUTRAL': '/assets/img/logo_big_anim_4_inf.png',
            'ERROR': '/assets/img/logo_big_anim_3.png'
        };
        const text_setup = {
            'POST_TEXT': 'Sending to the server...',
            'LOADING_TEXT': 'Loading from the server...'
        };

        ajax_loader.preloader = preloader;
        ajax_loader.loader_icon = icons_setup.NEUTRAL;
        ajax_loader.loader_error_icon = icons_setup.ERROR;
        ajax_loader.post_icon = icons_setup.NEUTRAL;
        ajax_loader.post_error_icon = icons_setup.ERROR;
        ajax_loader.post_text = text_setup.POST_TEXT;
        ajax_loader.initSignals();

        ajax_loader.preparePOSTDataCallback = function (form_obj, data, post_type, data_options) {

            // const container = $(data_options[ajax_loader.container_data_attr]);

            switch (post_type) {
                default:
                    data = form_obj.serialize();
                    break;
            }
            return data;
        };

        ajax_loader.preparePostCallback = function (form_obj, data, post_type, data_options) {
            return function(response) {
                switch (post_type) {
                    default:
                        if (response['errors']) {
                            //
                        } else {
                            //
                        }
                        break;
                }
            }
        };
    },

    initFloatingWindows: function () {
        const fw_windows = {
            'AUTH': 'auth'
        };
        // инициализация загрузчика всплывающих окон.
        const fw = new FloatingWindows();
        fw.set_windows_ids_to_url = true;
        fw.push_windows_events_to_history = true;
        // здесь нужно перечислить id всплывающих окон, через запятую, к которым привязаны кнопки их вызова.
        fw.initWindows(fw_windows.AUTH);

        $(document).on('floating-window:opened', function (event, window_id, options) {
            // отслеживание сигналов об открытии всплывающих окон для подгрузки в них контента.
        });
    },

    initShowPasswordFeature: function () {
        $(document).on('click', '.js-password_toggle_btn', function (event) {
            const input = $(this).closest('.js-input_wrapper').find('input');
            const button = $(this);

            if (input.attr('type') === 'password') {
                input.attr('type', 'text');
                button.addClass('active');
            } else {
                input.attr('type', 'password');
                button.removeClass('active');
            }

            event.preventDefault();
        })
    }
};