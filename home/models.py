from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import StructBlock, StreamBlock, CharBlock, RichTextBlock, PageChooserBlock, ChoiceBlock, \
    BooleanBlock, URLBlock

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render
from django.template.response import TemplateResponse


class HomePage(RoutablePageMixin, Page):
    footer_colour = models.CharField("Hover colour", max_length=255, blank=True, null=True)
    splash_items = StreamField([
        ('image', StructBlock([
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('title', CharBlock(required=False)),
            ('page_link', PageChooserBlock(blank=True))
        ],
            icon='image')),
    ], blank=True)

    @route('^checkout/$')
    def checkout(self, request):
        context = self.get_context(request)
        return TemplateResponse(request, 'shop/checkout.html', context)

    @route('^amend-basket/$')
    def amend_basket(self, request):
        context = self.get_context(request)
        return TemplateResponse(request, 'shop/amend_basket.html', context)

    content_panels = Page.content_panels + [
        StreamFieldPanel('splash_items'),
    ]

    promote_panels = [
                         FieldPanel('footer_colour'),
                     ] + Page.promote_panels


class OverviewPage(Page):
    content_panels = Page.content_panels + [
    ]


class ComplexPage(Page):
    footer_colour = models.CharField("Hover colour", max_length=255, blank=True, null=True)
    story = StreamField([
        ('new_line_break', BooleanBlock(required=False, default=False)),
        ('title', CharBlock(blank=True, classname="full title", template='home/blocks/inner_title.html', icon='title')),
        ('text_block', StructBlock([
            ('text', RichTextBlock(blank=True)),
            ('size', ChoiceBlock(required=False, max_length=20, choices=(
                (u'6', u'Half'),
                (u'9', u'Full'),
            ))),
        ],
            template='home/blocks/text.html',
            icon='pilcrow')),
        ('image', StructBlock([
            ('new_line_break', BooleanBlock(required=False, default=False)),
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('caption', CharBlock(required=False)),
            ('size', ChoiceBlock(required=False, max_length=20, choices=(
                (u'4', u'Small'),
                (u'6', u'Medium'),
                (u'8', u'Large'),
            ))),
        ],
            template='home/blocks/image.html',
            icon='image')),
        ('slideshow', StreamBlock([
            ('slide', StructBlock([
                ('image', ImageChooserBlock(blank=True, required=False)),
                ('caption', CharBlock(required=False)),
            ], icon='image'))
        ],
            template='home/blocks/slideshow.html',
            icon='code')),
        ('visual_link', StructBlock([
            ('new_line_break', BooleanBlock(required=False, default=False)),
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('title', CharBlock(required=False)),
            ('size', ChoiceBlock(required=False, max_length=20, choices=(
                (u'4', u'Small'),
                (u'6', u'Medium'),
                (u'8', u'Large'),
            ))),
            ('page_link', PageChooserBlock(blank=True))
        ],
            template='home/blocks/visual_link.html',
            icon='image')),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('story'),
    ]

    promote_panels = [
                         FieldPanel('footer_colour'),
                     ] + Page.promote_panels


class Plain(Page):
    footer_colour = models.CharField("Hover colour", max_length=255, blank=True, null=True)
    plain_text = RichTextField(blank=True)
    page_content = StreamField([
        ('text_block', StructBlock([
            ('text', RichTextBlock(blank=True)),
            ('width', ChoiceBlock(required=False, max_length=20, choices=(
                (u'6', u'half'),
                (u'8', u'third'),
            ))),
        ],
            template='home/blocks/text.html',
            icon="pilcrow"
        )),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('plain_text'),
        StreamFieldPanel('page_content'),
    ]
    promote_panels = [
                         FieldPanel('footer_colour'),
                     ] + Page.promote_panels
