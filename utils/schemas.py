from typing import Type

from template_schema.components import SingleButton, MaterialIcon, Badge, SimpleMenu, BadgeDropdown, \
    TemplateSchemaHTMLElement
from template_schema.handler import TemplateSchema


class MainNavbar(SimpleMenu):
    """
    Класс для реализации навбара приложения
    """

    class NavbarSingleButton(SingleButton):
        """
        Класс для реализации одиночной кнопки сайдбара
        """

        highlight_class = 'active'
        common_css_classes = ['navbar-btn', 'waves-btn']
        tag = 'button'

    def get_elements(self) -> dict:
        return {
            'navbar_button_1': self.NavbarSingleButton(
                key='navbar_button_1',
                icon_before_title=MaterialIcon('landscape'),
                title=None,
                active_url='/words/list/'
            ),
            'navbar_button_2': self.NavbarSingleButton(
                key='navbar_button_2',
                icon_before_title=MaterialIcon('landscape'),
                title=None
            ),
            'navbar_button_3': self.NavbarSingleButton(
                key='navbar_button_3',
                icon_before_title=MaterialIcon('landscape'),
                title=None
            )
        }

    def extend_context_data(self) -> dict:
        return dict(app_schema=self.schema)


class MainSidebar(SimpleMenu):
    """
    Класс для реализации сайдбара приложения
    """

    class SidebarSingleButton(SingleButton):
        """
        Класс для реализации одиночной кнопки сайдбара
        """

        highlight_class = 'active'
        common_css_classes = ['sidebar-btn', 'waves-btn']
        additional_element = TemplateSchemaHTMLElement(css_classes=['inner-btn-border-right'])

    class SidebarButtonTitle(TemplateSchemaHTMLElement):
        """
        Класс для вывода наименований кнопок
        """

        common_css_classes = ['title', 'hide-on-sidebar-close']

    class LogoImage(TemplateSchemaHTMLElement):
        """
        Класс для вывода изображения-логотипа
        """

        html_string = '<img %(html_params)s>'
        common_html_params = {'height': 22, 'width': 23}

    class LogoTitle(TemplateSchemaHTMLElement):
        """
        Класс для вывода текста к логотипу
        """

        common_css_classes = {'hide-on-sidebar-close'}

    def get_elements(self) -> dict:
        return {
            'random_word_set': self.SidebarSingleButton(
                key='random_word_set_button',
                icon_before_title=MaterialIcon('landscape'),
                title=self.SidebarButtonTitle('Случайная подборка'),
                html_params={'href': '#'},
                active_url='/words/list/'
            ),
            'exams': self.SidebarSingleButton(
                key='exams_button',
                icon_before_title=MaterialIcon('school'),
                title=self.SidebarButtonTitle('Экзамены'),
                html_params={'href': '#'},
                active_url='#',
                css_classes=['disabled-btn']
            ),
            'words_sets_history': self.SidebarSingleButton(
                key='words_sets_history_button',
                icon_before_title=MaterialIcon('history'),
                title=self.SidebarButtonTitle('История'),
                html_params={'href': '#'},
                active_url='#',
                css_classes=['disabled-btn']
            ),
            'rating': self.SidebarSingleButton(
                key='rating_button',
                icon_before_title=MaterialIcon('call_made'),
                title=self.SidebarButtonTitle('Рейтинг'),
                html_params={'href': '#'},
                active_url='#'
            ),
            'toggle_button': SingleButton(
                key='toggle_button',
                title=self.SidebarButtonTitle('Свернуть'),
                icon_after_title=MaterialIcon('keyboard_arrow_left', css_classes=['hide-on-sidebar-close']),
                icon_before_title=MaterialIcon('keyboard_arrow_right', css_classes=['hide-on-sidebar-open']),
                css_classes=['sidebar-toolbar-btn', 'js-sidebar_toggle_btn']
            )
        }

    def extend_context_data(self) -> dict:
        return dict(app_schema=self.schema)

    def get_toggle_button(self) -> Type[SingleButton]():
        return self.elements.get('toggle_button')


class ProfileDropdown(BadgeDropdown):
    """
    Класс для реализации выпадающего меню профиля
    """

    class MenuButton(SingleButton):
        """
        Класс для реализации кнопки внутреннего меню
        """

        tag = 'button'
        common_css_classes = ['dropdown-item']

    class Row(TemplateSchemaHTMLElement):
        """
        Класс для реализации строки
        """

        html_string = '<div class="%(css_classes)s"><span>%(data)s</span>%(icon)s</div>'
        common_css_classes = ['row', 'info-badge-row-description']

    def set_face_badge(self) -> None:
        self.face_badge = Badge(letter='E', rows=[
            self.Row('EVGENY',
                     css_classes=['info-badge-row-align', 'hide-on-sidebar-close'],
                     icon=MaterialIcon('keyboard_arrow_down')),
            self.Row('m3adez@gmail.com', css_classes=['info-badge-row-align', 'hide-on-sidebar-close'])
        ])

    def get_inner_badges(self) -> dict:
        return {
            'user_badge': Badge(letter='E', rows=[
                self.Row('INFO'),
                self.Row('INFO'),
                self.Row('INFO'),
                self.Row('INFO'),
                self.Row('INFO'),
                self.Row('INFO')
            ])
        }

    def get_elements(self) -> dict:
        return {
            'user_settings': self.MenuButton(
                key='user_settings_button',
                title='Настройки пользователя'
            ),
            'exit': self.MenuButton(
                key='exit_button',
                title='Выход'
            )
        }


class BaseApplicationSchema(TemplateSchema):
    """
    Базовая схема приложения
    """

    class GenericNavbar(MainNavbar):
        """
        Класс для реализации навбара приложения
        """

        template_name = 'components/bootstrap_v4/navbar/generic_navbar.html'
        unique_name = 'application_navbar'
        grouper_map = {'first_group': ['navbar_button_1'], 'second_group': ['navbar_button_2', 'navbar_button_3']}

    class GenericSidebar(MainSidebar):
        """
        Класс для реализации сайдбара приложения
        """

        template_name = 'components/bootstrap_v4/sidebar/generic_sidebar.html'
        unique_name = 'application_sidebar'
        grouper_map = {'Слова': ['random_word_set', 'exams'], 'Другое': ['words_sets_history', 'rating']}
        logo_image = MainSidebar.LogoImage(html_params={'src': '/assets/img/logo_img.png'})
        logo_title = MainSidebar.LogoTitle('26 Words Day')

    class ProfileDropdownWithBadge(ProfileDropdown):
        """
        Класс для реализации выпадающего меню профиля
        """

        template_name = 'components/bootstrap_v4/dropdown/dropdown_with_badge.html'
        unique_name = 'profile_dropdown'
        align = 'right'
        grouper_map = {'user_badge': ['user_settings', 'exit']}
