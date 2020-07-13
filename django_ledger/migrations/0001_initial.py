# Generated by Django 3.0.8 on 2020-07-13 18:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_ledger.io.mixin
import mptt.fields
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10, verbose_name='Account Code')),
                ('name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('role', models.CharField(choices=[('Assets', (('asset_ca_cash', 'Current Asset'), ('asset_ca_mkt_sec', 'Marketable Securities'), ('asset_ca_recv', 'Receivables'), ('asset_ca_inv', 'Inventory'), ('asset_ca_uncoll', 'Uncollectibles'), ('asset_ca_prepaid', 'Prepaid'), ('asset_ca_other', 'Other Liquid Assets'), ('asset_lti_notes', 'Notes Receivable'), ('asset_lti_land', 'Land'), ('asset_lti_sec', 'Securities'), ('asset_ppe', 'Property Plant & Equipment'), ('asset_ia', 'Intangible Assets'), ('asset_adjustment', 'Other Assets'))), ('Liabilities', (('lia_cl_acc_pay', 'Accounts Payable'), ('lia_cl_wage_pay', 'Wages Payable'), ('lia_cl_wage_pay', 'Interest Payable'), ('lia_cl_st_notes_payable', 'Notes Payable'), ('lia_cl_ltd_mat', 'Current Maturities of Long Tern Debt'), ('lia_cl_def_rev', 'Deferred Revenue'), ('lia_cl_other', 'Other Liabilities'), ('lia_ltl_notes', 'Notes Payable'), ('lia_ltl_bonds', 'Bonds Payable'), ('lia_ltl_mortgage', 'Mortgage Payable'))), ('Equity', (('eq_capital', 'Capital'), ('eq_stock_c', 'Common Stock'), ('eq_stock_p', 'Preferred Stock'), ('eq_adjustment', 'Other Equity Adjustments'), ('in_sales', 'Sales Income'), ('in_pass', 'Passive Income'), ('in_other', 'Other Income'), ('ex_cogs', 'Cost of Goods Sold'), ('ex_op', 'Operational Expense'), ('ex_interest', 'Interest Expense'), ('ex_taxes', 'Tax Expense'), ('ex_cap', 'Capital Expense'), ('ex_other', 'Other Expense')))], max_length=25, verbose_name='Account Role')),
                ('balance_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6, verbose_name='Account Balance Type')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntityManagementModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('permission_level', models.CharField(choices=[('read', 'Read Permissions'), ('write', 'Read/Write Permissions'), ('suspended', 'No Permissions')], default='read', max_length=10, verbose_name='Permission Level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntityModel',
            fields=[
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('address_1', models.CharField(max_length=70, verbose_name='Address Line 1')),
                ('address_2', models.CharField(blank=True, max_length=70, null=True, verbose_name='Address Line 2')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Entity Name')),
                ('hidden', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin_of', to=settings.AUTH_USER_MODEL, verbose_name='Admin')),
                ('managers', models.ManyToManyField(related_name='managed_by', through='django_ledger.EntityManagementModel', to=settings.AUTH_USER_MODEL, verbose_name='Managers')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.EntityModel', verbose_name='Parent Entity')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
                'ordering': ['-created'],
                'abstract': False,
            },
            bases=(models.Model, django_ledger.io.mixin.IOMixIn),
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ImportJobModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.EntityModel', verbose_name='Entity')),
            ],
            options={
                'verbose_name': 'Import Job Model',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JournalEntryModel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.CharField(blank=True, max_length=70, null=True, verbose_name='Description')),
                ('activity', models.CharField(choices=[('op', 'Operating'), ('fin', 'Financing'), ('inv', 'Investing'), ('other', 'Other')], max_length=5, verbose_name='Activity')),
                ('origin', models.CharField(blank=True, max_length=30, null=True, verbose_name='Origin')),
                ('posted', models.BooleanField(default=False, verbose_name='Posted')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Journal Entry',
                'verbose_name_plural': 'Journal Entries',
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tx_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10, verbose_name='Tx Type')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tx Description')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='txs', to='django_ledger.AccountModel', verbose_name='Account')),
                ('journal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txs', to='django_ledger.JournalEntryModel', verbose_name='Journal Entry')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StagedTransactionModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fitid', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_posted', models.DateField()),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('memo', models.CharField(blank=True, max_length=200, null=True)),
                ('earnings_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_ledger.AccountModel')),
                ('import_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.ImportJobModel')),
                ('tx', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_ledger.TransactionModel')),
            ],
            options={
                'verbose_name': 'Staged Transaction Model',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LedgerModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('posted', models.BooleanField(default=False, verbose_name='Posted')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to='django_ledger.EntityModel', verbose_name='Entity')),
            ],
            options={
                'verbose_name': 'Ledger',
                'verbose_name_plural': 'Ledgers',
                'ordering': ['-created'],
                'abstract': False,
            },
            bases=(models.Model, django_ledger.io.mixin.IOMixIn),
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='django_ledger.LedgerModel', verbose_name='Ledger'),
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.JournalEntryModel', verbose_name='Parent Journal Entry'),
        ),
        migrations.CreateModel(
            name='InvoiceModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('terms', models.CharField(choices=[('on_receipt', 'Due On Receipt'), ('net_30', 'Net 30 Days'), ('net_60', 'Net 60 Days'), ('net_90', 'Net 90 Days')], default='on_receipt', max_length=10, verbose_name='Terms')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Amount Due')),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Paid')),
                ('amount_receivable', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Receivable')),
                ('amount_unearned', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Unearned')),
                ('amount_earned', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Earned')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('paid_date', models.DateField(blank=True, null=True, verbose_name='Paid Date')),
                ('date', models.DateField(verbose_name='Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('void', models.BooleanField(default=False, verbose_name='Void')),
                ('void_date', models.DateField(blank=True, null=True, verbose_name='Void Date')),
                ('progressible', models.BooleanField(default=False, verbose_name='Progressible')),
                ('progress', models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=1)], verbose_name='Progress Amount')),
                ('address_1', models.CharField(max_length=70, verbose_name='Address Line 1')),
                ('address_2', models.CharField(blank=True, max_length=70, null=True, verbose_name='Address Line 2')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_to', models.CharField(max_length=100, verbose_name='Invoice To')),
                ('invoice_number', models.SlugField(max_length=20, unique=True, verbose_name='Invoice Number')),
                ('cash_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_cash_account', to='django_ledger.AccountModel', verbose_name='Cash Account')),
                ('earnings_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_earnings_account', to='django_ledger.AccountModel', verbose_name='Earnings Account')),
                ('ledger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.LedgerModel', verbose_name='Ledger')),
                ('payable_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_payable_account', to='django_ledger.AccountModel', verbose_name='Payable Account')),
                ('receivable_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_receivable_account', to='django_ledger.AccountModel', verbose_name='Receivable Account')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['-updated'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='importjobmodel',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.LedgerModel', verbose_name='Ledger'),
        ),
        migrations.AddField(
            model_name='entitymanagementmodel',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_permissions', to='django_ledger.EntityModel', verbose_name='Entity'),
        ),
        migrations.AddField(
            model_name='entitymanagementmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_permissions', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.CreateModel(
            name='ChartOfAccountModel',
            fields=[
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('description', models.TextField(blank=True, null=True, verbose_name='CoA Description')),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coa', to='django_ledger.EntityModel', verbose_name='Entity')),
            ],
            options={
                'verbose_name': 'Chart of Account',
                'verbose_name_plural': 'Chart of Accounts',
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('terms', models.CharField(choices=[('on_receipt', 'Due On Receipt'), ('net_30', 'Net 30 Days'), ('net_60', 'Net 60 Days'), ('net_90', 'Net 90 Days')], default='on_receipt', max_length=10, verbose_name='Terms')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Amount Due')),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Paid')),
                ('amount_receivable', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Receivable')),
                ('amount_unearned', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Unearned')),
                ('amount_earned', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Earned')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('paid_date', models.DateField(blank=True, null=True, verbose_name='Paid Date')),
                ('date', models.DateField(verbose_name='Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('void', models.BooleanField(default=False, verbose_name='Void')),
                ('void_date', models.DateField(blank=True, null=True, verbose_name='Void Date')),
                ('progressible', models.BooleanField(default=False, verbose_name='Progressible')),
                ('progress', models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=1)], verbose_name='Progress Amount')),
                ('address_1', models.CharField(max_length=70, verbose_name='Address Line 1')),
                ('address_2', models.CharField(blank=True, max_length=70, null=True, verbose_name='Address Line 2')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bill_to', models.CharField(max_length=100, verbose_name='Bill To')),
                ('bill_number', models.SlugField(max_length=20, unique=True, verbose_name='Bill Number')),
                ('xref', models.SlugField(blank=True, null=True, verbose_name='External Reference Number')),
                ('cash_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_cash_account', to='django_ledger.AccountModel', verbose_name='Cash Account')),
                ('earnings_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_earnings_account', to='django_ledger.AccountModel', verbose_name='Earnings Account')),
                ('ledger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.LedgerModel', verbose_name='Ledger')),
                ('payable_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_payable_account', to='django_ledger.AccountModel', verbose_name='Payable Account')),
                ('receivable_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_receivable_account', to='django_ledger.AccountModel', verbose_name='Receivable Account')),
            ],
            options={
                'verbose_name': 'Bill',
                'verbose_name_plural': 'Bills',
                'ordering': ['-updated'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankAccountModel',
            fields=[
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_number', models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\d+)*\\Z'), code='invalid', message='Only digits allowed')])),
                ('routing_number', models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\d+)*\\Z'), code='invalid', message='Only digits allowed')])),
                ('aba_number', models.CharField(blank=True, max_length=30, null=True)),
                ('account_type', models.CharField(choices=[('checking', 'Checking'), ('savings', 'Savings'), ('money_mkt', 'Money Market')], max_length=10)),
                ('cash_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_cash_account', to='django_ledger.AccountModel', verbose_name='Cash Account')),
                ('ledger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_ledger.LedgerModel', verbose_name='Ledger')),
            ],
            options={
                'verbose_name': 'Bank Account',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='coa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='django_ledger.ChartOfAccountModel', verbose_name='Chart of Accounts'),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.AccountModel', verbose_name='Parent'),
        ),
        migrations.AddIndex(
            model_name='transactionmodel',
            index=models.Index(fields=['tx_type'], name='django_ledg_tx_type_da7ba9_idx'),
        ),
        migrations.AddIndex(
            model_name='transactionmodel',
            index=models.Index(fields=['account'], name='django_ledg_account_c4bb7e_idx'),
        ),
        migrations.AddIndex(
            model_name='transactionmodel',
            index=models.Index(fields=['journal_entry'], name='django_ledg_journal_46c77f_idx'),
        ),
        migrations.AddIndex(
            model_name='transactionmodel',
            index=models.Index(fields=['created'], name='django_ledg_created_b74538_idx'),
        ),
        migrations.AddIndex(
            model_name='transactionmodel',
            index=models.Index(fields=['updated'], name='django_ledg_updated_494252_idx'),
        ),
        migrations.AddIndex(
            model_name='stagedtransactionmodel',
            index=models.Index(fields=['import_job'], name='django_ledg_import__8e6511_idx'),
        ),
        migrations.AddIndex(
            model_name='ledgermodel',
            index=models.Index(fields=['entity'], name='django_ledg_entity__e21c5d_idx'),
        ),
        migrations.AddIndex(
            model_name='ledgermodel',
            index=models.Index(fields=['entity', 'posted'], name='django_ledg_entity__040422_idx'),
        ),
        migrations.AddIndex(
            model_name='ledgermodel',
            index=models.Index(fields=['entity', 'locked'], name='django_ledg_entity__cde962_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentrymodel',
            index=models.Index(fields=['date'], name='django_ledg_date_470aff_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentrymodel',
            index=models.Index(fields=['ledger', 'parent'], name='django_ledg_ledger__e6d4a7_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentrymodel',
            index=models.Index(fields=['ledger', 'activity'], name='django_ledg_ledger__4ded91_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentrymodel',
            index=models.Index(fields=['ledger', 'posted', 'locked'], name='django_ledg_ledger__3547d4_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentrymodel',
            index=models.Index(fields=['ledger', 'date', 'activity', 'posted'], name='django_ledg_ledger__ccf075_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['cash_account'], name='django_ledg_cash_ac_00d697_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['receivable_account'], name='django_ledg_receiva_ca91df_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['payable_account'], name='django_ledg_payable_874ddd_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['earnings_account'], name='django_ledg_earning_826233_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['created'], name='django_ledg_created_9d66cb_idx'),
        ),
        migrations.AddIndex(
            model_name='invoicemodel',
            index=models.Index(fields=['updated'], name='django_ledg_updated_2bc689_idx'),
        ),
        migrations.AddIndex(
            model_name='importjobmodel',
            index=models.Index(fields=['entity'], name='django_ledg_entity__75d0e7_idx'),
        ),
        migrations.AddIndex(
            model_name='importjobmodel',
            index=models.Index(fields=['ledger'], name='django_ledg_ledger__1e8758_idx'),
        ),
        migrations.AddIndex(
            model_name='importjobmodel',
            index=models.Index(fields=['entity', 'ledger'], name='django_ledg_entity__176bc4_idx'),
        ),
        migrations.AddIndex(
            model_name='entitymodel',
            index=models.Index(fields=['admin'], name='django_ledg_admin_i_09f5c9_idx'),
        ),
        migrations.AddIndex(
            model_name='entitymanagementmodel',
            index=models.Index(fields=['entity', 'user'], name='django_ledg_entity__9541e6_idx'),
        ),
        migrations.AddIndex(
            model_name='entitymanagementmodel',
            index=models.Index(fields=['user', 'entity'], name='django_ledg_user_id_b7497b_idx'),
        ),
        migrations.AddIndex(
            model_name='chartofaccountmodel',
            index=models.Index(fields=['entity'], name='django_ledg_entity__48d6e0_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['cash_account'], name='django_ledg_cash_ac_82021a_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['receivable_account'], name='django_ledg_receiva_0236fc_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['payable_account'], name='django_ledg_payable_46e667_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['earnings_account'], name='django_ledg_earning_14e1c7_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['created'], name='django_ledg_created_41f19d_idx'),
        ),
        migrations.AddIndex(
            model_name='billmodel',
            index=models.Index(fields=['updated'], name='django_ledg_updated_f8ea81_idx'),
        ),
        migrations.AddIndex(
            model_name='bankaccountmodel',
            index=models.Index(fields=['ledger'], name='django_ledg_ledger__a7773b_idx'),
        ),
        migrations.AddIndex(
            model_name='bankaccountmodel',
            index=models.Index(fields=['cash_account', 'account_type'], name='django_ledg_cash_ac_2b8b2b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='bankaccountmodel',
            unique_together={('cash_account', 'account_number', 'routing_number')},
        ),
        migrations.AddIndex(
            model_name='accountmodel',
            index=models.Index(fields=['role'], name='django_ledg_role_812d08_idx'),
        ),
        migrations.AddIndex(
            model_name='accountmodel',
            index=models.Index(fields=['balance_type'], name='django_ledg_balance_daddac_idx'),
        ),
        migrations.AddIndex(
            model_name='accountmodel',
            index=models.Index(fields=['active'], name='django_ledg_active_f8adc2_idx'),
        ),
        migrations.AddIndex(
            model_name='accountmodel',
            index=models.Index(fields=['coa'], name='django_ledg_coa_id_b60916_idx'),
        ),
        migrations.AddIndex(
            model_name='accountmodel',
            index=models.Index(fields=['role', 'balance_type', 'active'], name='django_ledg_role_1bff96_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='accountmodel',
            unique_together={('coa', 'code')},
        ),
    ]
