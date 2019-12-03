function Sidebar (sidebar_selector) {
    /*
    Сервис-функция для управления сайдбаром
    */
    const sidebar = $(sidebar_selector);
    const service = new CollapsibleElement();

    this.toggleSidebar = function () {
        /*
        Метод для раскрытия/свертывания сайдбара
        */
        service.toggle_(sidebar);
    };

    this.openSidebar = function () {
        /*
        Метод для раскрытия сайдбара
        */
        service.toggle_(sidebar, false);
    };

    this.closeSidebar = function () {
        /*
        Метод для свертывания сайдбара
        */
        service.toggle_(sidebar, true);
    };
}

function initSimpleSidebar(sidebar_selector, sidebar_trigger_selector, collapse_on=700) {
    /*
    Функция для инициализации сайдбара
    */
    let sidebar = new Sidebar(sidebar_selector);

    $(sidebar_selector).on('click', sidebar_trigger_selector, function (e) {
        /*
        Сигнал на раскрытие/свертывание сайдбара
        */
        if ($(window).width() > collapse_on){
            sidebar.toggleSidebar();
        }
    });

    // При загрузке страницы также нужно проверять размер видимой области экрана
    resizeSidebar();

    $(window).on('resize', function() {
        /*
        Сигнал для раскрытия/свертывания сайдбара при изменении размера видимой области экрана
        */
        resizeSidebar();
    });

    function resizeSidebar() {
        if ($(window).width() < collapse_on){
            sidebar.closeSidebar();
        }
    }

}