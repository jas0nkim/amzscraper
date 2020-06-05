from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from pwweb import settings, utils

class RawData(models.Model):
    url = models.TextField(db_index=True)
    domain = models.CharField(max_length=32, db_index=True)
    http_status = models.SmallIntegerField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    job_id = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at.short_description = 'collected time'

    @property
    def item_title(self):
        if self.domain in ['amazon.com', 'amazon.ca',]:
            return self.data.get('title', None)
        elif self.domain in ['walmart.com',]:
            if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox'] and len(self.data['item']['product']['buyBox']['products']) > 0 and 'productName' in self.data['item']['product']['buyBox']['products'][0]:
                return self.data['item']['product']['buyBox']['products'][0]['productName']
        else:
            return None

    @property
    def sku(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'asin' in self.data:
                    return self.data['asin']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'primaryUsItemId' in self.data['item']['product']['buyBox']:
                    return self.data['item']['product']['buyBox']['primaryUsItemId']
            elif self.domain in ['walmart.ca',]:
                if 'product' in self.data and 'item' in self.data['product'] and 'skus' in self.data['product']['item']:
                    return truncatechars(','.join(self.data['product']['item']['skus']), 50)
        else:
            return None

    @property
    def price(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'price' in self.data:
                    return self.data['price']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox']:
                    return self.data['item']['product']['buyBox']['products'][0]['priceMap']['price']
            elif self.domain in ['walmart.ca',]:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['currentPrice']
                    return truncatechars(str(prices), 50)
        else:
            return None

    @property
    def quantity(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'quantity' in self.data:
                    return self.data['quantity']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox']:
                    if self.data['item']['product']['buyBox']['products'][0]['availabilityStatus'] == 'OUT_OF_STACK':
                        return 'out of stock'
                    elif self.data['item']['product']['buyBox']['products'][0]['availabilityStatus'] == 'IN_STOCK':
                        if self.data['item']['product']['buyBox']['products'][0]['urgentQuantity']:
                            return self.data['item']['product']['buyBox']['products'][0]['urgentQuantity']
                        else:
                            return 'in stock'
                    else:
                        return 'N/A'
            elif self.domain in ['walmart.ca',]:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['availableQuantity']
                    return truncatechars(str(prices), 50)
        else:
            return None

    def url_short(self):
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(self.url, truncatechars(self.url, 50)))
    url_short.short_description = 'url'

    def item_title_short(self):
        return truncatechars(self.item_title, 50)
    item_title_short.short_description = 'title'

    class Meta:
        db_table = 'resrc_raw_data'


class Item(models.Model):
    domain = models.CharField(max_length=32, db_index=True)
    sku = models.CharField(max_length=32, db_index=True)
    upc = models.CharField(max_length=20, blank=True, null=True)
    title = models.TextField()
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    picture_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resrc_items'


class ItemPrice(models.Model):
    domain = models.CharField(max_length=32, db_index=True)
    sku = models.CharField(max_length=32, db_index=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    store_location = models.CharField(max_length=255, blank=True, null=True)
    job_id = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resrc_item_prices'


class BuildItemPrice:
    """ build resrc_item_prices data from resrc_raw_data
    """

    _raw_data = None
    _domain = None
    _url = None
    _data = None

    _item = None
    _item_price = None

    def __init__(self, raw_data=None):
        if not isinstance(raw_data, RawData):
            raise Exception('Invalid raw_data value passed. Not a RawData type')
        self._job_id = raw_data.job_id
        self._domain = raw_data.domain
        self._url = raw_data.url
        self._data = raw_data.data

        if self._domain in ['amazon.com', 'amazon.ca',]:
            self._build_amazon_item_price()
        elif self._domain in ['walmart.com',]:
            self._build_walmart_com_item_price()
        elif self._domain in ['walmart.ca',]:
            self._build_walmart_ca_item_price()
        elif self._domain in ['canadiantire.ca',]:
            self._build_canadiantire_ca_item_price()

    def get_item(self):
        """ get model.Item object
        """
        return self._item

    def get_item_price(self):
        """ get model.ItemPrice object
        """
        return self._item_price

    def _build_amazon_item_price(self):
        """ 1. validate url
            2. check item already exist in resrc_items table
            3. extract and store values
                - sku
                - price
                - original price
                - quantity
        """
        sku = utils.extract_sku_from_url(url=self._url, domain=self._domain)
        if sku is None:
            raise Exception('SKU cannot be extracted from url - {}'.format(self._url))
        try:
            self._item = Item.objects.get(domain=self._domain, sku=sku)
        except Item.DoesNotExist:
            # create new item
            self._item = Item(domain=self._domain,
                        sku=sku,
                        upc=None,
                        title=self._data['title'],
                        brand_name=self._data.get('brand_name', None),
                        picture_url=self._data.get('picture_urls', [])[0] if len(self._data.get('picture_urls', [])) > 0 else None,
                    )
            self._item.save()
        self._item_price = ItemPrice(domain=self._domain,
                    sku=sku,
                    price=self._data['price'],
                    original_price=self._data['original_price'],
                    quantity=self._data['quantity'],
                    store_location=None,
                    job_id=self._job_id,
                )
        self._item_price.save()

    def _build_walmart_com_item_price(self):
        """ title: data['item']['product']['buyBox']['products'][0]['productName']
            brand: data['item']['product']['buyBox']['products'][0]['brandName']
            upc: data['item']['product']['buyBox']['products'][0]['upc']
        """
        pass

    def _build_walmart_ca_item_price(self):
        pass

    def _build_canadiantire_ca_item_price(self):
        pass

# class AmazonParentListing(models.Model):
#     parent_asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     asins = ArrayField(
#         base_field=models.CharField(max_length=32, blank=True, null=True), blank=True,
#         null=True)
#     review_count = models.SmallIntegerField(blank=True, null=True, default=0)
#     avg_rating = models.FloatField(blank=True, null=True, default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.parent_asin

#     class Meta:
#         db_table = 'resrc_amazon_parent_listings'
#         constraints = [
#             models.UniqueConstraint(fields=['parent_asin', 'domain'],name='unique_parent_asin_domain')
#         ]


# class AmazonListing(models.Model):
#     asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     parent_asin = models.CharField(max_length=32, db_index=True)
#     picture_urls = ArrayField(
#         base_field=models.CharField(
#             max_length=255, blank=True, null=True),
#         null=True)
#     url = models.TextField()
#     category = models.CharField(max_length=255, blank=True, null=True)
#     title = models.TextField()
#     price = models.DecimalField(max_digits=15, decimal_places=2)
#     original_price = models.DecimalField(max_digits=15, decimal_places=2)
#     quantity = models.SmallIntegerField(blank=True, null=True, default=0)
#     features = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     specifications = models.TextField(blank=True, null=True)
#     variation_specifics = models.CharField(max_length=255, blank=True, null=True)
#     is_fba = models.BooleanField(default=0)
#     is_addon = models.BooleanField(default=0)
#     is_pantry = models.BooleanField(default=0)
#     has_sizechart = models.BooleanField(default=0)
#     international_shipping = models.BooleanField(default=0)
#     merchant_id = models.CharField(max_length=32, blank=True, null=True)
#     merchant_name = models.CharField(max_length=100, blank=True, null=True)
#     brand_name = models.CharField(max_length=100, blank=True, null=True)
#     meta_title = models.TextField(blank=True, null=True)
#     meta_description = models.TextField(blank=True, null=True)
#     meta_keywords = models.TextField(blank=True, null=True)
#     status = models.SmallIntegerField(blank=True, null=True, default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return "[{}] {}".format(self.asin, self.title)

#     def save(self, *args, **kwargs):
#         try:
#             super().save(*args, **kwargs)
#         except ValueError as ve:
#             raise ve
#         except Exception as e:
#             raise e
#         # insert new price, original_price
#         self._save_listing_price()

#     def _save_listing_price(self):
#         new_listing_price = AmazonListingPrice()
#         new_listing_price.asin = self.asin
#         new_listing_price.domain = self.domain
#         new_listing_price.price = self.price
#         new_listing_price.original_price = self.original_price
#         new_listing_price.save()

#     class Meta:
#         db_table = 'resrc_amazon_listings'
#         constraints = [
#             models.UniqueConstraint(fields=['asin', 'domain'],name='unique_asin_domain')
#         ]


# class AmazonListingPrice(models.Model):
#     asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     price = models.DecimalField(max_digits=15, decimal_places=2)
#     original_price = models.DecimalField(max_digits=15, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "{}".format(self.asin)

#     class Meta:
#         db_table = 'resrc_amazon_listing_prices'
#         constraints = [
#             models.UniqueConstraint(fields=['asin', 'domain'],name='unique_asin_price_domain')
#         ]
