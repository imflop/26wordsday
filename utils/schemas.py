from template_schema.components import SingleButton, DropdownButton
from template_schema.handler import TemplateSchema, TemplateSchemaGroup, TemplateSchemaMethods


class Menu(TemplateSchemaGroup):
    """
    Класс для реализации бокового сворачивающегося меню
    """

    collapsible: bool = True
    is_open: bool = True

    @property
    def get_is_open(self) -> str:
        """
        Property для проверки состояния сайдбара - открыт/закрыт
        :return: str
        """
        return TemplateSchemaMethods.boolean_to_str_js_compatible(self.is_open)

    def initialize(self) -> None:
        """
        Метод для запуска инициализации меню. Установка кнопкам активного статуса при совпадении url, открытие
        выпадающего меню при наличии активной кнопки в нем
        :return: None
        """

        for button_key, button in self.elements.items():
            button.activate_by_url(self.schema.current_url)
            if isinstance(button, DropdownButton):
                for sub_button in button.sub_buttons.values():
                    url_check_result = sub_button.activate_by_url(self.schema.current_url)
                    if url_check_result:
                        parent_button = self.elements[button_key]
                        parent_button.open_dropdown()

    @classmethod
    def build(cls, **kwargs) -> TemplateSchemaGroup:
        """
        Метод для сборки сайдбара
        :return: None
        """
        instance = super().build(**kwargs)
        instance.initialize()
        return instance


class BaseApplicationSchema(TemplateSchema):
    """
    Базовая схема приложения
    """

    class Sidebar(Menu):
        """
        Класс для реализации сайдбара приложения
        """

        template_name = 'blocks/page/_generic_sidebar.html'
        unique_name = 'application_sidebar'
        grouper_map = {'Слова': ['random_word_set', 'exams'], 'Другое': ['words_sets_history', 'rating']}

        class SidebarSingleButton(SingleButton):
            """
            Класс для реализации одиночной кнопки сайдбара
            """

            highlight_class = 'active'
            common_css_classes = ['sidebar-btn', 'waves-btn']

        class SidebarDropdownButton(DropdownButton):
            """
            Класс для реализации кнопки с сворачивающимя меню для сайдбара
            """

            highlight_class = 'active'
            common_css_classes = ['sidebar-btn', 'waves-btn', 'js-collapsible-element-trigger']

        def get_elements(self) -> dict:

            return {
                'random_word_set': self.SidebarSingleButton(
                    key='random_word_set_button',
                    icon_before_title='landscape',
                    title='Случайная подборка',
                    html_params={'href': '#'},
                    active_url='/'
                ),
                'exams': self.SidebarSingleButton(
                    key='exams_button',
                    icon_before_title='school',
                    title='Экзамены',
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'words_sets_history': self.SidebarSingleButton(
                    key='words_sets_history_button',
                    icon_before_title='history',
                    title='История',
                    html_params={'href': '#'},
                    active_url='#',
                    css_classes=['disabled-btn']
                ),
                'rating': self.SidebarSingleButton(
                    key='rating_button',
                    icon_before_title='call_made',
                    title='Рейтинг',
                    html_params={'href': '#'},
                    active_url='#'
                )
            }
