from template_schema.handler import TemplateSchema
from template_schema_extensions.components.examples import NavbarExample, SidebarExample, ProfileDropdownExample


class BaseApplicationSchema(TemplateSchema):
    """
    Базовая схема приложения
    """

    class GenericNavbar(NavbarExample):
        """
        Класс для реализации навбара приложения
        """

        unique_name = 'application_navbar'

    class GenericSidebar(SidebarExample):
        """
        Класс для реализации сайдбара приложения
        """

        unique_name = 'application_sidebar'

    class ProfileDropdownWithBadge(ProfileDropdownExample):
        """
        Класс для реализации выпадающего меню профиля
        """

        unique_name = 'profile_dropdown'
