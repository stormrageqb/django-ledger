from random import choices
from string import ascii_uppercase, digits
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.utils.translation import gettext_lazy as _

from django_ledger.models import EntityModel
from django_ledger.models.mixins import CreateUpdateMixIn, ProgressibleMixIn, ContactInfoMixIn

BILL_NUMBER_CHARS = ascii_uppercase + digits


def generate_bill_number(length: int = 10):
    return 'B-' + ''.join(choices(BILL_NUMBER_CHARS, k=length))


class BillModelManager(models.Manager):

    def for_user(self, user_model):
        return self.get_queryset().filter(
            Q(ledger__entity__admin=user_model) |
            Q(ledger__entity__managers__in=[user_model])
        )

    def on_entity(self, entity):
        if isinstance(entity, EntityModel):
            return self.get_queryset().filter(ledger__entity=entity)
        elif isinstance(entity, str):
            return self.get_queryset().filter(ledger__entity__slug__exact=entity)


class BillModelAbstract(ProgressibleMixIn,
                        ContactInfoMixIn,
                        CreateUpdateMixIn):
    REL_NAME_PREFIX = 'bill'
    IS_DEBIT_BALANCE = False
    ALLOW_MIGRATE = True

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    bill_to = models.CharField(max_length=100, verbose_name=_('Bill To'))
    bill_number = models.SlugField(max_length=20, unique=True, verbose_name=_('Bill Number'))
    xref = models.SlugField(null=True, blank=True, verbose_name=_('External Reference Number'))

    cash_account = models.ForeignKey('django_ledger.AccountModel',
                                     on_delete=models.CASCADE,
                                     verbose_name=_('Cash Account'),
                                     related_name=f'{REL_NAME_PREFIX}_cash_account')
    receivable_account = models.ForeignKey('django_ledger.AccountModel',
                                           on_delete=models.CASCADE,
                                           verbose_name=_('Receivable Account'),
                                           related_name=f'{REL_NAME_PREFIX}_receivable_account')
    payable_account = models.ForeignKey('django_ledger.AccountModel',
                                        on_delete=models.CASCADE,
                                        verbose_name=_('Payable Account'),
                                        related_name=f'{REL_NAME_PREFIX}_payable_account')
    earnings_account = models.ForeignKey('django_ledger.AccountModel',
                                         on_delete=models.CASCADE,
                                         verbose_name=_('Earnings Account'),
                                         related_name=f'{REL_NAME_PREFIX}_earnings_account')

    objects = BillModelManager()

    class Meta:
        abstract = True
        ordering = ['-updated']
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')
        indexes = [
            models.Index(fields=['cash_account']),
            models.Index(fields=['receivable_account']),
            models.Index(fields=['payable_account']),
            models.Index(fields=['earnings_account']),
            models.Index(fields=['created']),
            models.Index(fields=['updated']),
        ]

    def __str__(self):
        return f'Bill: {self.bill_number}'

    def get_migrate_state_desc(self):
        """
        Must be implemented.
        :return:
        """
        return f'Bill {self.bill_number} account adjustment.'

    def clean(self):
        if not self.bill_number:
            self.bill_number = generate_bill_number()

        # todo: this is not executing the mixin clean() method...???
        super().clean()


class BillModel(BillModelAbstract):
    REL_NAME_PREFIX = 'bill'
    """
    Bill Model
    """


def billmodel_predelete(instance: BillModel, **kwargs):
    instance.ledger.delete()


post_delete.connect(receiver=billmodel_predelete, sender=BillModel)