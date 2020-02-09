from flex_forms.components import BaseButton, HTMLElementType, BaseHtmlElement, MaterialIcon


# region Flex Forms

class BaseLink(BaseButton):
    """
    Класс ссылки для flex-форм.
    """

    tag = 'a'


class DescriptionLink(BaseButton):
    """
    Класс ссылки c описанием для flex-форм.
    """

    html_string: str = '<%(tag)s>%(icon)s %(description)s <a %(html_params)s>%(data)s</a></%(tag)s>'
    tag = 'span'

    def __init__(self,
                 description: str,
                 data: str,
                 css_classes: list = None,
                 html_params: dict = None,
                 icon: HTMLElementType = None) -> None:

        self.description = description
        super().__init__(data, css_classes, html_params, icon)

    def get_format_kwargs(self, **kwargs) -> dict:
        return super().get_format_kwargs(description=self.description)

# endregion


class Img(BaseHtmlElement):
    """
    Класс изображения.
    """

    tag = 'img'
    html_string = '<%(tag)s %(html_params)s>'

    def __init__(self, **kwargs) -> None:
        super().__init__(data='', **kwargs)

    def __str__(self):
        return self.render()


class Link(BaseLink):
    """
    Класс простой ссылки.
    """

    def __str__(self):
        return self.render()


class TemplateMaterialIcon(MaterialIcon):
    """
    Иконка material для использования в шаблонах (авторендеринг)
    """

    def __str__(self):
        return self.render()
