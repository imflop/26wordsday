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
    }
};