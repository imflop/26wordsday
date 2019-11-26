// Контейнерные функции

const twentysixwordsday = {
    /*
    Контейнер для хранения основных функций приложения
    */
    initDropdown: function() {
        /*
        Функция для инициализации сворачиваемых элементов
        */

        const service = new CollapsibleElement();
        service.init_collapsible_elements();

        $(document).on('click', '.js-collapsible-element-trigger', function (e) {
            /*
            Сигнал на раскрытие/свертывание элемента 'collapsible' сайдбара
            */
            service.toggleDropdown($(this));
        });

    },

    initSidebar: function () {
        /*
        Функция для инициализации сайдбара
        */
        const sidebar_selector = '.js-collapsible_sidebar';
        let sidebar = new Sidebar(sidebar_selector);

        $(sidebar_selector).on('click', '.js-sidebar_toggle_btn', function (e) {
            /*
            Сигнал на раскрытие/свертывание сайдбара
            */
            if ($(window).width() > 700){
                sidebar.toggleSidebar();
            }
        });

        $(window).on('load resize', function() {
            /*
            Сигнал для раскрытия/свертывания сайдбара при изменении размера видимой области экрана
            */
            if ($(window).width() < 700){
                sidebar.closeSidebar();
            }
        });

        // При загрузке страницы также нужно проверять размер видимой области экрана
        if ($(window).width() < 700){
            sidebar.closeSidebar();
        }
    }
};