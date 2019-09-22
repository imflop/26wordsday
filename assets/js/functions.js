// Контейнерные функции

const twentysixwordsday = {
    /*
    Контейнер для хранения основных функций приложения
    */
    initSidebar: function () {
        /*
        Функция для инициализации сайдбара
        */
        const sidebar_selector = '.js-twentysixwords_sidebar';
        let sidebar = new Sidebar(sidebar_selector);
        sidebar.init_collapsible_elements();

        $(sidebar_selector).on('click', '.js-sidebar_toggle_btn', function (e) {
            /*
            Сигнал на раскрытие/свертывание сайдбара
            */
            if ($(window).width() > 700){
                sidebar.toggleSidebar();
            }
        });
        $(sidebar_selector).on('click', '.js-sidebar_dropdown_toggle_btn', function (e) {
            /*
            Сигнал на раскрытие/свертывание элемента 'dropdown' сайдбара
            */
            sidebar.toggleDropdown($(this));
        });
        $(window).on('load resize', function() {
            /*
            Сигнал для раскрытия/свертывания сайдбара при определенном размере видимой области экрана
            */
            if ($(window).width() < 700){
                sidebar.closeSidebar();
            }
        });
    }
};