from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import StructBlock, StreamBlock, CharBlock, RichTextBlock, PageChooserBlock, ChoiceBlock, \
    BooleanBlock, URLBlock, IntegerBlock

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, \
    PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.snippets.models import register_snippet

from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_snippet
class FrameSnippet(Orderable, models.Model):
    frame_name = models.CharField(max_length=255, blank=True, null=True)
    frame_description = RichTextField(blank=True)
    frame_images = StreamField([
        ('image', ImageChooserBlock(blank=True, required=False))
    ], blank=True)

    panels = [
        FieldPanel('frame_name'),
        FieldPanel('frame_description'),
        StreamFieldPanel('frame_images'),
    ]

    def __str__(self):
        return self.frame_name

    class Meta:
        verbose_name_plural = 'Frame Snippets'


class PrintSeries(Page):
    footer_colour = models.CharField(max_length=255, blank=True, null=True)
    """ All Series Page """
    year = models.CharField(max_length=255, blank=True, null=True)
    series_description = RichTextField(blank=True)
    print_type = models.CharField(max_length=255, blank=True, null=True, help_text='E.g "Photogram Screen Print"')
    edition = models.CharField('Edition of', max_length=255, blank=True, null=True)
    dim_x = models.IntegerField(blank=True, null=True)
    dim_y = models.IntegerField(blank=True, null=True)

    items = StreamField([
        ('item', StructBlock([
            ('select_page', PageChooserBlock(blank=True))
        ])),
    ], blank=True)

    story = StreamField([
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
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('caption', CharBlock(required=False)),
            ('size', ChoiceBlock(required=False, max_length=20, choices=(
                (u'4', u'Small'),
                (u'6', u'Medium'),
                (u'8', u'Large'),
            ))),
        ],
            template='home/blocks/image.html',
            icon='image'))
    ], blank=True)

    behind_the_scenes = StreamField([
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
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('caption', CharBlock(required=False)),
            ('size', ChoiceBlock(required=False, max_length=20, choices=(
                (u'4', u'Small'),
                (u'6', u'Medium'),
                (u'8', u'Large'),
            ))),
        ],
            template='home/blocks/image.html',
            icon='image'))
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('year'),
        FieldPanel('edition'),
        FieldPanel('print_type'),
        FieldPanel('dim_x'),
        FieldPanel('dim_y'),
        FieldPanel('series_description'),
        StreamFieldPanel('items'),
        StreamFieldPanel('story'),
        StreamFieldPanel('behind_the_scenes'),
    ]

    promote_panels = [
                         FieldPanel('footer_colour'),
                     ] + Page.promote_panels


class Product(Page):
    @property
    def page_class(self):
        return 'Product'

    @property
    def getInitalPrice(self):
        """ base price + first attribute price variant """
        return str(self.base_price + dict(self.product_attributes[0].__dict__['value'])['price_variation'])

    @property
    def getLowestPrice(self):
        return str(self.base_price)

    @property
    def parent_series(self):
        try:
            parent_series = PrintSeries.objects.parent_of(self).live().first()
            return parent_series
        except:
            return None

    @property
    def sibling_products(self):
        try:
            sibling_products = Product.objects.live().sibling_of(self, inclusive=False)
            return sibling_products
        except:
            return None

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    footer_colour = models.CharField(max_length=255, blank=True, null=True)

    product_description = RichTextField(blank=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    edition = models.IntegerField('Edition of', null=True, blank=True)
    print_type = models.CharField(max_length=255, blank=True, null=True, help_text='E.g "Photogram Screen Print"')
    edition = models.CharField('Edition of', max_length=255, blank=True, null=True)
    dim_x = models.IntegerField(blank=True, null=True)
    dim_y = models.IntegerField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # product_index = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    quantity_available = models.IntegerField('Quantity Available', null=True, blank=True)
    out_of_stock = models.BooleanField(default=False)
    shipping_weight = models.FloatField('Shipping Weight', null=True, blank=True)
    free_uk_shipping = models.BooleanField('Free UK Shipping', default=False)

    # exclude_from_available_stock = models.BooleanField(default=False)

    product_images = StreamField([
        ('add_item', StructBlock([
            ('image', ImageChooserBlock(blank=True, required=False)),
        ], icon='image'))
    ], blank=True)

    product_attributes = StreamField([
        ('add_attribute', StructBlock([
            ('title', CharBlock(blank=True, null=True, required=False, classname="full title", icon='title')),
            ('image', ImageChooserBlock(blank=True, required=False)),
            ('dim_x', IntegerBlock(blank=True, null=True, required=False)),
            ('dim_y', IntegerBlock(blank=True, null=True, required=False)),
            ('dim_z', IntegerBlock(required=False)),
            ('price_variation', IntegerBlock(blank=True, null=True)),
            ('quantity_available', IntegerBlock(required=False)),
        ], icon='plus'))
    ], blank=True)

    OVERRIDE_SERIES_CLUSTER = [
        FieldPanel('product_description'),
        FieldPanel('year'),
        FieldPanel('edition'),
        FieldPanel('print_type'),
        FieldPanel('dim_x'),
        FieldPanel('dim_y'),
    ]

    PRICE_CLUSTER = [
        # FieldPanel('product_index'),
        FieldPanel('base_price'),
        FieldPanel('quantity_available'),
        FieldPanel('out_of_stock'),
        FieldPanel('shipping_weight'),
        FieldPanel('free_uk_shipping'),
    ]

    content_panels = Page.content_panels + [
        # FieldPanel('view'),
        ImageChooserPanel('thumbnail'),
        MultiFieldPanel(OVERRIDE_SERIES_CLUSTER, heading="Override Parent Series Settings",
                        classname="collapsible collapsed"),
        MultiFieldPanel(PRICE_CLUSTER, heading="Price details"),
        StreamFieldPanel('product_images'),
        StreamFieldPanel('product_attributes'),
    ]

    promote_panels = [
                         FieldPanel('footer_colour'),
                     ] + Page.promote_panels


class RelatedObjects(models.Model):
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def link(self):
        return self.link_page

    panels = [
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


# --- promotion ---
class Promotion(models.Model):
    """ Basic order Ssipping costs. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=6, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    discount_value = models.DecimalField(
        verbose_name="Discount Value (%)",
        decimal_places=2, max_digits=5,
        default=0.0
    )
    discount_amount = models.DecimalField(
        verbose_name="Discount Amount (£)",
        decimal_places=2, max_digits=6,
        default=0.0
    )
    free_shipping = models.BooleanField(default=False)
    quantity_available = models.IntegerField(default=1)

    selected_item = models.ForeignKey('wagtailcore.Page', on_delete=models.CASCADE, null=True, blank=True,
                                      help_text='A specific Product or Event')

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    panels = [
        FieldPanel('title'),
        MultiFieldPanel([FieldPanel('start_date'), FieldPanel('end_date')], heading='Date Range'),
        MultiFieldPanel([FieldPanel('discount_value'), FieldPanel('discount_amount'), FieldPanel('free_shipping')],
                        heading='Discount'),
        FieldPanel('quantity_available'),

        MultiFieldPanel([FieldPanel('user'), PageChooserPanel('selected_item')], heading='Selection'),
    ]

    def __str__(self):
        return self.title

    def clean(self):
        if (self.discount_amount <= 0 and self.discount_value <= 0) \
                or (self.discount_amount > 0 and self.discount_value > 0):
            # raise ValidationError(_('You should define either discount_amount or discount_value.'))
            raise ValidationError({'discount_amount': 'You should define only discount_amount or discount_value.',
                                   'discount_value': 'You should define only discount_amount or discount_value.'})

        if self.discount_value > 100 or self.discount_value < 0:
            raise ValidationError({'discount_value': 'Invalid Discount value'})

        if self.discount_amount < 0:
            raise ValidationError({'discount_value': 'Invalid Discount amount'})


@register_snippet
class ShopOrder(ClusterableModel):
    """ Order Snippet """
    order_created = models.DateTimeField('Created', auto_now_add=True)
    email = models.EmailField('Email', null=True, blank=True)
    telephone = models.CharField('Telephone', null=True, blank=True, max_length=255)
    invoice_notes = RichTextField(blank=True)

    billing_name = models.CharField('Billing Name', null=True, blank=False, max_length=255)
    billing_address1 = models.CharField('Billing Address 1', null=True, blank=True, max_length=255)
    billing_address2 = models.CharField('Billing Address 2', null=True, blank=True, max_length=255)
    billing_address3 = models.CharField('Billing Address 3', null=True, blank=True, max_length=255)
    billing_postcode = models.CharField('Billing Postcode', null=True, blank=True, max_length=255)
    billing_state = models.CharField('Billing State', null=True, blank=True, max_length=255)
    billing_city = models.CharField('Billing City', null=True, blank=True, max_length=255)
    billing_country = models.CharField('Billing Country', null=True, blank=True, max_length=255)

    shipping_name = models.CharField('Shipping Name', null=True, blank=True, max_length=255)
    shipping_address1 = models.CharField('Shipping Address 1', null=True, blank=True, max_length=255)
    shipping_address2 = models.CharField('Shipping Address 2', null=True, blank=True, max_length=255)
    shipping_address3 = models.CharField('Shipping Address 3', null=True, blank=True, max_length=255)
    shipping_postcode = models.CharField('Shipping Postcode', null=True, blank=True, max_length=255)
    shipping_state = models.CharField('Shipping State', null=True, blank=True, max_length=255)
    shipping_city = models.CharField('Shipping City', null=True, blank=True, max_length=255)
    shipping_country = models.CharField('Shipping Country', null=True, blank=True, max_length=255)

    order_total = models.DecimalField('Order', null=True, blank=True, max_digits=6, decimal_places=2, default=0)
    shipping_charged = models.DecimalField('Shipping Charged', null=True, blank=True, max_digits=6, decimal_places=2,
                                           default=0)
    shipped = models.DateTimeField('Shipped', null=True, blank=True)
    transaction_id = models.CharField('WorldPay Transaction ID', null=True, blank=True, max_length=255)

    shipping_tracking_code = models.CharField(null=True, blank=True, max_length=255)

    @property
    def total_price(self):
        return self.order_total + self.shipping_charged

    ORDER_PRICE = [
        FieldRowPanel([
            FieldPanel('order_total'),
            FieldPanel('shipping_charged'),
        ])
    ]

    panels = [
        # FieldPanel('order_created'),
        FieldPanel('email'),
        FieldPanel('telephone'),
        FieldPanel('invoice_notes', classname="full"),
        MultiFieldPanel(ORDER_PRICE, heading="Order Price"),
        InlinePanel('order_items', label='Items'),
        FieldPanel('billing_name'),
        FieldPanel('billing_address1'),
        FieldPanel('billing_address2'),
        FieldPanel('billing_address3'),
        FieldPanel('billing_postcode'),
        FieldPanel('billing_state'),
        FieldPanel('billing_city'),
        FieldPanel('billing_country'),
        FieldPanel('shipping_name'),
        FieldPanel('shipping_address1'),
        FieldPanel('shipping_address2'),
        FieldPanel('shipping_address3'),
        FieldPanel('shipping_postcode'),
        FieldPanel('shipping_state'),
        FieldPanel('shipping_city'),
        FieldPanel('shipping_country'),
        FieldPanel('shipping_tracking_code'),
        FieldPanel('shipped'),
        FieldPanel('transaction_id'),
    ]

    def __unicode__(self):
        return u'{}'.format(self.id or 'Not paid')

    def save(self, send_notification=True, *args, **kwargs):
        if send_notification:
            try:
                shop_order = ShopOrder.objects.get(id=self.id)
                # if self.shipped and not shop_order.shipped:
                #     send_shipping_confirmation(self)
            except ShopOrder.DoesNotExist:
                pass
        super(ShopOrder, self).save(**kwargs)

    class Meta:
        ordering = ['-order_created']
        verbose_name = "Shop Order"
        verbose_name_plural = "Shop Orders"


class ShopOrderItem(models.Model):
    """ Basket Item Snippet """
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT)
    order = ParentalKey(ShopOrder, related_name='order_items')
    attribute = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField('Quantity', default=1, null=False, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __unicode__(self):
        return u'{} {}'.format(self.product, self.quantity)
        # return u'{} {}'.format(self.product or self.publication, self.quantity)

    class Meta:
        verbose_name = "Shop Order Item"
        verbose_name_plural = "Shop Order Items"


@register_snippet
class ShopShipping(models.Model):
    """ Shipping Snippet """
    min_weight = models.FloatField('Minimum Weight', null=False, blank=False)
    max_weight = models.FloatField('Maximum Weight', null=False, blank=False)
    uk_price = models.FloatField('United Kingdom Price', null=False, blank=False)
    europe_price = models.FloatField('Europe Price', null=False, blank=False)
    row_price = models.FloatField('Rest of World Price', null=False, blank=False)

    panels = [
        MultiFieldPanel([FieldPanel('min_weight'), FieldPanel('max_weight')], heading='Weight Range'),
        MultiFieldPanel([FieldPanel('uk_price'), FieldPanel('europe_price'), FieldPanel('row_price')],
                        heading='Shipping Price')
    ]

    def __unicode__(self):
        return u'[ {} g - {} g ] UK: {}, EU: {}, Other: {}'.format(
            self.min_weight,
            self.max_weight,
            self.uk_price,
            self.europe_price,
            self.row_price)

    class Meta:
        ordering = ['min_weight', 'max_weight']
        verbose_name = "Shop Shipping"
        verbose_name_plural = "Shop Shippings"


class AvailableStock(RoutablePageMixin, Page):
    @route(r'^all/$')
    def view_all(self, request):
        stock = Product.objects.live().filter(exclude_from_available_stock=False, out_of_stock=False,
                                              quantity_available__gt=0).order_by('-date_added', '-last_published_at')
        return render(request, 'shop/available_stock.html', {
            'is_availble_page': True,
            'page': self,
            'stock': stock,
            'artist_option': 'All Artists',
            'order': 'Order By',
        })

    @route(r'^older/$')
    def view_older(self, request):
        stock = Product.objects.live().filter(exclude_from_available_stock=False, out_of_stock=False,
                                              quantity_available__gt=0).order_by('date_added', 'last_published_at')
        return render(request, 'shop/available_stock.html', {
            'is_availble_page': True,
            'page': self,
            'stock': stock,
            'artist_option': 'All Artists',
            'order': 'Older',
        })

    @route(r'^newer/$')
    def view_newer(self, request):
        stock = Product.objects.live().filter(exclude_from_available_stock=False, out_of_stock=False,
                                              quantity_available__gt=0).order_by('-date_added', '-last_published_at')
        return render(request, 'shop/available_stock.html', {
            'is_availble_page': True,
            'page': self,
            'stock': stock,
            'artist_option': 'All Artists',
            'order': 'Newer',
        })

    # TODO: only grab that has available products
    def all_artists(self):
        stock = Product.objects.live().filter(exclude_from_available_stock=False, out_of_stock=False,
                                              quantity_available__gt=0).order_by('-date_added', '-last_published_at')
        artists = []
        for product in stock:
            artist = str(product.parent_artist)
            if artist not in artists:
                artists.append(artist)
        return artists

    content_panels = Page.content_panels + [

    ]


class Country(models.Model):
    """ Basic order Country. """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "%s" % self.name


class VAT(models.Model):
    """ Basic vat settings. """
    name = models.CharField(max_length=50)
    countries = models.ManyToManyField(Country)

    class Meta:
        ordering = ['name']
        verbose_name = 'VAT setting'
        verbose_name_plural = 'VAT settings'

    def __str__(self):
        return "%s" % self.name
