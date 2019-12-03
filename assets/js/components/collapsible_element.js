function CollapsibleElement() {
    /*
    Сервис-функция для управления сворачиваемыми элементами
    */
    const self = this;

    this.initCollapsibleElements = function () {
        /*
        Метод инициализации css-классов для сворачиваемых элементов
        */
        $('[data-is-open="true"]').addClass('is-open');
        $('[data-is-open="false"]').addClass('closed');
    };

    this.toggleCollapsibleElementByTrigger = function (trigger, collapsible_element_selector) {
        /*
        Метод для раскрытия/свертывания элементов 'collapsible'
        */
        const element = $(trigger).closest(collapsible_element_selector);
        self.toggle_(element);
    };

    this.toggle_ = function(element_object, state_to_close=null) {
        /*
        Функция для назначения атрибутов сворачиваемым элементам
        */
        if (state_to_close === null && element_object.hasClass('is-open') || state_to_close) {
            element_object.removeClass('is-open');
            element_object.attr('data-is-open', false);
        }
        else {
            element_object.addClass('is-open');
            element_object.attr('data-is-open', true);
        }
    }
}

function initSimpleCollapsibleElement(collapsible_element_selector, trigger_selector) {
    /*
    Функция для инициализации сворачиваемых элементов
    */

    const service = new CollapsibleElement();
    service.initCollapsibleElements();

    $(document).on('click', trigger_selector, function (e) {
        /*
        Сигнал на раскрытие/свертывание collapsible-элемента
        */
        service.toggleCollapsibleElementByTrigger($(this), collapsible_element_selector);
    });

}