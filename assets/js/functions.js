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

        initSimpleCollapsibleElement(collapsible_element_selector, trigger_selector)

    },

    initSidebar: function () {
        /*
        Функция для инициализации сайдбара
        */

        const sidebar_selector = '.js-collapsible_sidebar';
        const sidebar_trigger_selector = '.js-sidebar_toggle_btn';
        const collapse_on = 700;

        initSimpleSidebar(sidebar_selector, sidebar_trigger_selector, collapse_on)

    }
};